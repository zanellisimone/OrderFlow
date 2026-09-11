import sqlite3
import tempfile
import unittest

from pathlib import Path
from contextlib import closing

from database.database_manager import DatabaseManager
from model import Client, Product, OrderStatus
from services import OrderFlowManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp_dir.name)

        self.database = DatabaseManager(self.directory)

        self.manager = OrderFlowManager()

        self.client1 = Client(
            id_client="C0001",
            name="Mario",
            surname="Rossi",
            email="mario.rossi@example.com",
            phone="+393331234567"
        )

        self.client2 = Client(
            id_client="C0002",
            name="Anna",
            surname="Bianchi",
            email="anna.bianchi@example.com"
        )

        self.product1 = Product(
            id_product="P0001",
            name="Mechanical Keyboard",
            category="Peripherals",
            price=79.90,
            quantity_available=10
        )

        self.product2 = Product(
            id_product="P0002",
            name="Mouse",
            category="Peripherals",
            price=29.90,
            quantity_available=20
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    # --------------------------------------------------
    # DATABASE CREATION
    # --------------------------------------------------

    def test_database_file_is_created(self):
        database_file = (
            self.directory
            / "order_flow_database.db"
        )

        self.assertTrue(database_file.exists())

    def test_tables_are_created(self):
        database_file = (
            self.directory
            / "order_flow_database.db"
        )

        with closing(
            sqlite3.connect(database_file)
        ) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table';
                """
            )

            tables = {
                row[0]
                for row in cursor.fetchall()
            }

        self.assertIn("clients", tables)
        self.assertIn("products", tables)
        self.assertIn("orders", tables)
        self.assertIn("order_lines", tables)

    def test_invalid_directory_type(self):
        with self.assertRaises(TypeError):
            DatabaseManager("invalid")

    # --------------------------------------------------
    # EMPTY MANAGER
    # --------------------------------------------------

    def test_save_and_load_empty_manager(self):
        self.database.save(self.manager)

        loaded_manager = self.database.load()

        self.assertEqual(
            loaded_manager.get_clients(),
            ()
        )

        self.assertEqual(
            loaded_manager.get_products(),
            ()
        )

        self.assertEqual(
            loaded_manager.get_orders(),
            ()
        )

    # --------------------------------------------------
    # CLIENTS
    # --------------------------------------------------

    def test_save_and_load_client(self):
        self.manager.add_client(
            self.client1
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_client = (
            loaded_manager.get_client(
                "C0001"
            )
        )

        self.assertEqual(
            loaded_client.id_client,
            "C0001"
        )

        self.assertEqual(
            loaded_client.name,
            "Mario"
        )

        self.assertEqual(
            loaded_client.surname,
            "Rossi"
        )

        self.assertEqual(
            loaded_client.email,
            "mario.rossi@example.com"
        )

        self.assertEqual(
            loaded_client.phone,
            "+393331234567"
        )

    def test_save_and_load_client_without_phone(self):
        self.manager.add_client(
            self.client2
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_client = (
            loaded_manager.get_client(
                "C0002"
            )
        )

        self.assertIsNone(
            loaded_client.phone
        )

    # --------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------

    def test_save_and_load_product(self):
        self.manager.add_product(
            self.product1
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_product = (
            loaded_manager.get_product(
                "P0001"
            )
        )

        self.assertEqual(
            loaded_product.id_product,
            "P0001"
        )

        self.assertEqual(
            loaded_product.name,
            "Mechanical Keyboard"
        )

        self.assertEqual(
            loaded_product.category,
            "Peripherals"
        )

        self.assertAlmostEqual(
            loaded_product.price,
            79.90
        )

        self.assertEqual(
            loaded_product.quantity_available,
            10
        )

    # --------------------------------------------------
    # ORDERS
    # --------------------------------------------------

    def test_save_and_load_draft_order(self):
        self.manager.add_client(
            self.client1
        )

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        creation_date = order.creation_date

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertEqual(
            loaded_order.id_order,
            "O0001"
        )

        self.assertEqual(
            loaded_order.client.id_client,
            "C0001"
        )

        self.assertEqual(
            loaded_order.status,
            OrderStatus.DRAFT
        )

        self.assertEqual(
            loaded_order.creation_date,
            creation_date
        )

    def test_save_and_load_confirmed_order(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            2
        )

        self.manager.confirm_order(
            "O0001"
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertEqual(
            loaded_order.status,
            OrderStatus.CONFIRMED
        )

    def test_save_and_load_shipped_order(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            1
        )

        self.manager.confirm_order(
            "O0001"
        )

        self.manager.ship_order(
            "O0001"
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertEqual(
            loaded_order.status,
            OrderStatus.SHIPPED
        )

    def test_save_and_load_cancelled_order(self):
        self.manager.add_client(
            self.client1
        )

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        order.cancel()

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertEqual(
            loaded_order.status,
            OrderStatus.CANCELLED
        )

    # --------------------------------------------------
    # ORDER LINES
    # --------------------------------------------------

    def test_save_and_load_order_lines(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.add_product(
            self.product2
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            2
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0002",
            3
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertEqual(
            len(loaded_order),
            2
        )

        lines_by_product = {
            line.product.id_product: line
            for line in loaded_order.lines
        }

        self.assertEqual(
            lines_by_product["P0001"].quantity,
            2
        )

        self.assertEqual(
            lines_by_product["P0002"].quantity,
            3
        )

    # --------------------------------------------------
    # HISTORICAL UNIT PRICE
    # --------------------------------------------------

    def test_historical_unit_price_is_preserved(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            2
        )

        original_unit_price = (
            order.lines[0].unit_price
        )

        self.product1.price = 99.90

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        loaded_product = (
            loaded_manager.get_product(
                "P0001"
            )
        )

        self.assertAlmostEqual(
            loaded_product.price,
            99.90
        )

        self.assertAlmostEqual(
            loaded_order.lines[0].unit_price,
            original_unit_price
        )

        self.assertAlmostEqual(
            loaded_order.lines[0].unit_price,
            79.90
        )

    # --------------------------------------------------
    # STOCK
    # --------------------------------------------------

    def test_stock_after_confirmation_is_preserved(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order(
            "O0001"
        )

        self.assertEqual(
            self.product1.quantity_available,
            7
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_product = (
            loaded_manager.get_product(
                "P0001"
            )
        )

        self.assertEqual(
            loaded_product.quantity_available,
            7
        )

    # --------------------------------------------------
    # OBJECT RELATIONSHIPS
    # --------------------------------------------------

    def test_loaded_order_uses_loaded_client(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_client = (
            loaded_manager.get_client(
                "C0001"
            )
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertIs(
            loaded_order.client,
            loaded_client
        )

    def test_loaded_order_line_uses_loaded_product(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            1
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        loaded_product = (
            loaded_manager.get_product(
                "P0001"
            )
        )

        loaded_order = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        self.assertIs(
            loaded_order.lines[0].product,
            loaded_product
        )

    # --------------------------------------------------
    # COMPLETE ROUND TRIP
    # --------------------------------------------------

    def test_complete_round_trip(self):
        self.manager.add_client(
            self.client1
        )

        self.manager.add_client(
            self.client2
        )

        self.manager.add_product(
            self.product1
        )

        self.manager.add_product(
            self.product2
        )

        order1 = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            2
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0002",
            1
        )

        self.manager.confirm_order(
            "O0001"
        )

        order2 = self.manager.create_order(
            "O0002",
            "C0002"
        )

        self.manager.add_product_to_order(
            "O0002",
            "P0002",
            4
        )

        self.database.save(
            self.manager
        )

        loaded_manager = (
            self.database.load()
        )

        self.assertEqual(
            len(loaded_manager.get_clients()),
            2
        )

        self.assertEqual(
            len(loaded_manager.get_products()),
            2
        )

        self.assertEqual(
            len(loaded_manager.get_orders()),
            2
        )

        loaded_order1 = (
            loaded_manager.get_order(
                "O0001"
            )
        )

        loaded_order2 = (
            loaded_manager.get_order(
                "O0002"
            )
        )

        self.assertEqual(
            loaded_order1.status,
            OrderStatus.CONFIRMED
        )

        self.assertEqual(
            loaded_order2.status,
            OrderStatus.DRAFT
        )

        self.assertEqual(
            len(loaded_order1),
            2
        )

        self.assertEqual(
            len(loaded_order2),
            1
        )

    # --------------------------------------------------
    # SAVE OVERWRITES PREVIOUS STATE
    # --------------------------------------------------

    def test_second_save_replaces_previous_database_state(self):
        self.manager.add_client(
            self.client1
        )

        self.database.save(
            self.manager
        )

        second_manager = (
            OrderFlowManager()
        )

        second_manager.add_client(
            self.client2
        )

        self.database.save(
            second_manager
        )

        loaded_manager = (
            self.database.load()
        )

        clients = (
            loaded_manager.get_clients()
        )

        self.assertEqual(
            len(clients),
            1
        )

        self.assertEqual(
            clients[0],
            self.client2
        )

    # --------------------------------------------------
    # INVALID SAVE
    # --------------------------------------------------

    def test_save_invalid_manager_type(self):
        with self.assertRaises(TypeError):
            self.database.save(
                "not a manager"
            )


if __name__ == "__main__":
    unittest.main()
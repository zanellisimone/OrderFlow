import unittest

from model import Client, Product, OrderStatus
from services import OrderFlowManager

from exceptions import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
    ClientHasOrdersError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductHasOrdersError,
    OrderAlreadyExistsError,
    OrderNotFoundError,
    InsufficientStockError,
    EmptyOrderError,
    OrderCantBeConfirmedError,
    OrderCantBeShippedError,
    OrderCantBeCancelledError,
    OrderNotModificableError
)


class TestOrderFlowManager(unittest.TestCase):

    def setUp(self):
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

        self.product3 = Product(
            id_product="P0003",
            name="Monitor",
            category="Displays",
            price=249.90,
            quantity_available=2
        )

    # --------------------------------------------------
    # CLIENTS
    # --------------------------------------------------

    def test_add_client(self):
        self.manager.add_client(self.client1)

        self.assertEqual(
            self.manager.get_client("C0001"),
            self.client1
        )

    def test_add_invalid_client_type(self):
        with self.assertRaises(TypeError):
            self.manager.add_client("not a client")

    def test_add_duplicate_client(self):
        self.manager.add_client(self.client1)

        duplicate = Client(
            id_client="C0001",
            name="Other",
            surname="Person",
            email="other@example.com"
        )

        with self.assertRaises(ClientAlreadyExistsError):
            self.manager.add_client(duplicate)

    def test_get_client_normalizes_id(self):
        self.manager.add_client(self.client1)

        client = self.manager.get_client(" c0001 ")

        self.assertEqual(client, self.client1)

    def test_get_client_invalid_id_type(self):
        with self.assertRaises(TypeError):
            self.manager.get_client(1)

    def test_get_client_not_found(self):
        with self.assertRaises(ClientNotFoundError):
            self.manager.get_client("C9999")

    def test_get_clients_empty(self):
        self.assertEqual(
            self.manager.get_clients(),
            ()
        )

    def test_get_clients(self):
        self.manager.add_client(self.client1)
        self.manager.add_client(self.client2)

        clients = self.manager.get_clients()

        self.assertEqual(len(clients), 2)
        self.assertIn(self.client1, clients)
        self.assertIn(self.client2, clients)

    def test_get_clients_returns_tuple(self):
        self.assertIsInstance(
            self.manager.get_clients(),
            tuple
        )

    def test_remove_client(self):
        self.manager.add_client(self.client1)

        self.manager.remove_client("C0001")

        with self.assertRaises(ClientNotFoundError):
            self.manager.get_client("C0001")

    def test_remove_client_not_found(self):
        with self.assertRaises(ClientNotFoundError):
            self.manager.remove_client("C9999")

    def test_remove_client_with_orders(self):
        self.manager.add_client(self.client1)
        self.manager.create_order("O0001", "C0001")

        with self.assertRaises(ClientHasOrdersError):
            self.manager.remove_client("C0001")

    # --------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------

    def test_add_product(self):
        self.manager.add_product(self.product1)

        self.assertEqual(
            self.manager.get_product("P0001"),
            self.product1
        )

    def test_add_invalid_product_type(self):
        with self.assertRaises(TypeError):
            self.manager.add_product("not a product")

    def test_add_duplicate_product(self):
        self.manager.add_product(self.product1)

        duplicate = Product(
            id_product="P0001",
            name="Other Product",
            category="Other",
            price=10,
            quantity_available=1
        )

        with self.assertRaises(ProductAlreadyExistsError):
            self.manager.add_product(duplicate)

    def test_get_product_normalizes_id(self):
        self.manager.add_product(self.product1)

        product = self.manager.get_product(" p0001 ")

        self.assertEqual(product, self.product1)

    def test_get_product_invalid_id_type(self):
        with self.assertRaises(TypeError):
            self.manager.get_product(1)

    def test_get_product_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            self.manager.get_product("P9999")

    def test_get_products_empty(self):
        self.assertEqual(
            self.manager.get_products(),
            ()
        )

    def test_get_products(self):
        self.manager.add_product(self.product1)
        self.manager.add_product(self.product2)

        products = self.manager.get_products()

        self.assertEqual(len(products), 2)
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)

    def test_get_products_returns_tuple(self):
        self.assertIsInstance(
            self.manager.get_products(),
            tuple
        )

    def test_remove_product(self):
        self.manager.add_product(self.product1)

        self.manager.remove_product("P0001")

        with self.assertRaises(ProductNotFoundError):
            self.manager.get_product("P0001")

    def test_remove_product_not_found(self):
        with self.assertRaises(ProductNotFoundError):
            self.manager.remove_product("P9999")

    def test_remove_product_used_in_order(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            1
        )

        with self.assertRaises(ProductHasOrdersError):
            self.manager.remove_product("P0001")

        self.assertTrue(order.has_product(self.product1))

    # --------------------------------------------------
    # ORDERS
    # --------------------------------------------------

    def test_create_order(self):
        self.manager.add_client(self.client1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.assertEqual(order.id_order, "O0001")
        self.assertEqual(order.client, self.client1)
        self.assertEqual(order.status, OrderStatus.DRAFT)

    def test_create_order_normalizes_id(self):
        self.manager.add_client(self.client1)

        order = self.manager.create_order(
            " o0001 ",
            "C0001"
        )

        self.assertEqual(order.id_order, "O0001")

    def test_create_order_invalid_order_id_type(self):
        self.manager.add_client(self.client1)

        with self.assertRaises(TypeError):
            self.manager.create_order(
                1,
                "C0001"
            )

    def test_create_order_with_missing_client(self):
        with self.assertRaises(ClientNotFoundError):
            self.manager.create_order(
                "O0001",
                "C9999"
            )

    def test_create_duplicate_order(self):
        self.manager.add_client(self.client1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        with self.assertRaises(OrderAlreadyExistsError):
            self.manager.create_order(
                "O0001",
                "C0001"
            )

    def test_get_order(self):
        self.manager.add_client(self.client1)

        created = self.manager.create_order(
            "O0001",
            "C0001"
        )

        retrieved = self.manager.get_order("O0001")

        self.assertIs(retrieved, created)

    def test_get_order_normalizes_id(self):
        self.manager.add_client(self.client1)
        self.manager.create_order("O0001", "C0001")

        order = self.manager.get_order(" o0001 ")

        self.assertEqual(order.id_order, "O0001")

    def test_get_order_invalid_id_type(self):
        with self.assertRaises(TypeError):
            self.manager.get_order(1)

    def test_get_order_not_found(self):
        with self.assertRaises(OrderNotFoundError):
            self.manager.get_order("O9999")

    def test_get_orders_empty(self):
        self.assertEqual(
            self.manager.get_orders(),
            ()
        )

    def test_get_orders(self):
        self.manager.add_client(self.client1)
        self.manager.add_client(self.client2)

        order1 = self.manager.create_order(
            "O0001",
            "C0001"
        )

        order2 = self.manager.create_order(
            "O0002",
            "C0002"
        )

        orders = self.manager.get_orders()

        self.assertEqual(len(orders), 2)
        self.assertIn(order1, orders)
        self.assertIn(order2, orders)

    def test_get_orders_returns_tuple(self):
        self.assertIsInstance(
            self.manager.get_orders(),
            tuple
        )

    # --------------------------------------------------
    # ADD PRODUCT TO ORDER
    # --------------------------------------------------

    def test_add_product_to_order(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)
        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            2
        )

        self.assertEqual(len(order), 1)
        self.assertEqual(order.lines[0].product, self.product1)
        self.assertEqual(order.lines[0].quantity, 2)

    def test_add_same_product_to_order_updates_quantity(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
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
            "P0001",
            3
        )

        self.assertEqual(len(order), 1)
        self.assertEqual(order.lines[0].quantity, 5)

    def test_add_product_to_missing_order(self):
        self.manager.add_product(self.product1)

        with self.assertRaises(OrderNotFoundError):
            self.manager.add_product_to_order(
                "O9999",
                "P0001",
                1
            )

    def test_add_missing_product_to_order(self):
        self.manager.add_client(self.client1)
        self.manager.create_order(
            "O0001",
            "C0001"
        )

        with self.assertRaises(ProductNotFoundError):
            self.manager.add_product_to_order(
                "O0001",
                "P9999",
                1
            )

    def test_add_product_to_confirmed_order(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            1
        )

        self.manager.confirm_order("O0001")

        with self.assertRaises(OrderNotModificableError):
            self.manager.add_product_to_order(
                "O0001",
                "P0001",
                1
            )

    # --------------------------------------------------
    # CONFIRM ORDER / STOCK
    # --------------------------------------------------

    def test_confirm_order(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order("O0001")

        self.assertEqual(
            order.status,
            OrderStatus.CONFIRMED
        )

    def test_confirm_order_decreases_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            7
        )

    def test_confirm_order_decreases_all_products_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)
        self.manager.add_product(self.product2)

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
            4
        )

        self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            8
        )

        self.assertEqual(
            self.product2.quantity_available,
            16
        )

    def test_confirm_order_with_insufficient_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product3)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0003",
            3
        )

        with self.assertRaises(InsufficientStockError):
            self.manager.confirm_order("O0001")

        self.assertEqual(
            order.status,
            OrderStatus.DRAFT
        )

        self.assertEqual(
            self.product3.quantity_available,
            2
        )

    def test_failed_confirmation_does_not_modify_other_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)
        self.manager.add_product(self.product3)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            5
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0003",
            3
        )

        with self.assertRaises(InsufficientStockError):
            self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            10
        )

        self.assertEqual(
            self.product3.quantity_available,
            2
        )

        self.assertEqual(
            order.status,
            OrderStatus.DRAFT
        )

    def test_empty_order_cannot_be_confirmed(self):
        self.manager.add_client(self.client1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        with self.assertRaises(EmptyOrderError):
            self.manager.confirm_order("O0001")

    def test_double_confirmation_does_not_decrease_stock_twice(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            7
        )

        with self.assertRaises(OrderCantBeConfirmedError):
            self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            7
        )

    # --------------------------------------------------
    # SHIP ORDER
    # --------------------------------------------------

    def test_ship_confirmed_order(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            1
        )

        self.manager.confirm_order("O0001")
        self.manager.ship_order("O0001")

        self.assertEqual(
            order.status,
            OrderStatus.SHIPPED
        )

    def test_ship_draft_order(self):
        self.manager.add_client(self.client1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        with self.assertRaises(OrderCantBeShippedError):
            self.manager.ship_order("O0001")

    # --------------------------------------------------
    # CANCEL ORDER
    # --------------------------------------------------

    def test_cancel_draft_order_does_not_change_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.cancel_order("O0001")

        self.assertEqual(
            order.status,
            OrderStatus.CANCELLED
        )

        self.assertEqual(
            self.product1.quantity_available,
            10
        )

    def test_cancel_confirmed_order_restores_stock(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            7
        )

        self.manager.cancel_order("O0001")

        self.assertEqual(
            order.status,
            OrderStatus.CANCELLED
        )

        self.assertEqual(
            self.product1.quantity_available,
            10
        )

    def test_cancel_confirmed_order_restores_all_products(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)
        self.manager.add_product(self.product2)

        order = self.manager.create_order(
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
            5
        )

        self.manager.confirm_order("O0001")
        self.manager.cancel_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            10
        )

        self.assertEqual(
            self.product2.quantity_available,
            20
        )

        self.assertEqual(
            order.status,
            OrderStatus.CANCELLED
        )

    def test_shipped_order_cannot_be_cancelled_and_stock_is_unchanged(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0001",
            "P0001",
            3
        )

        self.manager.confirm_order("O0001")
        self.manager.ship_order("O0001")

        stock_before = self.product1.quantity_available

        with self.assertRaises(OrderCantBeCancelledError):
            self.manager.cancel_order("O0001")

        self.assertEqual(
            self.product1.quantity_available,
            stock_before
        )

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    def test_get_orders_by_client(self):
        self.manager.add_client(self.client1)
        self.manager.add_client(self.client2)

        order1 = self.manager.create_order(
            "O0001",
            "C0001"
        )

        order2 = self.manager.create_order(
            "O0002",
            "C0001"
        )

        self.manager.create_order(
            "O0003",
            "C0002"
        )

        orders = self.manager.get_orders_by_client(
            "C0001"
        )

        self.assertEqual(len(orders), 2)
        self.assertIn(order1, orders)
        self.assertIn(order2, orders)

    def test_get_orders_by_client_with_no_orders(self):
        self.manager.add_client(self.client1)

        self.assertEqual(
            self.manager.get_orders_by_client("C0001"),
            ()
        )

    def test_get_orders_by_missing_client(self):
        with self.assertRaises(ClientNotFoundError):
            self.manager.get_orders_by_client("C9999")

    def test_get_orders_by_status(self):
        self.manager.add_client(self.client1)
        self.manager.add_product(self.product1)

        draft_order = self.manager.create_order(
            "O0001",
            "C0001"
        )

        confirmed_order = self.manager.create_order(
            "O0002",
            "C0001"
        )

        self.manager.add_product_to_order(
            "O0002",
            "P0001",
            1
        )

        self.manager.confirm_order("O0002")

        draft_orders = self.manager.get_orders_by_status(
            OrderStatus.DRAFT
        )

        confirmed_orders = self.manager.get_orders_by_status(
            OrderStatus.CONFIRMED
        )

        self.assertEqual(
            draft_orders,
            (draft_order,)
        )

        self.assertEqual(
            confirmed_orders,
            (confirmed_order,)
        )

    def test_get_orders_by_status_with_no_results(self):
        self.manager.add_client(self.client1)

        self.manager.create_order(
            "O0001",
            "C0001"
        )

        self.assertEqual(
            self.manager.get_orders_by_status(
                OrderStatus.SHIPPED
            ),
            ()
        )

    def test_get_orders_by_invalid_status_type(self):
        with self.assertRaises(TypeError):
            self.manager.get_orders_by_status(
                "CONFIRMED"
            )


if __name__ == "__main__":
    unittest.main()
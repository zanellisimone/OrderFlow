import unittest
from datetime import datetime

from model import (
    Client,
    Product,
    OrderLine,
    Order,
    OrderStatus
)

from exceptions import (
    OrderNotModificableError,
    ProductNotFoundError,
    OrderCantBeConfirmedError,
    OrderCantBeShippedError,
    OrderCantBeCancelledError,
    EmptyOrderError
)


class TestOrder(unittest.TestCase):

    def setUp(self):
        self.client = Client(
            id_client="C0001",
            name="Mario",
            surname="Rossi",
            email="mario.rossi@example.com",
            phone="+393331234567"
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

        self.order = Order(
            id_order="O0001",
            client=self.client
        )

    # --------------------------------------------------
    # CREATION
    # --------------------------------------------------

    def test_order_creation(self):
        self.assertEqual(self.order.id_order, "O0001")
        self.assertEqual(self.order.client, self.client)
        self.assertEqual(self.order.status, OrderStatus.DRAFT)
        self.assertEqual(len(self.order), 0)

    def test_creation_date_is_datetime(self):
        self.assertIsInstance(
            self.order.creation_date,
            datetime
        )

    def test_creation_date_is_set_automatically(self):
        before = datetime.today()

        order = Order(
            id_order="O0002",
            client=self.client
        )

        after = datetime.today()

        self.assertGreaterEqual(
            order.creation_date,
            before
        )

        self.assertLessEqual(
            order.creation_date,
            after
        )

    def test_invalid_client_type(self):
        with self.assertRaises(TypeError):
            Order(
                id_order="O0002",
                client="not a client"
            )

    def test_client_property_has_no_setter(self):
        other_client = Client(
            id_client="C0002",
            name="Anna",
            surname="Bianchi",
            email="anna.bianchi@example.com"
        )

        with self.assertRaises(AttributeError):
            self.order.client = other_client

    def test_creation_date_property_has_no_setter(self):
        with self.assertRaises(AttributeError):
            self.order.creation_date = datetime.today()

    def test_status_property_has_no_setter(self):
        with self.assertRaises(AttributeError):
            self.order.status = OrderStatus.CONFIRMED

    def test_order_id_cannot_be_modified(self):
        with self.assertRaises(AttributeError):
            self.order.id_order = "O9999"

    # --------------------------------------------------
    # LINES PROPERTY
    # --------------------------------------------------

    def test_lines_is_tuple(self):
        self.assertIsInstance(
            self.order.lines,
            tuple
        )

    def test_lines_cannot_be_modified_directly(self):
        self.assertFalse(
            hasattr(self.order.lines, "append")
        )

    # --------------------------------------------------
    # LEN / ITER / CONTAINS
    # --------------------------------------------------

    def test_len_empty_order(self):
        self.assertEqual(
            len(self.order),
            0
        )

    def test_len_after_adding_product(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.assertEqual(
            len(self.order),
            1
        )

    def test_order_is_iterable(self):
        self.order.add_product(
            self.product1,
            2
        )

        lines = list(self.order)

        self.assertEqual(len(lines), 1)
        self.assertIsInstance(
            lines[0],
            OrderLine
        )

    def test_order_contains_order_line(self):
        self.order.add_product(
            self.product1,
            2
        )

        line = self.order.lines[0]

        self.assertIn(
            line,
            self.order
        )

    def test_order_does_not_contain_different_line(self):
        self.order.add_product(
            self.product1,
            2
        )

        different_line = OrderLine(
            self.product2,
            1
        )

        self.assertNotIn(
            different_line,
            self.order
        )

    def test_contains_invalid_type_returns_false(self):
        self.assertFalse(
            "invalid" in self.order
        )

    # --------------------------------------------------
    # ADD PRODUCT
    # --------------------------------------------------

    def test_add_product(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.assertEqual(
            len(self.order),
            1
        )

        line = self.order.lines[0]

        self.assertEqual(
            line.product,
            self.product1
        )

        self.assertEqual(
            line.quantity,
            2
        )

    def test_add_second_product(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.order.add_product(
            self.product2,
            3
        )

        self.assertEqual(
            len(self.order),
            2
        )

    def test_add_existing_product_updates_quantity(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.order.add_product(
            self.product1,
            3
        )

        self.assertEqual(
            len(self.order),
            1
        )

        self.assertEqual(
            self.order.lines[0].quantity,
            5
        )

    def test_add_product_preserves_initial_unit_price(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.product1.price = 99.90

        line = self.order.lines[0]

        self.assertEqual(
            line.unit_price,
            79.90
        )

    def test_add_invalid_product_type(self):
        with self.assertRaises(TypeError):
            self.order.add_product(
                "not a product",
                2
            )

    def test_add_product_with_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_product(
                self.product1,
                0
            )

    def test_add_product_with_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_product(
                self.product1,
                -1
            )

    def test_add_product_with_float_quantity(self):
        with self.assertRaises(TypeError):
            self.order.add_product(
                self.product1,
                2.5
            )

    def test_add_product_with_boolean_quantity(self):
        with self.assertRaises(TypeError):
            self.order.add_product(
                self.product1,
                True
            )

    # --------------------------------------------------
    # REMOVE PRODUCT
    # --------------------------------------------------

    def test_remove_product(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.order.remove_product(
            self.product1
        )

        self.assertEqual(
            len(self.order),
            0
        )

    def test_remove_one_product_preserves_other_lines(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.order.add_product(
            self.product2,
            1
        )

        self.order.remove_product(
            self.product1
        )

        self.assertEqual(
            len(self.order),
            1
        )

        self.assertEqual(
            self.order.lines[0].product,
            self.product2
        )

    def test_remove_product_not_in_order(self):
        with self.assertRaises(
            ProductNotFoundError
        ):
            self.order.remove_product(
                self.product1
            )

    def test_remove_invalid_product_type(self):
        with self.assertRaises(TypeError):
            self.order.remove_product(
                "not a product"
            )

    # --------------------------------------------------
    # CALCULATE TOTAL
    # --------------------------------------------------

    def test_empty_order_total_is_zero(self):
        self.assertEqual(
            self.order.calculate_total(),
            0
        )

    def test_calculate_total_with_one_line(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.assertAlmostEqual(
            self.order.calculate_total(),
            159.80
        )

    def test_calculate_total_with_multiple_lines(self):
        self.order.add_product(
            self.product1,
            2
        )

        self.order.add_product(
            self.product2,
            3
        )

        expected_total = (
            79.90 * 2
            + 29.90 * 3
        )

        self.assertAlmostEqual(
            self.order.calculate_total(),
            expected_total
        )

    # --------------------------------------------------
    # CONFIRM
    # --------------------------------------------------

    def test_confirm_order(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()

        self.assertEqual(
            self.order.status,
            OrderStatus.CONFIRMED
        )

    def test_empty_order_cannot_be_confirmed(self):
        with self.assertRaises(
            EmptyOrderError
        ):
            self.order.confirm()

    def test_confirmed_order_cannot_be_confirmed_again(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()

        with self.assertRaises(
            OrderCantBeConfirmedError
        ):
            self.order.confirm()

    # --------------------------------------------------
    # SHIP
    # --------------------------------------------------

    def test_ship_confirmed_order(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()
        self.order.ship()

        self.assertEqual(
            self.order.status,
            OrderStatus.SHIPPED
        )

    def test_draft_order_cannot_be_shipped(self):
        with self.assertRaises(
            OrderCantBeShippedError
        ):
            self.order.ship()

    def test_cancelled_order_cannot_be_shipped(self):
        self.order.cancel()

        with self.assertRaises(
            OrderCantBeShippedError
        ):
            self.order.ship()

    def test_shipped_order_cannot_be_shipped_again(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()
        self.order.ship()

        with self.assertRaises(
            OrderCantBeShippedError
        ):
            self.order.ship()

    # --------------------------------------------------
    # CANCEL
    # --------------------------------------------------

    def test_cancel_draft_order(self):
        self.order.cancel()

        self.assertEqual(
            self.order.status,
            OrderStatus.CANCELLED
        )

    def test_cancel_confirmed_order(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()
        self.order.cancel()

        self.assertEqual(
            self.order.status,
            OrderStatus.CANCELLED
        )

    def test_shipped_order_cannot_be_cancelled(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()
        self.order.ship()

        with self.assertRaises(
            OrderCantBeCancelledError
        ):
            self.order.cancel()

    def test_cancelled_order_cannot_be_cancelled_again(self):
        self.order.cancel()

        with self.assertRaises(
            OrderCantBeCancelledError
        ):
            self.order.cancel()

    # --------------------------------------------------
    # MODIFICATION AFTER STATE CHANGE
    # --------------------------------------------------

    def test_confirmed_order_cannot_add_products(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()

        with self.assertRaises(
            OrderNotModificableError
        ):
            self.order.add_product(
                self.product2,
                1
            )

    def test_confirmed_order_cannot_remove_products(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()

        with self.assertRaises(
            OrderNotModificableError
        ):
            self.order.remove_product(
                self.product1
            )

    def test_cancelled_order_cannot_add_products(self):
        self.order.cancel()

        with self.assertRaises(
            OrderNotModificableError
        ):
            self.order.add_product(
                self.product1,
                1
            )

    def test_cancelled_order_cannot_remove_products(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.cancel()

        with self.assertRaises(
            OrderNotModificableError
        ):
            self.order.remove_product(
                self.product1
            )

    def test_shipped_order_cannot_add_products(self):
        self.order.add_product(
            self.product1,
            1
        )

        self.order.confirm()
        self.order.ship()

        with self.assertRaises(
            OrderNotModificableError
        ):
            self.order.add_product(
                self.product2,
                1
            )

    # --------------------------------------------------
    # EQUALITY
    # --------------------------------------------------

    def test_orders_with_same_id_are_equal(self):
        other_order = Order(
            id_order="O0001",
            client=self.client
        )

        self.assertEqual(
            self.order,
            other_order
        )

    def test_orders_with_different_ids_are_not_equal(self):
        other_order = Order(
            id_order="O0002",
            client=self.client
        )

        self.assertNotEqual(
            self.order,
            other_order
        )

    # --------------------------------------------------
    # REPR / STR
    # --------------------------------------------------

    def test_repr_contains_order_data(self):
        representation = repr(
            self.order
        )

        self.assertIn(
            "O0001",
            representation
        )

        self.assertIn(
            "C0001",
            representation
        )

        self.assertIn(
            "DRAFT",
            representation
        )

    def test_str_contains_order_data(self):
        representation = str(
            self.order
        )

        self.assertIn(
            "O0001",
            representation
        )

        self.assertIn(
            "C0001",
            representation
        )

        self.assertIn(
            "DRAFT",
            representation
        )


if __name__ == "__main__":
    unittest.main()
import unittest

from model import Product, OrderLine


class TestOrderLine(unittest.TestCase):

    def setUp(self):
        self.product = Product(
            id_product="P0001",
            name="Mechanical Keyboard",
            category="Peripherals",
            price=79.90,
            quantity_available=10
        )

        self.order_line = OrderLine(
            product=self.product,
            quantity=2
        )

    def test_order_line_creation(self):
        self.assertEqual(self.order_line.product, self.product)
        self.assertEqual(self.order_line.quantity, 2)
        self.assertEqual(self.order_line.unit_price, 79.90)

    def test_unit_price_is_copied_from_product(self):
        self.product.price = 99.90

        self.assertEqual(self.order_line.unit_price, 79.90)

    def test_invalid_product_type(self):
        with self.assertRaises(TypeError):
            OrderLine(
                product="not a product",
                quantity=2
            )

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            OrderLine(
                product=self.product,
                quantity=0
            )

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            OrderLine(
                product=self.product,
                quantity=-1
            )

    def test_float_quantity(self):
        with self.assertRaises(TypeError):
            OrderLine(
                product=self.product,
                quantity=2.5
            )

    def test_boolean_quantity(self):
        with self.assertRaises(TypeError):
            OrderLine(
                product=self.product,
                quantity=True
            )

    def test_valid_quantity_update(self):
        self.order_line.quantity = 5

        self.assertEqual(self.order_line.quantity, 5)

    def test_invalid_quantity_update(self):
        with self.assertRaises(ValueError):
            self.order_line.quantity = 0

    def test_valid_unit_price_update(self):
        self.order_line.unit_price = 89.90

        self.assertEqual(self.order_line.unit_price, 89.90)

    def test_invalid_unit_price_update_zero(self):
        with self.assertRaises(ValueError):
            self.order_line.unit_price = 0

    def test_invalid_unit_price_update_negative(self):
        with self.assertRaises(ValueError):
            self.order_line.unit_price = -10

    def test_invalid_unit_price_update_boolean(self):
        with self.assertRaises(TypeError):
            self.order_line.unit_price = True

    def test_calculate_subtotal(self):
        subtotal = self.order_line.calculate_subtotal()

        self.assertAlmostEqual(subtotal, 159.80)

    def test_calculate_subtotal_after_quantity_update(self):
        self.order_line.quantity = 3

        subtotal = self.order_line.calculate_subtotal()

        self.assertAlmostEqual(subtotal, 239.70)

    def test_equal_order_lines(self):
        other_line = OrderLine(
            product=self.product,
            quantity=5
        )

        self.assertEqual(self.order_line, other_line)

    def test_order_lines_with_different_products_are_not_equal(self):
        other_product = Product(
            id_product="P0002",
            name="Mouse",
            category="Peripherals",
            price=79.90,
            quantity_available=10
        )

        other_line = OrderLine(
            product=other_product,
            quantity=2
        )

        self.assertNotEqual(self.order_line, other_line)

    def test_order_lines_with_different_unit_price_are_not_equal(self):
        other_line = OrderLine(
            product=self.product,
            quantity=2
        )

        other_line.unit_price = 89.90

        self.assertNotEqual(self.order_line, other_line)

    def test_product_property(self):
        self.assertIs(self.order_line.product, self.product)

    def test_product_property_has_no_setter(self):
        other_product = Product(
            id_product="P0002",
            name="Mouse",
            category="Peripherals",
            price=29.90,
            quantity_available=5
        )

        with self.assertRaises(AttributeError):
            self.order_line.product = other_product

    def test_repr_contains_order_line_data(self):
        representation = repr(self.order_line)

        self.assertIn("P0001", representation)
        self.assertIn("2", representation)
        self.assertIn("79.9", representation)

    def test_str_contains_order_line_data(self):
        representation = str(self.order_line)

        self.assertIn("Mechanical Keyboard", representation)
        self.assertIn("2", representation)
        self.assertIn("79.90", representation)


if __name__ == "__main__":
    unittest.main()
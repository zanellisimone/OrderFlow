import unittest

from model.product import Product


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.product = Product(
            id_product="P0001",
            name="Mechanical Keyboard",
            category="Peripherals",
            price=79.90,
            quantity_available=12
        )

    def test_product_creation(self):
        self.assertEqual(self.product.id_product, "P0001")
        self.assertEqual(self.product.name, "Mechanical Keyboard")
        self.assertEqual(self.product.category, "Peripherals")
        self.assertEqual(self.product.price, 79.90)
        self.assertEqual(self.product.quantity_available, 12)

    def test_product_values_are_normalized(self):
        product = Product(
            id_product=" p0002 ",
            name=" Mouse ",
            category=" Peripherals ",
            price=29.90,
            quantity_available=5
        )

        self.assertEqual(product.id_product, "P0002")
        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.category, "Peripherals")

    def test_invalid_product_id(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="C0001",
                name="Mouse",
                category="Peripherals",
                price=29.90,
                quantity_available=5
            )

    def test_non_string_product_id(self):
        with self.assertRaises(TypeError):
            Product(
                id_product=1,
                name="Mouse",
                category="Peripherals",
                price=29.90,
                quantity_available=5
            )

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="",
                category="Peripherals",
                price=29.90,
                quantity_available=5
            )

    def test_name_with_spaces_only(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="   ",
                category="Peripherals",
                price=29.90,
                quantity_available=5
            )

    def test_empty_category(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="",
                price=29.90,
                quantity_available=5
            )

    def test_category_with_spaces_only(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="   ",
                price=29.90,
                quantity_available=5
            )

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=0,
                quantity_available=5
            )

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=-10,
                quantity_available=5
            )

    def test_non_numeric_price(self):
        with self.assertRaises(TypeError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price="29.90",
                quantity_available=5
            )

    def test_boolean_price(self):
        with self.assertRaises(TypeError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=True,
                quantity_available=5
            )

    def test_zero_quantity_is_valid(self):
        product = Product(
            id_product="P0002",
            name="Mouse",
            category="Peripherals",
            price=29.90,
            quantity_available=0
        )

        self.assertEqual(product.quantity_available, 0)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=29.90,
                quantity_available=-1
            )

    def test_float_quantity(self):
        with self.assertRaises(TypeError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=29.90,
                quantity_available=2.5
            )

    def test_boolean_quantity(self):
        with self.assertRaises(TypeError):
            Product(
                id_product="P0002",
                name="Mouse",
                category="Peripherals",
                price=29.90,
                quantity_available=True
            )

    def test_valid_name_update(self):
        self.product.name = "Gaming Keyboard"

        self.assertEqual(self.product.name, "Gaming Keyboard")

    def test_invalid_name_update(self):
        with self.assertRaises(ValueError):
            self.product.name = ""

    def test_valid_category_update(self):
        self.product.category = "Gaming"

        self.assertEqual(self.product.category, "Gaming")

    def test_valid_price_update(self):
        self.product.price = 89.90

        self.assertEqual(self.product.price, 89.90)

    def test_invalid_price_update(self):
        with self.assertRaises(ValueError):
            self.product.price = 0

    def test_valid_quantity_update(self):
        self.product.quantity_available = 20

        self.assertEqual(self.product.quantity_available, 20)

    def test_invalid_quantity_update(self):
        with self.assertRaises(ValueError):
            self.product.quantity_available = -1

    def test_product_id_cannot_be_modified(self):
        with self.assertRaises(AttributeError):
            self.product.id_product = "P9999"

    def test_products_with_same_id_are_equal(self):
        other_product = Product(
            id_product="P0001",
            name="Different Product",
            category="Different Category",
            price=10,
            quantity_available=1
        )

        self.assertEqual(self.product, other_product)

    def test_products_with_different_ids_are_not_equal(self):
        other_product = Product(
            id_product="P0002",
            name="Mechanical Keyboard",
            category="Peripherals",
            price=79.90,
            quantity_available=12
        )

        self.assertNotEqual(self.product, other_product)

    def test_equal_products_have_same_hash(self):
        other_product = Product(
            id_product="P0001",
            name="Different Product",
            category="Other",
            price=10,
            quantity_available=1
        )

        self.assertEqual(hash(self.product), hash(other_product))

    def test_product_can_be_used_in_set(self):
        same_product = Product(
            id_product="P0001",
            name="Another Name",
            category="Other",
            price=15,
            quantity_available=2
        )

        products = {self.product, same_product}

        self.assertEqual(len(products), 1)

    def test_repr_contains_product_data(self):
        representation = repr(self.product)

        self.assertIn("P0001", representation)
        self.assertIn("Mechanical Keyboard", representation)
        self.assertIn("Peripherals", representation)

    def test_str_contains_product_data(self):
        representation = str(self.product)

        self.assertIn("P0001", representation)
        self.assertIn("Mechanical Keyboard", representation)
        self.assertIn("Peripherals", representation)
        self.assertIn("79.9", representation)
        self.assertIn("12", representation)


if __name__ == "__main__":
    unittest.main()
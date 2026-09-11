import unittest

from descriptors import ProductID, PositiveNumber, NonNegativeInteger


class TestClass:
    id_product = ProductID()
    price = PositiveNumber()
    quantity_available = NonNegativeInteger()


class TestProductID(unittest.TestCase):

    def test_valid_product_id(self):
        obj = TestClass()
        obj.id_product = "P0001"

        self.assertEqual(obj.id_product, "P0001")

    def test_lowercase_product_id_is_normalized(self):
        obj = TestClass()
        obj.id_product = "p0001"

        self.assertEqual(obj.id_product, "P0001")

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.id_product = "  P0001  "

        self.assertEqual(obj.id_product, "P0001")

    def test_non_string_product_id(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.id_product = 1

    def test_product_id_too_short(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_product = "P001"

    def test_product_id_too_long(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_product = "P00001"

    def test_product_id_without_p_prefix(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_product = "C0001"

    def test_product_id_with_letters_in_numeric_part(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_product = "P00A1"

    def test_product_id_with_only_digits(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_product = "00001"

    def test_product_id_cannot_be_modified(self):
        obj = TestClass()
        obj.id_product = "P0001"

        with self.assertRaises(AttributeError):
            obj.id_product = "P0002"

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.id_product, ProductID)


class TestPositiveNumber(unittest.TestCase):

    def test_valid_integer(self):
        obj = TestClass()
        obj.price = 10

        self.assertEqual(obj.price, 10)

    def test_valid_float(self):
        obj = TestClass()
        obj.price = 19.99

        self.assertEqual(obj.price, 19.99)

    def test_small_positive_float(self):
        obj = TestClass()
        obj.price = 0.01

        self.assertEqual(obj.price, 0.01)

    def test_zero_value(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.price = 0

    def test_negative_integer(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.price = -10

    def test_negative_float(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.price = -0.5

    def test_string_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.price = "19.99"

    def test_boolean_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.price = True

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.price, PositiveNumber)


class TestNonNegativeInteger(unittest.TestCase):

    def test_positive_integer(self):
        obj = TestClass()
        obj.quantity_available = 10

        self.assertEqual(obj.quantity_available, 10)

    def test_zero_is_valid(self):
        obj = TestClass()
        obj.quantity_available = 0

        self.assertEqual(obj.quantity_available, 0)

    def test_negative_integer(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.quantity_available = -1

    def test_float_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.quantity_available = 5.5

    def test_string_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.quantity_available = "10"

    def test_boolean_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.quantity_available = True

    def test_none_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.quantity_available = None

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(
            TestClass.quantity_available,
            NonNegativeInteger
        )


if __name__ == "__main__":
    unittest.main()
import unittest

from descriptors import OrderID


class TestClass:
    id_order = OrderID()


class TestOrderID(unittest.TestCase):

    def test_valid_order_id(self):
        obj = TestClass()
        obj.id_order = "O0001"

        self.assertEqual(obj.id_order, "O0001")

    def test_lowercase_order_id_is_normalized(self):
        obj = TestClass()
        obj.id_order = "o0001"

        self.assertEqual(obj.id_order, "O0001")

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.id_order = "  O0001  "

        self.assertEqual(obj.id_order, "O0001")

    def test_non_string_order_id(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.id_order = 1

    def test_order_id_too_short(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_order = "O001"

    def test_order_id_too_long(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_order = "O00001"

    def test_order_id_without_o_prefix(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_order = "P0001"

    def test_order_id_with_letters_in_numeric_part(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_order = "O00A1"

    def test_order_id_with_only_digits(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.id_order = "00001"

    def test_order_id_cannot_be_modified(self):
        obj = TestClass()
        obj.id_order = "O0001"

        with self.assertRaises(AttributeError):
            obj.id_order = "O0002"

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.id_order, OrderID)


if __name__ == "__main__":
    unittest.main()
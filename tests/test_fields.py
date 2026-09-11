import unittest

from descriptors import (
    ClientID,
    StringNotEmpty,
    ValidEmail,
    ValidPhoneNumber
)


class TestClass:
    client_id = ClientID()
    name = StringNotEmpty()
    email = ValidEmail()
    phone = ValidPhoneNumber()


class TestClientID(unittest.TestCase):

    def test_valid_client_id(self):
        obj = TestClass()
        obj.client_id = "C0001"

        self.assertEqual(obj.client_id, "C0001")

    def test_lowercase_client_id_is_normalized(self):
        obj = TestClass()
        obj.client_id = "c0001"

        self.assertEqual(obj.client_id, "C0001")

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.client_id = "  C0001  "

        self.assertEqual(obj.client_id, "C0001")

    def test_non_string_client_id(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.client_id = 1

    def test_client_id_too_short(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.client_id = "C001"

    def test_client_id_too_long(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.client_id = "C00001"

    def test_client_id_without_c_prefix(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.client_id = "A0001"

    def test_client_id_with_letters_in_numeric_part(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.client_id = "C00A1"

    def test_client_id_with_only_digits(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.client_id = "00001"

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.client_id, ClientID)


class TestStringNotEmpty(unittest.TestCase):

    def test_valid_string(self):
        obj = TestClass()
        obj.name = "Mario"

        self.assertEqual(obj.name, "Mario")

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.name = "  Mario  "

        self.assertEqual(obj.name, "Mario")

    def test_empty_string(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.name = ""

    def test_string_with_spaces_only(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.name = "   "

    def test_non_string_value(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.name = 123

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.name, StringNotEmpty)


class TestValidEmail(unittest.TestCase):

    def test_valid_email(self):
        obj = TestClass()
        obj.email = "mario.rossi@gmail.com"

        self.assertEqual(obj.email, "mario.rossi@gmail.com")

    def test_valid_email_with_plus_symbol(self):
        obj = TestClass()
        obj.email = "mario+orders@gmail.com"

        self.assertEqual(obj.email, "mario+orders@gmail.com")

    def test_valid_email_with_subdomain(self):
        obj = TestClass()
        obj.email = "mario@mail.company.it"

        self.assertEqual(obj.email, "mario@mail.company.it")

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.email = "  mario.rossi@gmail.com  "

        self.assertEqual(obj.email, "mario.rossi@gmail.com")

    def test_empty_email(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = ""

    def test_email_with_spaces_only(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = "   "

    def test_email_without_at_symbol(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = "mario.rossi.gmail.com"

    def test_email_without_local_part(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = "@gmail.com"

    def test_email_without_domain(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = "mario@"

    def test_email_without_extension(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.email = "mario@gmail"

    def test_non_string_email(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.email = 123

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.email, ValidEmail)


class TestValidPhoneNumber(unittest.TestCase):

    def test_valid_phone_number(self):
        obj = TestClass()
        obj.phone = "3331234567"

        self.assertEqual(obj.phone, "3331234567")

    def test_valid_phone_number_with_prefix(self):
        obj = TestClass()
        obj.phone = "+393331234567"

        self.assertEqual(obj.phone, "+393331234567")

    def test_none_phone_number(self):
        obj = TestClass()
        obj.phone = None

        self.assertIsNone(obj.phone)

    def test_outer_spaces_are_removed(self):
        obj = TestClass()
        obj.phone = " 3331234567 "

        self.assertEqual(obj.phone, "3331234567")

    def test_internal_spaces_are_removed(self):
        obj = TestClass()
        obj.phone = "+39 333 1234567"

        self.assertEqual(obj.phone, "+393331234567")

    def test_phone_number_too_short(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.phone = "1234567"

    def test_phone_number_too_long(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.phone = "1234567890123456"

    def test_phone_number_with_letters(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.phone = "333ABC4567"

    def test_plus_symbol_inside_phone_number(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.phone = "333+1234567"

    def test_multiple_plus_symbols(self):
        obj = TestClass()

        with self.assertRaises(ValueError):
            obj.phone = "++393331234567"

    def test_non_string_phone_number(self):
        obj = TestClass()

        with self.assertRaises(TypeError):
            obj.phone = 3331234567

    def test_descriptor_access_from_class(self):
        self.assertIsInstance(TestClass.phone, ValidPhoneNumber)


if __name__ == "__main__":
    unittest.main()
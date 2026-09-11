import unittest
from model.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(
            id_client="C0001",
            surname="Rossi",
            name="Mario",
            email="mario.rossi@gmail.com",
            phone="+393331234567"
        )

    def test_client_creation(self):
        self.assertEqual(self.client.id_client, "C0001")
        self.assertEqual(self.client.name, "Mario")
        self.assertEqual(self.client.surname, "Rossi")
        self.assertEqual(self.client.email, "mario.rossi@gmail.com")
        self.assertEqual(self.client.phone, "+393331234567")

    def test_client_without_phone(self):
        client = Client(
            id_client="C0002",
            surname="Bianchi",
            name="Anna",
            email="anna.bianchi@gmail.com"
        )

        self.assertIsNone(client.phone)

    def test_client_values_are_normalized(self):
        client = Client(
            id_client=" c0003 ",
            surname=" Rossi ",
            name=" Mario ",
            email=" mario.rossi@gmail.com ",
            phone="+39 333 1234567"
        )

        self.assertEqual(client.id_client, "C0003")
        self.assertEqual(client.name, "Mario")
        self.assertEqual(client.surname, "Rossi")
        self.assertEqual(client.email, "mario.rossi@gmail.com")
        self.assertEqual(client.phone, "+393331234567")

    def test_invalid_client_id(self):
        with self.assertRaises(ValueError):
            Client(
                id_client="A0001",
                surname="Rossi",
                name="Mario",
                email="mario.rossi@gmail.com"
            )

    def test_non_string_client_id(self):
        with self.assertRaises(TypeError):
            Client(
                id_client=1,
                surname="Rossi",
                name="Mario",
                email="mario.rossi@gmail.com"
            )

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Client(
                id_client="C0002",
                surname="Rossi",
                name="",
                email="mario.rossi@gmail.com"
            )

    def test_empty_surname(self):
        with self.assertRaises(ValueError):
            Client(
                id_client="C0002",
                surname="",
                name="Mario",
                email="mario.rossi@gmail.com"
            )

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            Client(
                id_client="C0002",
                surname="Rossi",
                name="Mario",
                email="invalid-email"
            )

    def test_invalid_phone_number(self):
        with self.assertRaises(ValueError):
            Client(
                id_client="C0002",
                surname="Rossi",
                name="Mario",
                email="mario.rossi@gmail.com",
                phone="ABC123"
            )

    def test_valid_name_update(self):
        self.client.name = "Luigi"

        self.assertEqual(self.client.name, "Luigi")

    def test_invalid_name_update(self):
        with self.assertRaises(ValueError):
            self.client.name = ""

    def test_valid_surname_update(self):
        self.client.surname = "Bianchi"

        self.assertEqual(self.client.surname, "Bianchi")

    def test_invalid_surname_update(self):
        with self.assertRaises(ValueError):
            self.client.surname = "   "

    def test_valid_email_update(self):
        self.client.email = "new.email@example.com"

        self.assertEqual(
            self.client.email,
            "new.email@example.com"
        )

    def test_invalid_email_update(self):
        with self.assertRaises(ValueError):
            self.client.email = "invalid"

    def test_valid_phone_update(self):
        self.client.phone = "+39 340 1234567"

        self.assertEqual(
            self.client.phone,
            "+393401234567"
        )

    def test_phone_update_to_none(self):
        self.client.phone = None

        self.assertIsNone(self.client.phone)

    def test_invalid_phone_update(self):
        with self.assertRaises(ValueError):
            self.client.phone = "phone"

    def test_client_id_cannot_be_modified(self):
        with self.assertRaises(AttributeError):
            self.client.id_client = "C9999"

    def test_equal_clients_have_same_hash(self):
        client2 = Client(
            id_client="C0001",
            name="Other",
            surname="Person",
            email="other@example.com"
        )
        self.assertEqual(self.client, client2)
        self.assertEqual(hash(self.client), hash(client2))


if __name__ == "__main__":
    unittest.main()
from __future__ import annotations
from descriptors import ClientID, StringNotEmpty, ValidEmail, ValidPhoneNumber

class Client:

    id_client = ClientID()
    name = StringNotEmpty()
    surname = StringNotEmpty()
    email = ValidEmail()
    phone = ValidPhoneNumber()

    def __init__(self, id_client:str, surname:str, name:str, email:str, phone:str | None = None) -> None:            
        self.id_client = id_client
        self.surname = surname
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self) -> str:
        return f"Client(id_client={self.id_client!r}, surname={self.surname!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"

    def __str__(self) -> str:
        response = ""
        response += f"ID: {self.id_client}\n"
        response += f"Surname: {self.surname}\n"
        response += f"Name: {self.name}\n"
        response += f"Email: {self.email}\n"
        response += f"Phone: {self.phone}"
        return response

    def __eq__(self, other_object:object) -> bool:
        if not isinstance(other_object, Client):
            return NotImplemented
        return other_object.id_client == self.id_client

    def __hash__(self) -> int:
        return hash(self.id_client)
import tkinter as tk

from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Client
from services import OrderFlowManager


class ClientForm(tk.Toplevel):

    def __init__(self, parent, manager: OrderFlowManager, on_success: Callable[[], None], client: Client | None = None) -> None:
        super().__init__(parent)

        if not isinstance(manager, OrderFlowManager):
            raise TypeError("manager must be an instance of OrderFlowManager!")

        if client is not None and not isinstance(client, Client):
            raise TypeError("client must be an instance of Client or None!")

        self.__manager = manager
        self.__client: Client | None = client
        self.__on_success = on_success

        self.title("Add Client" if client is None else "Edit Client")
        self.resizable(False, False)

        self.__create_variables()
        self.__create_widgets()

        if self.__client is not None:
            self.__fill_fields()

        self.transient(parent)
        self.grab_set()

    def __create_variables(self) -> None:
        self.__id_var = tk.StringVar()
        self.__name_var = tk.StringVar()
        self.__surname_var = tk.StringVar()
        self.__email_var = tk.StringVar()
        self.__phone_var = tk.StringVar()

    def __create_widgets(self) -> None:
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        labels = ("ID", "Name", "Surname", "Email", "Phone")
        variables = (self.__id_var, self.__name_var, self.__surname_var, self.__email_var, self.__phone_var)

        self.__entries = []

        for row, (label_text, variable) in enumerate(zip(labels, variables)):
            label = ttk.Label(container, text=label_text)
            label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)

            entry = ttk.Entry(container, textvariable=variable, width=35)
            entry.grid(row=row, column=1, sticky="ew", pady=5)

            self.__entries.append(entry)

        buttons_frame = ttk.Frame(container)
        buttons_frame.grid(row=5, column=0, columnspan=2, sticky="e", pady=(15, 0))

        save_button = ttk.Button(buttons_frame, text="Save", command=self.__save)
        save_button.pack(side="left", padx=5)

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side="left", padx=5)

    def __fill_fields(self) -> None:
        client = self.__client

        if client is None:
            return

        self.__id_var.set(client.id_client)
        self.__name_var.set(client.name)
        self.__surname_var.set(client.surname)
        self.__email_var.set(client.email)
        self.__phone_var.set(client.phone or "")

        self.__entries[0].state(["disabled"])

    def __save(self) -> None:
        id_client = self.__id_var.get().strip()
        name = self.__name_var.get().strip()
        surname = self.__surname_var.get().strip()
        email = self.__email_var.get().strip()
        phone = self.__phone_var.get().strip()

        if phone == "":
            phone = None

        try:
            if self.__client is None:
                new_client = Client(id_client=id_client, surname=surname, name=name, email=email, phone=phone)
                self.__manager.add_client(new_client)
            else:
                self.__client.name = name
                self.__client.surname = surname
                self.__client.email = email
                self.__client.phone = phone

            self.__on_success()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        self.destroy()
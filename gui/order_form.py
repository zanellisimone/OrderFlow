import tkinter as tk

from tkinter import ttk, messagebox
from collections.abc import Callable
from services import OrderFlowManager


class OrderForm(tk.Toplevel):

    def __init__(self, parent, manager: OrderFlowManager, on_success: Callable[[], None]) -> None:
        super().__init__(parent)

        self.__manager = manager
        self.__on_success = on_success

        self.title("Create Order")
        self.resizable(False, False)

        self.__id_var = tk.StringVar()
        self.__client_var = tk.StringVar()

        self.__create_widgets()

        self.transient(parent)
        self.grab_set()

    def __create_widgets(self) -> None:
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0)

        ttk.Label(container, text="Order ID").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(container, textvariable=self.__id_var, width=35).grid(row=0, column=1, pady=5)

        ttk.Label(container, text="Client").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)

        clients = [f"{client.id_client} - {client.name} {client.surname}" for client in self.__manager.get_clients()]

        self.__client_combo = ttk.Combobox(container, textvariable=self.__client_var, values=clients, state="readonly", width=32)
        self.__client_combo.grid(row=1, column=1, pady=5)

        if clients:
            self.__client_combo.current(0)

        buttons_frame = ttk.Frame(container)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(15, 0))

        ttk.Button(buttons_frame, text="Create", command=self.__create_order).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def __create_order(self) -> None:
        try:
            id_order = self.__id_var.get().strip()
            client_value = self.__client_var.get()

            if client_value == "":
                raise ValueError("A client must be selected!")

            id_client = client_value.split(" - ", 1)[0]

            self.__manager.create_order(id_order, id_client)
            self.__on_success()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        self.destroy()
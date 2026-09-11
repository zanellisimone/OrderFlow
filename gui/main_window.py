import tkinter as tk

from tkinter import ttk, messagebox
from services import OrderFlowManager
from database import DatabaseManager
from .clients_view import ClientsView
from .products_view import ProductsView
from .orders_view import OrdersView

class MainWindow(tk.Tk):

    def __init__(self, manager: OrderFlowManager, database_manager: DatabaseManager) -> None:
        super().__init__()

        if not isinstance(manager, OrderFlowManager):
            raise TypeError("manager must be an instance of OrderFlowManager!")

        if not isinstance(database_manager, DatabaseManager):
            raise TypeError("database_manager must be an instance of DatabaseManager!")

        self.__manager = manager
        self.__database_manager = database_manager

        self.title("OrderFlow")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.__configure_layout()
        self.__create_sidebar()
        self.__create_main_content()
        self.__show_clients_view()

        self.protocol("WM_DELETE_WINDOW", self.__close)

    def __configure_layout(self) -> None:
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def __create_sidebar(self) -> None:
        self.__sidebar = ttk.Frame(self, padding=15)
        self.__sidebar.grid(row=0, column=0, sticky="ns")

        title_label = ttk.Label(self.__sidebar, text="OrderFlow", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 30))

        clients_button = ttk.Button(self.__sidebar, text="Clients", command=self.__show_clients_view)
        clients_button.pack(fill="x", pady=5)

        products_button = ttk.Button(self.__sidebar, text="Products", command=self.__show_products_view)
        products_button.pack(fill="x", pady=5)

        orders_button = ttk.Button(self.__sidebar, text="Orders", command=self.__show_orders_view)
        orders_button.pack(fill="x", pady=5)

        exit_button = ttk.Button(self.__sidebar, text="Exit", command=self.__close)
        exit_button.pack(side="bottom", fill="x", pady=5)

    def __create_main_content(self) -> None:
        self.__main_content = ttk.Frame(self, padding=20)
        self.__main_content.grid(row=0, column=1, sticky="nsew")
        self.__main_content.columnconfigure(0, weight=1)
        self.__main_content.rowconfigure(0, weight=1)

    def __clear_main_content(self) -> None:
        for widget in self.__main_content.winfo_children():
            widget.destroy()

    def __show_clients_view(self) -> None:
        self.__clear_main_content()
        view = ClientsView(self.__main_content, self.__manager, self.__save_data)
        view.grid(row=0, column=0, sticky="nsew")

    def __show_products_view(self) -> None:
        self.__clear_main_content()
        view = ProductsView(self.__main_content, self.__manager, self.__save_data)
        view.grid(row=0, column=0, sticky="nsew")

    def __show_orders_view(self) -> None:
        self.__clear_main_content()
        view = OrdersView(self.__main_content, self.__manager, self.__save_data)
        view.grid(row=0, column=0, sticky="nsew")

    def __save_data(self) -> None:
        try:
            self.__database_manager.save(self.__manager)
        except Exception as error:
            messagebox.showerror("Database error", str(error), parent=self)

    def __close(self) -> None:
        try:
            self.__database_manager.save(self.__manager)
        except Exception as error:
            messagebox.showerror("Database error", str(error), parent=self)
            return

        self.destroy()
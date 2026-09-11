import tkinter as tk

from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Product
from services import OrderFlowManager


class ProductForm(tk.Toplevel):

    def __init__(self, parent, manager: OrderFlowManager, on_success: Callable[[], None], product: Product | None = None) -> None:
        super().__init__(parent)

        self.__manager = manager
        self.__product: Product | None = product
        self.__on_success = on_success

        self.title("Add Product" if product is None else "Edit Product")
        self.resizable(False, False)

        self.__create_variables()
        self.__create_widgets()

        if self.__product is not None:
            self.__fill_fields()

        self.transient(parent)
        self.grab_set()

    def __create_variables(self) -> None:
        self.__id_var = tk.StringVar()
        self.__name_var = tk.StringVar()
        self.__category_var = tk.StringVar()
        self.__price_var = tk.StringVar()
        self.__quantity_var = tk.StringVar()

    def __create_widgets(self) -> None:
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0)

        labels = ("ID", "Name", "Category", "Price", "Quantity")
        variables = (self.__id_var, self.__name_var, self.__category_var, self.__price_var, self.__quantity_var)

        self.__entries = []

        for row, (label_text, variable) in enumerate(zip(labels, variables)):
            ttk.Label(container, text=label_text).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=5)

            entry = ttk.Entry(container, textvariable=variable, width=35)
            entry.grid(row=row, column=1, pady=5)

            self.__entries.append(entry)

        buttons_frame = ttk.Frame(container)
        buttons_frame.grid(row=5, column=0, columnspan=2, sticky="e", pady=(15, 0))

        ttk.Button(buttons_frame, text="Save", command=self.__save).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def __fill_fields(self) -> None:
        product = self.__product

        if product is None:
            return

        self.__id_var.set(product.id_product)
        self.__name_var.set(product.name)
        self.__category_var.set(product.category)
        self.__price_var.set(str(product.price))
        self.__quantity_var.set(str(product.quantity_available))

        self.__entries[0].state(["disabled"])

    def __save(self) -> None:
        id_product = self.__id_var.get().strip()
        name = self.__name_var.get().strip()
        category = self.__category_var.get().strip()

        try:
            price = float(self.__price_var.get().strip())
            quantity = int(self.__quantity_var.get().strip())

            if self.__product is None:
                new_product = Product(id_product, name, category, price, quantity)
                self.__manager.add_product(new_product)
            else:
                self.__product.name = name
                self.__product.category = category
                self.__product.price = price
                self.__product.quantity_available = quantity

            self.__on_success()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        self.destroy()
import tkinter as tk

from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Order
from services import OrderFlowManager


class OrderDetails(tk.Toplevel):

    def __init__(self, parent, manager: OrderFlowManager, order: Order, on_change: Callable[[], None]) -> None:
        super().__init__(parent)

        self.__manager = manager
        self.__order = order
        self.__on_change = on_change

        self.title(f"Order {order.id_order}")
        self.geometry("750x500")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.__create_header()
        self.__create_actions()
        self.__create_treeview()
        self.__refresh()

        self.transient(parent)

    def __create_header(self) -> None:
        self.__header = ttk.Label(self, font=("Arial", 14, "bold"))
        self.__header.grid(row=0, column=0, sticky="w", padx=15, pady=15)

    def __create_actions(self) -> None:
        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))

        ttk.Button(actions_frame, text="Add Product", command=self.__add_product).pack(side="left", padx=(0, 5))
        ttk.Button(actions_frame, text="Remove Product", command=self.__remove_product).pack(side="left", padx=5)

    def __create_treeview(self) -> None:
        columns = ("product", "name", "quantity", "price", "subtotal")

        self.__treeview = ttk.Treeview(self, columns=columns, show="headings")

        self.__treeview.heading("product", text="Product")
        self.__treeview.heading("name", text="Name")
        self.__treeview.heading("quantity", text="Quantity")
        self.__treeview.heading("price", text="Unit Price")
        self.__treeview.heading("subtotal", text="Subtotal")

        self.__treeview.column("product", width=90, anchor="center")
        self.__treeview.column("name", width=200)
        self.__treeview.column("quantity", width=90, anchor="center")
        self.__treeview.column("price", width=100, anchor="e")
        self.__treeview.column("subtotal", width=100, anchor="e")

        self.__treeview.grid(row=2, column=0, sticky="nsew", padx=15)

        self.__total_label = ttk.Label(self, font=("Arial", 12, "bold"))
        self.__total_label.grid(row=3, column=0, sticky="e", padx=15, pady=15)

    def __refresh(self) -> None:
        self.__header.config(text=f"Client: {self.__order.client.name} {self.__order.client.surname} | Status: {self.__order.status.name}")

        for item in self.__treeview.get_children():
            self.__treeview.delete(item)

        for line in self.__order.lines:
            self.__treeview.insert("", "end", values=(line.product.id_product, line.product.name, line.quantity, f"{line.unit_price:.2f}", f"{line.calculate_subtotal():.2f}"))

        self.__total_label.config(text=f"Total: € {self.__order.calculate_total():.2f}")

    def __add_product(self) -> None:
        AddProductToOrderForm(self, self.__manager, self.__order, self.__order_changed)

    def __remove_product(self) -> None:
        selected = self.__treeview.selection()

        if not selected:
            messagebox.showwarning("No selection", "Select a product first.", parent=self)
            return

        values = self.__treeview.item(selected[0], "values")

        try:
            product = self.__manager.get_product(values[0])
            self.__order.remove_product(product)
            self.__order_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __order_changed(self) -> None:
        self.__refresh()
        self.__on_change()


class AddProductToOrderForm(tk.Toplevel):

    def __init__(self, parent, manager: OrderFlowManager, order: Order, on_success: Callable[[], None]) -> None:
        super().__init__(parent)

        self.__manager = manager
        self.__order = order
        self.__on_success = on_success

        self.title("Add Product")
        self.resizable(False, False)

        self.__product_var = tk.StringVar()
        self.__quantity_var = tk.StringVar(value="1")

        self.__create_widgets()

        self.transient(parent)
        self.grab_set()

    def __create_widgets(self) -> None:
        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0)

        ttk.Label(container, text="Product").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)

        products = [f"{product.id_product} - {product.name}" for product in self.__manager.get_products()]

        product_combo = ttk.Combobox(container, textvariable=self.__product_var, values=products, state="readonly", width=35)
        product_combo.grid(row=0, column=1, pady=5)

        if products:
            product_combo.current(0)

        ttk.Label(container, text="Quantity").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        ttk.Entry(container, textvariable=self.__quantity_var, width=38).grid(row=1, column=1, pady=5)

        buttons_frame = ttk.Frame(container)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(15, 0))

        ttk.Button(buttons_frame, text="Add", command=self.__add).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

    def __add(self) -> None:
        try:
            product_value = self.__product_var.get()

            if product_value == "":
                raise ValueError("A product must be selected!")

            id_product = product_value.split(" - ", 1)[0]
            quantity = int(self.__quantity_var.get().strip())

            self.__manager.add_product_to_order(self.__order.id_order, id_product, quantity)
            self.__on_success()

        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)
            return

        self.destroy()
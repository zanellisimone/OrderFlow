from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Product
from services import OrderFlowManager
from .product_form import ProductForm


class ProductsView(ttk.Frame):

    def __init__(self, parent, manager: OrderFlowManager, on_change: Callable[[], None]) -> None:
        super().__init__(parent)

        self.__manager = manager
        self.__on_change = on_change

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.__create_title()
        self.__create_actions()
        self.__create_treeview()
        self.__refresh_treeview()

    def __create_title(self) -> None:
        ttk.Label(self, text="Products", font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 15))

    def __create_actions(self) -> None:
        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        ttk.Button(actions_frame, text="Add Product", command=self.__add_product).pack(side="left", padx=(0, 5))
        ttk.Button(actions_frame, text="Edit Product", command=self.__edit_product).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Delete Product", command=self.__delete_product).pack(side="left", padx=5)

    def __create_treeview(self) -> None:
        columns = ("id", "name", "category", "price", "quantity")

        self.__treeview = ttk.Treeview(self, columns=columns, show="headings")

        self.__treeview.heading("id", text="ID")
        self.__treeview.heading("name", text="Name")
        self.__treeview.heading("category", text="Category")
        self.__treeview.heading("price", text="Price")
        self.__treeview.heading("quantity", text="Quantity")

        self.__treeview.column("id", width=80, anchor="center")
        self.__treeview.column("name", width=200)
        self.__treeview.column("category", width=160)
        self.__treeview.column("price", width=100, anchor="e")
        self.__treeview.column("quantity", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.__treeview.yview)
        self.__treeview.configure(yscrollcommand=scrollbar.set)

        self.__treeview.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.__treeview.bind("<Double-1>", lambda event: self.__edit_product())

    def __refresh_treeview(self) -> None:
        for item in self.__treeview.get_children():
            self.__treeview.delete(item)

        for product in self.__manager.get_products():
            self.__treeview.insert("", "end", values=(product.id_product, product.name, product.category, f"{product.price:.2f}", product.quantity_available))

    def __get_selected_product(self) -> Product | None:
        selected = self.__treeview.selection()

        if not selected:
            messagebox.showwarning("No selection", "Select a product first.", parent=self)
            return None

        values = self.__treeview.item(selected[0], "values")
        return self.__manager.get_product(values[0])

    def __add_product(self) -> None:
        ProductForm(self, self.__manager, self.__product_changed)

    def __edit_product(self) -> None:
        product = self.__get_selected_product()

        if product is None:
            return

        ProductForm(self, self.__manager, self.__product_changed, product)

    def __delete_product(self) -> None:
        product = self.__get_selected_product()

        if product is None:
            return

        confirmed = messagebox.askyesno("Delete Product", f"Are you sure you want to delete {product.name}?", parent=self)

        if not confirmed:
            return

        try:
            self.__manager.remove_product(product.id_product)
            self.__product_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __product_changed(self) -> None:
        self.__refresh_treeview()
        self.__on_change()
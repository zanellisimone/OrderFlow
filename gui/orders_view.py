from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Order
from services import OrderFlowManager
from .order_form import OrderForm
from .order_details import OrderDetails


class OrdersView(ttk.Frame):

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
        ttk.Label(self, text="Orders", font=("Arial", 20, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 15))

    def __create_actions(self) -> None:
        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        ttk.Button(actions_frame, text="Create Order", command=self.__create_order).pack(side="left", padx=(0, 5))
        ttk.Button(actions_frame, text="Details", command=self.__show_details).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Confirm", command=self.__confirm_order).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Ship", command=self.__ship_order).pack(side="left", padx=5)
        ttk.Button(actions_frame, text="Cancel", command=self.__cancel_order).pack(side="left", padx=5)

    def __create_treeview(self) -> None:
        columns = ("id", "client", "date", "status", "total")

        self.__treeview = ttk.Treeview(self, columns=columns, show="headings")

        self.__treeview.heading("id", text="ID")
        self.__treeview.heading("client", text="Client")
        self.__treeview.heading("date", text="Creation Date")
        self.__treeview.heading("status", text="Status")
        self.__treeview.heading("total", text="Total")

        self.__treeview.column("id", width=80, anchor="center")
        self.__treeview.column("client", width=220)
        self.__treeview.column("date", width=130, anchor="center")
        self.__treeview.column("status", width=110, anchor="center")
        self.__treeview.column("total", width=110, anchor="e")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.__treeview.yview)
        self.__treeview.configure(yscrollcommand=scrollbar.set)

        self.__treeview.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.__treeview.bind("<Double-1>", lambda event: self.__show_details())

    def __refresh_treeview(self) -> None:
        for item in self.__treeview.get_children():
            self.__treeview.delete(item)

        for order in self.__manager.get_orders():
            client_name = f"{order.client.name} {order.client.surname}"
            creation_date = order.creation_date.strftime("%d/%m/%Y")
            total = f"€ {order.calculate_total():.2f}"

            self.__treeview.insert("", "end", values=(order.id_order, client_name, creation_date, order.status.name, total))

    def __get_selected_order(self) -> Order | None:
        selected = self.__treeview.selection()

        if not selected:
            messagebox.showwarning("No selection", "Select an order first.", parent=self)
            return None

        values = self.__treeview.item(selected[0], "values")
        return self.__manager.get_order(values[0])

    def __create_order(self) -> None:
        OrderForm(self, self.__manager, self.__order_changed)

    def __show_details(self) -> None:
        order = self.__get_selected_order()

        if order is None:
            return

        OrderDetails(self, self.__manager, order, self.__order_changed)

    def __confirm_order(self) -> None:
        order = self.__get_selected_order()

        if order is None:
            return

        try:
            self.__manager.confirm_order(order.id_order)
            self.__order_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __ship_order(self) -> None:
        order = self.__get_selected_order()

        if order is None:
            return

        try:
            self.__manager.ship_order(order.id_order)
            self.__order_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __cancel_order(self) -> None:
        order = self.__get_selected_order()

        if order is None:
            return

        confirmed = messagebox.askyesno("Cancel Order", f"Are you sure you want to cancel order {order.id_order}?", parent=self)

        if not confirmed:
            return

        try:
            self.__manager.cancel_order(order.id_order)
            self.__order_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __order_changed(self) -> None:
        self.__refresh_treeview()
        self.__on_change()
from tkinter import ttk, messagebox
from collections.abc import Callable
from model import Client
from services import OrderFlowManager
from .client_form import ClientForm


class ClientsView(ttk.Frame):

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
        title_label = ttk.Label(self, text="Clients", font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 15))

    def __create_actions(self) -> None:
        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        add_button = ttk.Button(actions_frame, text="Add Client", command=self.__add_client)
        add_button.pack(side="left", padx=(0, 5))

        edit_button = ttk.Button(actions_frame, text="Edit Client", command=self.__edit_client)
        edit_button.pack(side="left", padx=5)

        delete_button = ttk.Button(actions_frame, text="Delete Client", command=self.__delete_client)
        delete_button.pack(side="left", padx=5)

    def __create_treeview(self) -> None:
        columns = ("id", "name", "surname", "email", "phone")

        self.__treeview = ttk.Treeview(self, columns=columns, show="headings")

        self.__treeview.heading("id", text="ID")
        self.__treeview.heading("name", text="Name")
        self.__treeview.heading("surname", text="Surname")
        self.__treeview.heading("email", text="Email")
        self.__treeview.heading("phone", text="Phone")

        self.__treeview.column("id", width=80, anchor="center")
        self.__treeview.column("name", width=140)
        self.__treeview.column("surname", width=140)
        self.__treeview.column("email", width=220)
        self.__treeview.column("phone", width=140)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.__treeview.yview)
        self.__treeview.configure(yscrollcommand=scrollbar.set)

        self.__treeview.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.__treeview.bind("<Double-1>", lambda event: self.__edit_client())

    def __refresh_treeview(self) -> None:
        for item in self.__treeview.get_children():
            self.__treeview.delete(item)

        for client in self.__manager.get_clients():
            self.__treeview.insert("", "end", values=(client.id_client, client.name, client.surname, client.email, client.phone or ""))

    def __get_selected_client(self) -> Client | None:
        selected = self.__treeview.selection()

        if not selected:
            messagebox.showwarning("No selection", "Select a client first.", parent=self)
            return None

        values = self.__treeview.item(selected[0], "values")
        return self.__manager.get_client(values[0])

    def __add_client(self) -> None:
        ClientForm(self, self.__manager, self.__client_changed)

    def __edit_client(self) -> None:
        client = self.__get_selected_client()

        if client is None:
            return

        ClientForm(self, self.__manager, self.__client_changed, client)

    def __delete_client(self) -> None:
        client = self.__get_selected_client()

        if client is None:
            return

        confirmed = messagebox.askyesno("Delete Client", f"Are you sure you want to delete {client.name} {client.surname}?", parent=self)

        if not confirmed:
            return

        try:
            self.__manager.remove_client(client.id_client)
            self.__client_changed()
        except Exception as error:
            messagebox.showerror("Error", str(error), parent=self)

    def __client_changed(self) -> None:
        self.__refresh_treeview()
        self.__on_change()
# OrderFlow

OrderFlow is a desktop order and inventory management application built with **Python**, **Tkinter/ttk**, and **SQLite**.

The project was developed as an end-to-end application to demonstrate object-oriented design, validation, persistence, automated testing, and a clear separation of responsibilities between the graphical interface, business logic, domain model, and database layer.

## Features

### Client management
- Create, edit, view, and delete clients
- Validation of client IDs, names, email addresses, and phone numbers
- Protection against deleting clients associated with existing orders

### Product and inventory management
- Create, edit, view, and delete products
- Product ID, price, and stock validation
- Inventory tracking
- Protection against deleting products already referenced by orders

### Order management
- Create orders for registered clients
- Add and remove products from draft orders
- Automatically calculate order totals
- Preserve the historical unit price of each order line
- Manage the complete order lifecycle:
  - `DRAFT`
  - `CONFIRMED`
  - `SHIPPED`
  - `CANCELLED`
- Validate stock before order confirmation
- Decrease stock only after successful confirmation
- Restore stock when a confirmed order is cancelled

### Persistence
- SQLite database with relational integrity and foreign keys
- Complete save/load cycle for clients, products, orders, and order lines
- Preservation of order status, creation date, inventory state, and historical prices
- Transaction-based saving with rollback on database errors

### Desktop GUI
- Tkinter/ttk graphical interface
- Separate views for clients, products, and orders
- Forms for creating and editing entities
- Order detail window with line management
- User-friendly error dialogs and confirmation prompts

## Architecture

```text
OrderFlow/
├── database/
├── descriptors/
├── exceptions/
├── gui/
├── model/
├── services/
├── tests/
├── main.py
├── .gitignore
├── LICENSE
└── README.md
```

The GUI does not access SQLite directly. User actions are delegated to `OrderFlowManager`, while `DatabaseManager` is responsible for persistence.

```text
GUI
 ↓
OrderFlowManager
 ↓
Domain Model
 ↓
DatabaseManager
 ↓
SQLite
```

## Technologies

- Python 3
- Tkinter / ttk
- SQLite (`sqlite3`)
- `unittest`
- Object-oriented programming
- Custom descriptors
- Custom exceptions
- Type hints

The application uses only Python standard-library modules and does not require third-party runtime dependencies.

## Testing

The project currently includes **282 automated tests** covering the domain model, descriptors, service layer, database persistence, validation rules, stock management, order transitions, and save/load round trips.

Run the complete test suite from the project root with:

```bash
python -m unittest discover -s tests -v
```

On Windows:

```bash
py -m unittest discover -s tests -v
```

## Running the application

### 1. Clone the repository

```bash
git clone https://github.com/zanellisimone/OrderFlow.git
cd OrderFlow
```

### 2. Run OrderFlow

```bash
python main.py
```

or on Windows:

```bash
py main.py
```

The SQLite database is created automatically when the application starts. Runtime database files are excluded from version control through `.gitignore`.

## Domain rules

Some of the main rules enforced by the application are:

- IDs follow entity-specific formats (`Cxxxx`, `Pxxxx`, `Oxxxx`).
- An order can be modified only while it is in `DRAFT` state.
- An empty order cannot be confirmed.
- All required stock must be available before confirmation.
- A shipped order cannot be cancelled.
- Cancelling a previously confirmed order restores its stock.
- Order lines retain their original unit price even if the product price changes later.

## What this project demonstrates

OrderFlow demonstrates:

- design of a non-trivial Python desktop application;
- separation of presentation, business, domain, and persistence responsibilities;
- relational database modelling with SQLite;
- defensive input validation;
- state-based business rules;
- transactional persistence;
- automated testing of isolated components and complete persistence workflows.

## Possible future improvements

- Search and filtering in the GUI
- Sorting and pagination for larger datasets
- Dashboard with inventory and order statistics
- Application logging
- Export of orders and reports to CSV/PDF
- Packaging as a standalone desktop executable
- Continuous integration with GitHub Actions

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

## Author

**Simone Zanelli**

GitHub: [@zanellisimone](https://github.com/zanellisimone)

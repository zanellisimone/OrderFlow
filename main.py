from database import DatabaseManager
from gui import MainWindow

def main() -> None:
    database_manager = DatabaseManager(None)
    manager = database_manager.load()
    app = MainWindow(manager, database_manager)
    app.mainloop()

if __name__ == "__main__":
    main()
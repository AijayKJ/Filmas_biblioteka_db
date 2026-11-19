from app.database import izveidot_datubazi
from app.library_app import FilmuBiblioteka


if __name__ == "__main__":
    izveidot_datubazi()
    app = FilmuBiblioteka()
    app.mainloop()

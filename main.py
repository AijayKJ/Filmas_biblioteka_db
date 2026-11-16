
import sqlite3
import tkinter as tk
from tkinter import messagebox

from dizains import build_interface, refresh_content, create_fields


# =====================================================
# DATUBĀZE
# =====================================================

DB_FAILS = "filmu_biblioteka.db"

TABULAS = {
    "movies": [
        "title", "release_year", "genre_id", "director_id",
        "runtime_minutes", "synopsis", "studio_id"
    ],
    "actors": [
        "name", "birthday", "nationality"
    ],
    "directors": [
        "name", "birthday", "nationality"
    ],
    "genres": [
        "name", "description"
    ],
    "studios": [
        "name", "country", "founded_year", "website"
    ],
    "users": [
        "username", "email", "password_hash", "full_name"
    ],
    "watchlist_items": [
        "user_id", "movie_id"
    ],
    "reviews": [
        "user_id", "movie_id", "rating", "body"
    ],
    "movie_cast": [
        "movie_id", "actor_id", "character_name", "billing_order"
    ],
    "movie_awards": [
        "movie_id", "actor_id", "award_name", "category",
        "award_year", "won"
    ]
}

NOSAUKUMI = {
    "movies": "Filmas",
    "actors": "Aktieri",
    "directors": "Režisori",
    "genres": "Žanri",
    "studios": "Studijas",
    "users": "Lietotāji",
    "watchlist_items": "Skatīšanās saraksti",
    "reviews": "Atsauksmes",
    "movie_cast": "Filmu lomas",
    "movie_awards": "Filmu balvas"
}

FK = {
    "genre_id": ("genres", "name"),
    "director_id": ("directors", "name"),
    "studio_id": ("studios", "name"),
    "user_id": ("users", "username"),
    "movie_id": ("movies", "title"),
    "actor_id": ("actors", "name")
}

LAUKU_NOSAUKUMI = {
    "title": "Filmas nosaukums",
    "release_year": "Izdošanas gads",
    "genre_id": "Žanrs",
    "director_id": "Režisors",
    "runtime_minutes": "Ilgums (min)",
    "synopsis": "Apraksts",
    "studio_id": "Studija",
    "name": "Nosaukums",
    "birthday": "Dzimšanas datums",
    "nationality": "Valstiskā piederība",
    "description": "Apraksts",
    "country": "Valsts",
    "founded_year": "Dibināšanas gads",
    "website": "Tīmekļa vietne",
    "username": "Lietotājvārds",
    "email": "E-pasts",
    "password_hash": "Paroles jaucējvērtība",
    "full_name": "Pilns vārds",
    "user_id": "Lietotājs",
    "movie_id": "Filma",
    "actor_id": "Aktieris",
    "rating": "Vērtējums (1–10)",
    "body": "Atsauksmes teksts",
    "character_name": "Tēla vārds",
    "billing_order": "Lomas secība",
    "award_name": "Balvas nosaukums",
    "category": "Kategorija",
    "award_year": "Balvas gads",
    "won": "Balva iegūta (0/1)"
}


def savienot():
    conn = sqlite3.connect(DB_FAILS)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def izveidot_datubazi():

    conn = savienot()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            birthday DATE,
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS actors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            birthday DATE,
            nationality VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS studios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            country VARCHAR(100),
            founded_year INTEGER,
            website VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(150) NOT NULL,
            release_year INTEGER,
            genre_id INTEGER REFERENCES genres(id),
            director_id INTEGER REFERENCES directors(id),
            runtime_minutes INTEGER,
            synopsis TEXT,
            studio_id INTEGER REFERENCES studios(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS watchlist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, movie_id)
        );

        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 10),
            body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, movie_id)
        );

        CREATE TABLE IF NOT EXISTS movie_cast (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            actor_id INTEGER NOT NULL REFERENCES actors(id),
            character_name VARCHAR(100),
            billing_order INTEGER,
            UNIQUE(movie_id, actor_id, character_name)
        );

        CREATE TABLE IF NOT EXISTS movie_awards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL REFERENCES movies(id),
            actor_id INTEGER REFERENCES actors(id),
            award_name VARCHAR(100) NOT NULL,
            category VARCHAR(100),
            award_year INTEGER,
            won BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Vecākas datubāzes pielāgošana jaunajai struktūrai
    movie_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(movies)")
    }

    if "studio_id" not in movie_columns:
        conn.execute(
            "ALTER TABLE movies ADD COLUMN studio_id INTEGER REFERENCES studios(id)"
        )

    # Sākotnējie dati
    if conn.execute("SELECT COUNT(*) FROM genres").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO genres (name, description) VALUES (?, ?)",
            [
                ("Sci-Fi", "Zinātniskā fantastika"),
                ("Drāma", "Nopietni stāsti"),
                ("Action", "Asa sižeta filmas"),
                ("Comedy", "Komēdijas")
            ]
        )

    if conn.execute("SELECT COUNT(*) FROM directors").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO directors
            (name, birthday, nationality)
            VALUES (?, ?, ?)""",
            ("Christopher Nolan", "1970-07-30", "Lielbritānija")
        )

    if conn.execute("SELECT COUNT(*) FROM actors").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO actors
            (name, birthday, nationality)
            VALUES (?, ?, ?)""",
            ("Leonardo DiCaprio", "1974-11-11", "ASV")
        )

    if conn.execute("SELECT COUNT(*) FROM studios").fetchone()[0] == 0:
        conn.execute(
            "INSERT INTO studios (name, country) VALUES (?, ?)",
            ("Warner Bros.", "ASV")
        )

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO users
            (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)""",
            ("janis", "janis@epasts.lv", "parole123", "Jānis Bērziņš")
        )

    if conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0] == 0:
        conn.execute(
            """INSERT INTO movies
            (title, release_year, genre_id, director_id,
             runtime_minutes, synopsis, studio_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                "Inception", 2010, 1, 1,
                148, "Zagļi, kas iezogas sapņos.", 1
            )
        )

    conn.commit()
    conn.close()


# =====================================================
# GALVENĀ PROGRAMMA
# =====================================================

class FilmuBiblioteka(tk.Tk):

    def __init__(self):
        super().__init__()

        self.TABULAS = TABULAS
        self.FK = FK
        self.LAUKE_NOSAUKUMI = LAUKU_NOSAUKUMI
        self.current_table = "movies"
        self.selected_id = None
        self.current_tree = None
        self.entries = {}

        build_interface(self)

    # TABULU PĀRSLĒGŠANA

    def change_table(self, table):
        self.current_table = table
        self.selected_id = None
        create_fields(self)
        refresh_content(self)

    # DATU NOLASĪŠANA

    def get_records(self, table):
        columns = ["id"] + TABULAS[table]

        conn = savienot()

        try:
            records = conn.execute(
                f"SELECT {', '.join(columns)} FROM {table} ORDER BY id DESC"
            ).fetchall()

            return records

        finally:
            conn.close()

    def get_record(self, table, record_id):
        columns = ["id"] + TABULAS[table]

        conn = savienot()

        try:
            return conn.execute(
                f"SELECT {', '.join(columns)} FROM {table} WHERE id = ?",
                (record_id,)
            ).fetchone()

        finally:
            conn.close()

    # SAISTĪTO TABULU VĒRTĪBAS

    def fk_label(self, field, value):

        if value is None:
            return ""

        table, label_column = FK[field]

        conn = savienot()

        try:
            result = conn.execute(
                f"SELECT {label_column} FROM {table} WHERE id = ?",
                (value,)
            ).fetchone()

            if result:
                return f"{value} — {result[0]}"

            return str(value)

        finally:
            conn.close()

    def display_value(self, field, value):

        if field in FK and value is not None:
            return self.fk_label(field, value)

        if field == "won":
            return "Jā" if value else "Nē"

        return "" if value is None else str(value)

    # IZVĒLĒTĀ IERAKSTA DATI

    def select_record(self, record):

        self.selected_id = record[0]

        for field_name, value in zip(
            self.entries,
            record[1:]
        ):

            widget = self.entries[field_name]

            if field_name in FK:
                widget.set(
                    self.fk_label(field_name, value)
                    if value is not None else ""
                )

            else:
                widget.delete(0, "end")

                if value is not None:
                    widget.insert(0, str(value))

    # FORMAS VĒRTĪBAS

    def get_form_values(self):

        values = []

        for field_name, widget in self.entries.items():

            raw = widget.get().strip()

            if field_name in FK:

                if not raw:
                    values.append(None)
                else:
                    try:
                        values.append(int(raw.split(" — ")[0]))
                    except ValueError:
                        raise ValueError(
                            f"Izvēlies derīgu vērtību laukā "
                            f"{LAUKU_NOSAUKUMI[field_name]}."
                        )

            else:
                values.append(raw or None)

        return values

    # FORMAS NOTĪRĪŠANA

    def clear_form(self):

        for widget in self.entries.values():

            if widget.winfo_class() == "TCombobox":
                widget.set("")
            else:
                widget.delete(0, "end")

        self.selected_id = None

        if self.current_tree is not None:
            self.current_tree.selection_remove(
                self.current_tree.selection()
            )

    # PIEVIENOT IERAKSTU

    def add_record(self):

        try:
            values = self.get_form_values()
        except ValueError as error:
            messagebox.showwarning("Pārbaudi ievadi", str(error))
            return

        if not any(value is not None for value in values):
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms aizpildi ievades laukus."
            )
            return

        columns = ", ".join(TABULAS[self.current_table])

        placeholders = ", ".join(
            ["?"] * len(TABULAS[self.current_table])
        )

        sql = (
            f"INSERT INTO {self.current_table} "
            f"({columns}) VALUES ({placeholders})"
        )

        self.execute_sql(sql, values)

    # LABOT IERAKSTU

    def update_record(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms izvēlies ierakstu."
            )
            return

        try:
            values = self.get_form_values()
        except ValueError as error:
            messagebox.showwarning("Pārbaudi ievadi", str(error))
            return

        changes = ", ".join(
            f"{column} = ?"
            for column in TABULAS[self.current_table]
        )

        sql = (
            f"UPDATE {self.current_table} "
            f"SET {changes}, updated_at = CURRENT_TIMESTAMP "
            f"WHERE id = ?"
        )

        # Tabulās bez updated_at izmanto atsevišķu vaicājumu.
        if self.current_table in (
            "watchlist_items", "movie_cast", "movie_awards"
        ):
            sql = (
                f"UPDATE {self.current_table} "
                f"SET {changes} WHERE id = ?"
            )

        self.execute_sql(
            sql,
            values + [self.selected_id]
        )

    # DZĒST IERAKSTU

    def delete_record(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Uzmanību",
                "Vispirms izvēlies ierakstu."
            )
            return

        if not messagebox.askyesno(
            "Dzēst ierakstu",
            f"Vai tiešām dzēst ierakstu ar ID {self.selected_id}?"
        ):
            return

        self.execute_sql(
            f"DELETE FROM {self.current_table} WHERE id = ?",
            [self.selected_id]
        )

    # SQL IZPILDE

    def execute_sql(self, sql, values):

        conn = savienot()

        try:

            conn.execute(sql, values)
            conn.commit()

            self.selected_id = None
            self.clear_form()
            refresh_content(self)

        except sqlite3.IntegrityError as error:

            messagebox.showerror(
                "Datu saistību kļūda",
                "Nevar saglabāt ierakstu.\n\n"
                "Pārbaudi ārējās atslēgas, obligātos laukus "
                "un iespējamos dublikātus.\n\n"
                + str(error)
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Datubāzes kļūda",
                str(error)
            )

        finally:
            conn.close()


# =====================================================
# PROGRAMMAS PALAIŠANA
# =====================================================

if __name__ == "__main__":

    izveidot_datubazi()

    app = FilmuBiblioteka()
    app.mainloop()

# ============================================================
#  FILMU BIBLIOTĒKA
#  Programma ar logu (tkinter), kas glabā datus SQLite datubāzē.
#  5 tabulas: movies, actors, directors, genres, users
# ============================================================

import sqlite3                        # darbs ar datubāzi
import tkinter as tk                  # logs, pogas, teksta lauki
from tkinter import ttk, messagebox   # tabula (Treeview), izvēlne un paziņojumi

DB_FAILS = "filmu_biblioteka.db"


# ------------------------------------------------------------
# 1. DATUBĀZE
# ------------------------------------------------------------

# Katrai tabulai: kolonnas, ko lietotājs aizpilda pats.
# id, created_at un updated_at datubāze aizpilda automātiski.
TABULAS = {
    "movies":    ["title", "release_year", "runtime_minutes", "synopsis",
                  "director_id", "genre_id", "actor_id", "user_id"],
    "actors":    ["name", "birthday", "nationality"],
    "directors": ["name", "birthday", "nationality"],
    "genres":    ["name", "description"],
    "users":     ["username", "email", "password_hash", "full_name"],
}


def savienot():
    """Atver savienojumu ar datubāzi un ieslēdz ārējo atslēgu pārbaudi."""
    conn = sqlite3.connect(DB_FAILS)
    conn.execute("PRAGMA foreign_keys = ON")  # neļaus ierakstīt neeksistējošu ID
    return conn


def izveidot_datubazi():
    """Izveido tabulas (ja to vēl nav) un ieliek dažus piemēra datus."""
    conn = savienot()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS genres (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS directors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        VARCHAR(100) NOT NULL,
            birthday    DATE,
            nationality VARCHAR(50),
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS actors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        VARCHAR(100) NOT NULL,
            birthday    DATE,
            nationality VARCHAR(50),
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      VARCHAR(50)  NOT NULL UNIQUE,
            email         VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            full_name     VARCHAR(100),
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Galvenā tabula. *_id kolonnas ir ārējās atslēgas (FOREIGN KEY),
        -- kas norāda uz ierakstu citā tabulā.
        CREATE TABLE IF NOT EXISTS movies (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            title           VARCHAR(150) NOT NULL,
            release_year    INTEGER,
            runtime_minutes INTEGER,
            synopsis        TEXT,
            director_id     INTEGER REFERENCES directors(id),
            genre_id        INTEGER REFERENCES genres(id),
            actor_id        INTEGER REFERENCES actors(id),
            user_id         INTEGER REFERENCES users(id),
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Piemēra dati, lai programma nav tukša (tikai pirmajā palaišanā)
    if conn.execute("SELECT COUNT(*) FROM genres").fetchone()[0] == 0:
        conn.executescript("""
            INSERT INTO genres (name, description) VALUES
                ('Sci-Fi', 'Zinātniskā fantastika'), ('Drāma', 'Nopietni stāsti');
            INSERT INTO directors (name, birthday, nationality) VALUES
                ('Christopher Nolan', '1970-07-30', 'Lielbritānija');
            INSERT INTO actors (name, birthday, nationality) VALUES
                ('Leonardo DiCaprio', '1974-11-11', 'ASV');
            INSERT INTO users (username, email, password_hash, full_name) VALUES
                ('janis', 'janis@epasts.lv', 'parole123', 'Jānis Bērziņš');
            INSERT INTO movies (title, release_year, runtime_minutes, synopsis,
                                director_id, genre_id, actor_id, user_id) VALUES
                ('Inception', 2010, 148, 'Zagļi, kas iezogas sapņos', 1, 1, 1, 1);
        """)
    conn.commit()
    conn.close()


# ------------------------------------------------------------
# 2. LOGS (tkinter)
# ------------------------------------------------------------

class FilmuBiblioteka(tk.Tk):

    def __init__(self):
        """Izveido logu: augšā tabulas izvēle, kreisajā pusē lauki, labajā saraksts."""
        super().__init__()
        self.title("Filmu bibliotēka")
        self.geometry("1100x500")

        # Izvēlne, ar kuru izvēlas tabulu
        tk.Label(self, text="Tabula:").pack(anchor="w", padx=10, pady=(10, 0))
        self.izvele = ttk.Combobox(self, values=list(TABULAS), state="readonly")
        self.izvele.pack(anchor="w", padx=10)
        self.izvele.bind("<<ComboboxSelected>>", lambda notikums: self.paradit_tabulu())

        # Kreisā puse: ievades lauki un pogas
        self.forma = tk.Frame(self)
        self.forma.pack(side="left", fill="y", padx=10, pady=10)

        # Labā puse: tabulas dati
        self.saraksts = ttk.Treeview(self, show="headings")
        self.saraksts.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.saraksts.bind("<<TreeviewSelect>>", lambda notikums: self.ielikt_laukos())

        self.izvele.set("movies")   # sākumā rāda filmas
        self.paradit_tabulu()

    def tabula(self):
        """Atgriež pašlaik izvēlētās tabulas nosaukumu."""
        return self.izvele.get()

    def paradit_tabulu(self):
        """Uzzīmē laukus un pogas izvēlētajai tabulai un ielādē tās datus."""
        # Notīra vecos laukus
        for elements in self.forma.winfo_children():
            elements.destroy()

        # Katrai kolonnai: uzraksts + teksta lauks
        self.lauki = {}
        for rinda, kolonna in enumerate(TABULAS[self.tabula()]):
            tk.Label(self.forma, text=kolonna).grid(row=rinda, column=0, sticky="w")
            lauks = tk.Entry(self.forma, width=30)
            lauks.grid(row=rinda, column=1, pady=2)
            self.lauki[kolonna] = lauks

        # Pogas
        pogas = tk.Frame(self.forma)
        pogas.grid(row=len(self.lauki), column=0, columnspan=2, pady=10)
        tk.Button(pogas, text="Pievienot", command=self.pievienot).pack(side="left")
        tk.Button(pogas, text="Labot",     command=self.labot).pack(side="left", padx=5)
        tk.Button(pogas, text="Dzēst",     command=self.dzest).pack(side="left")
        tk.Button(pogas, text="Notīrīt",   command=self.notirit).pack(side="left", padx=5)

        # Saraksta kolonnas: id + lietotāja kolonnas
        kolonnas = ["id"] + TABULAS[self.tabula()]
        self.saraksts["columns"] = kolonnas
        for kolonna in kolonnas:
            self.saraksts.heading(kolonna, text=kolonna)
            self.saraksts.column(kolonna, width=100)

        self.ieladet_datus()

    def ieladet_datus(self):
        """Nolasa visus ierakstus no datubāzes (SELECT) un parāda sarakstā."""
        self.saraksts.delete(*self.saraksts.get_children())
        kolonnas = ", ".join(["id"] + TABULAS[self.tabula()])
        conn = savienot()
        for ieraksts in conn.execute(f"SELECT {kolonnas} FROM {self.tabula()}"):
            # None (tukša vērtība) rādām kā tukšu tekstu
            self.saraksts.insert("", "end", values=["" if v is None else v for v in ieraksts])
        conn.close()

    def ielikt_laukos(self):
        """Kad uzklikšķina uz rindas sarakstā, tās dati parādās laukos."""
        izveletais = self.saraksts.selection()
        if not izveletais:
            return
        vertibas = self.saraksts.item(izveletais[0])["values"][1:]  # [1:] = bez id
        for lauks, vertiba in zip(self.lauki.values(), vertibas):
            lauks.delete(0, "end")
            lauks.insert(0, vertiba)

    def notirit(self):
        """Iztukšo visus laukus."""
        for lauks in self.lauki.values():
            lauks.delete(0, "end")
        self.saraksts.selection_remove(self.saraksts.selection())

    def lauku_vertibas(self):
        """Nolasa tekstu no laukiem. Tukšs lauks datubāzē saglabājas kā NULL."""
        return [lauks.get().strip() or None for lauks in self.lauki.values()]

    def izveleta_id(self):
        """Atgriež sarakstā izvēlētās rindas id (vai None, ja nekas nav izvēlēts)."""
        izveletais = self.saraksts.selection()
        if not izveletais:
            messagebox.showwarning("Uzmanību", "Vispirms izvēlies rindu sarakstā!")
            return None
        return self.saraksts.item(izveletais[0])["values"][0]

    def izpildit_sql(self, sql, parametri):
        """Izpilda SQL komandu. Ja ir kļūda (piem. neeksistējošs ID), parāda to."""
        conn = savienot()
        try:
            conn.execute(sql, parametri)
            conn.commit()
        except sqlite3.Error as kluda:
            messagebox.showerror("Kļūda", str(kluda))
        conn.close()
        self.ieladet_datus()

    # --- Pogu darbības (CRUD: Create, Update, Delete) ---

    def pievienot(self):
        """INSERT - pievieno jaunu ierakstu."""
        kolonnas = ", ".join(self.lauki)                   # "name, birthday, ..."
        jautajumi = ", ".join(["?"] * len(self.lauki))     # "?, ?, ..."
        self.izpildit_sql(f"INSERT INTO {self.tabula()} ({kolonnas}) VALUES ({jautajumi})",
                          self.lauku_vertibas())
        self.notirit()

    def labot(self):
        """UPDATE - izmaina izvēlēto ierakstu."""
        ieraksta_id = self.izveleta_id()
        if ieraksta_id is None:
            return
        izmainas = ", ".join(f"{kolonna} = ?" for kolonna in self.lauki)  # "name = ?, ..."
        self.izpildit_sql(
            f"UPDATE {self.tabula()} SET {izmainas}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            self.lauku_vertibas() + [ieraksta_id])

    def dzest(self):
        """DELETE - izdzēš izvēlēto ierakstu (pēc apstiprinājuma)."""
        ieraksta_id = self.izveleta_id()
        if ieraksta_id is not None and messagebox.askyesno("Dzēst", f"Dzēst ierakstu ar ID {ieraksta_id}?"):
            self.izpildit_sql(f"DELETE FROM {self.tabula()} WHERE id = ?", [ieraksta_id])
            self.notirit()


# ------------------------------------------------------------
# 3. PROGRAMMAS SĀKUMS
# ------------------------------------------------------------
if __name__ == "__main__":
    izveidot_datubazi()
    FilmuBiblioteka().mainloop()

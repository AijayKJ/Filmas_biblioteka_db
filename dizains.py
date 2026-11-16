
import tkinter as tk
from tkinter import ttk


# =====================================================
# KRĀSU PALETE
# =====================================================

BG = "#101318"
SIDEBAR = "#171B22"
PANEL = "#1A2029"
FIELD = "#222A35"

WHITE = "#EDF1F5"
GREY = "#A2ACB8"
MUTED = "#737F8D"

ACCENT = "#D5A45B"
BORDER = "#2B3542"
DANGER = "#A84F55"


# =====================================================
# TABULU NOSAUKUMI
# =====================================================

TABLE_TITLES = {
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


# =====================================================
# STILS
# =====================================================

def setup_style(app):

    app.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=PANEL,
        foreground=WHITE,
        fieldbackground=PANEL,
        rowheight=38,
        font=("Segoe UI", 9),
        borderwidth=0
    )

    style.configure(
        "Treeview.Heading",
        background=FIELD,
        foreground=GREY,
        font=("Segoe UI", 8, "bold"),
        padding=12,
        relief="flat"
    )

    style.map(
        "Treeview",
        background=[("selected", "#39414B")],
        foreground=[("selected", WHITE)]
    )

    style.configure(
        "TCombobox",
        fieldbackground=FIELD,
        background=FIELD,
        foreground=WHITE,
        arrowcolor=ACCENT,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=8
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", FIELD)],
        foreground=[("readonly", WHITE)]
    )

    style.configure(
        "Vertical.TScrollbar",
        background=FIELD,
        troughcolor=BG,
        bordercolor=BG,
        arrowcolor=GREY
    )


# =====================================================
# POGAS
# =====================================================

def make_button(parent, text, command, color=FIELD, fg=WHITE):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=ACCENT,
        activeforeground="#17191D",
        relief="flat",
        bd=0,
        padx=14,
        pady=11,
        cursor="hand2",
        font=("Segoe UI", 9, "bold")
    )


# =====================================================
# IEVADES LAUKI
# =====================================================

def create_fields(app):

    for widget in app.form_fields.winfo_children():
        widget.destroy()

    app.entries = {}

    table = app.current_table

    for column in app.TABULAS[table]:

        label = app.LAUKE_NOSAUKUMI.get(
            column,
            column.replace("_", " ").title()
        )

        tk.Label(
            app.form_fields,
            text=label.upper(),
            bg=PANEL,
            fg=GREY,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            pady=(12, 5)
        )

        # ĀRĒJO ATSLĒGU IZVĒLE

        if column in app.FK:

            related_table, label_column = app.FK[column]

            conn = __import__("main").savienot()

            try:

                records = conn.execute(
                    f"SELECT id, {label_column} "
                    f"FROM {related_table} "
                    f"ORDER BY {label_column}"
                ).fetchall()

            finally:
                conn.close()

            options = [
                f"{row[0]} — {row[1]}"
                for row in records
            ]

            entry = ttk.Combobox(
                app.form_fields,
                values=options,
                state="readonly",
                font=("Segoe UI", 9)
            )

            entry.pack(
                fill="x",
                ipady=3
            )

        else:

            entry = tk.Entry(
                app.form_fields,
                bg=FIELD,
                fg=WHITE,
                insertbackground=ACCENT,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9),
                highlightthickness=1,
                highlightbackground=BORDER,
                highlightcolor=ACCENT
            )

            entry.pack(
                fill="x",
                ipady=9
            )

        app.entries[column] = entry


# =====================================================
# IERAKSTU PĀRVALDĪBAS FORMA
# =====================================================
def build_form(app):
    panel = app.form_panel

    tk.Label(
        panel,
        text="IERAKSTA PĀRVALDĪBA",
        bg=PANEL,
        fg=ACCENT,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        pady=(0, 8)
    )

    tk.Label(
        panel,
        text="Informācija",
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 19, "bold")
    ).pack(anchor="w")

    tk.Label(
        panel,
        text="Pievieno jaunu ierakstu vai rediģē esošu.",
        bg=PANEL,
        fg=GREY,
        font=("Segoe UI", 9),
        wraplength=260,
        justify="left"
    ).pack(
        anchor="w",
        pady=(5, 16)
    )

    # RITINĀMIE IEVADES LAUKI

    form_container = tk.Frame(
        panel,
        bg=PANEL
    )

    form_container.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        form_container,
        bg=PANEL,
        highlightthickness=0
    )
    # Peles ritenīša ritināšana

    def scroll_form(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def linux_scroll_up(event):
        canvas.yview_scroll(-1, "units")

    def linux_scroll_down(event):
        canvas.yview_scroll(1, "units")

    def enable_scroll(event):
        canvas.bind_all("<MouseWheel>", scroll_form)
        canvas.bind_all("<Button-4>", linux_scroll_up)
        canvas.bind_all("<Button-5>", linux_scroll_down)

    def disable_scroll(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", enable_scroll)
    canvas.bind("<Leave>", disable_scroll)
    
    scrollbar = ttk.Scrollbar(
        form_container,
        orient="vertical",
        command=canvas.yview
    )

    app.form_fields = tk.Frame(
        canvas,
        bg=PANEL
    )

    app.form_fields.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=app.form_fields,
        anchor="nw"
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            canvas_window,
            width=event.width
        )
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # POGU JOSLA

    app.form_buttons = tk.Frame(
        panel,
        bg=PANEL
    )

    app.form_buttons.pack(
        fill="x",
        side="bottom",
        pady=(15, 0)
    )

    make_button(
        app.form_buttons,
        "Pievienot ierakstu",
        app.add_record,
        ACCENT,
        "#17191D"
    ).pack(
        fill="x",
        pady=3
    )

    make_button(
        app.form_buttons,
        "Saglabāt izmaiņas",
        app.update_record,
        "#35404D"
    ).pack(
        fill="x",
        pady=3
    )

    button_row = tk.Frame(
        app.form_buttons,
        bg=PANEL
    )

    button_row.pack(
        fill="x",
        pady=3
    )

    make_button(
        button_row,
        "Notīrīt",
        app.clear_form
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 4)
    )

    make_button(
        button_row,
        "Dzēst",
        app.delete_record,
        "#482B30"
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=(4, 0)
    )

    create_fields(app)


# =====================================================
# GALVENĀ INTERFEISA IZVEIDE
# =====================================================

def build_interface(app):

    setup_style(app)

    app.title("Filmu bibliotēka")
    app.geometry("1500x900")
    app.minsize(1120, 700)

    # -------------------------------------------------
    # SĀNU IZVĒLNE
    # -------------------------------------------------

    app.sidebar = tk.Frame(
        app,
        bg=SIDEBAR,
        width=225
    )

    app.sidebar.pack(
        side="left",
        fill="y"
    )

    app.sidebar.pack_propagate(False)

    tk.Label(
        app.sidebar,
        text="KINOTEKA",
        bg=SIDEBAR,
        fg=WHITE,
        font=("Segoe UI", 18, "bold")
    ).pack(
        anchor="w",
        padx=24,
        pady=(32, 3)
    )

    tk.Label(
        app.sidebar,
        text="FILMU DATUBĀZE",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 30)
    )

    tk.Frame(
        app.sidebar,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=(0, 18)
    )

    tk.Label(
        app.sidebar,
        text="DATUBĀZE",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        padx=24,
        pady=(0, 10)
    )

    app.nav_buttons = {}

    navigation = [
        ("movies", "Filmas"),
        ("actors", "Aktieri"),
        ("directors", "Režisori"),
        ("genres", "Žanri"),
        ("studios", "Studijas"),
        ("users", "Lietotāji"),
        ("watchlist_items", "Skatīšanās saraksti"),
        ("reviews", "Atsauksmes"),
        ("movie_cast", "Filmu lomas"),
        ("movie_awards", "Filmu balvas")
    ]

    for table, title in navigation:

        button = tk.Button(
            app.sidebar,
            text=title,
            command=lambda t=table: app.change_table(t),
            bg=SIDEBAR,
            fg=GREY,
            activebackground="#303741",
            activeforeground=ACCENT,
            relief="flat",
            bd=0,
            anchor="w",
            padx=24,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 9)
        )

        button.pack(
            fill="x",
            padx=9,
            pady=1
        )

        app.nav_buttons[table] = button

    tk.Frame(
        app.sidebar,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=20,
        pady=20
    )

    tk.Label(
        app.sidebar,
        text="SQLite datubāze  •  lokāla",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(
        side="bottom",
        pady=22
    )

    # -------------------------------------------------
    # GALVENAIS SATURS
    # -------------------------------------------------

    app.main_area = tk.Frame(
        app,
        bg=BG
    )

    app.main_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    # AUGŠĒJĀ JOSLA

    header = tk.Frame(
        app.main_area,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=32,
        pady=(28, 18)
    )

    app.page_title = tk.Label(
        header,
        text="Filmas",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 25, "bold")
    )

    app.page_title.pack(
        side="left"
    )

    # MEKLĒŠANA

    app.search_var = tk.StringVar()

    search_wrap = tk.Frame(
        header,
        bg=FIELD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    search_wrap.pack(
        side="right"
    )

    tk.Label(
        search_wrap,
        text="⌕",
        bg=FIELD,
        fg=ACCENT,
        font=("Segoe UI", 17)
    ).pack(
        side="left",
        padx=(10, 4)
    )

    search = tk.Entry(
        search_wrap,
        textvariable=app.search_var,
        bg=FIELD,
        fg=WHITE,
        insertbackground=ACCENT,
        relief="flat",
        bd=0,
        font=("Segoe UI", 9),
        width=27
    )

    search.pack(
        side="left",
        padx=(2, 12),
        ipady=10
    )

    app.search_var.trace_add(
        "write",
        lambda *args: refresh_content(app)
    )

    # APRAKSTS

    intro = tk.Frame(
        app.main_area,
        bg=BG
    )

    intro.pack(
        fill="x",
        padx=32,
        pady=(0, 18)
    )

    tk.Label(
        intro,
        text="PĀRVALDI SAVU FILMU KOLEKCIJU",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 8, "bold")
    ).pack(anchor="w")

    tk.Label(
        intro,
        text="Viss vienuviet, pārskatāmi.",
        bg=BG,
        fg=GREY,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    tk.Frame(
        app.main_area,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=32,
        pady=(0, 18)
    )

    # -------------------------------------------------
    # DARBA LAUKUMS
    # -------------------------------------------------

    body = tk.Frame(
        app.main_area,
        bg=BG
    )

    body.pack(
        fill="both",
        expand=True,
        padx=32,
        pady=(0, 25)
    )

    app.content = tk.Frame(
        body,
        bg=BG
    )

    app.content.pack(
        side="left",
        fill="both",
        expand=True
    )

    app.form_panel = tk.Frame(
        body,
        bg=PANEL,
        width=310,
        padx=18,
        pady=18
    )

    app.form_panel.pack(
        side="right",
        fill="y",
        padx=(22, 0)
    )

    app.form_panel.pack_propagate(False)

    build_form(app)

    refresh_content(app)


# =====================================================
# SATURA ATJAUNOŠANA
# =====================================================

def refresh_content(app):

    if not hasattr(app, "content"):
        return

    for widget in app.content.winfo_children():
        widget.destroy()

    table = app.current_table

    search = app.search_var.get().strip().lower()

    app.page_title.configure(
        text=TABLE_TITLES[table]
    )

    # AKTĪVĀ IZVĒLNE

    for name, button in app.nav_buttons.items():

        active = name == table

        button.configure(
            bg="#303741" if active else SIDEBAR,
            fg=ACCENT if active else GREY,
            font=(
                "Segoe UI",
                9,
                "bold" if active else "normal"
            )
        )

    records = app.get_records(table)

    # MEKLĒŠANA

    if search:

        filtered = []

        for record in records:

            values = [
                str(value)
                for value in record
                if value is not None
            ]

            for field, value in zip(
                app.TABULAS[table],
                record[1:]
            ):

                values.append(
                    app.display_value(field, value)
                )

            text = " ".join(values).lower()

            if search in text:
                filtered.append(record)

        records = filtered

    tk.Label(
        app.content,
        text=f"{len(records)} IERAKSTI",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 8, "bold")
    ).pack(
        anchor="w",
        pady=(0, 10)
    )

    show_table(app, records)


# =====================================================
# DATU TABULA
# =====================================================

def show_table(app, records):

    table = app.current_table

    columns = ["id"] + app.TABULAS[table]

    wrap = tk.Frame(
        app.content,
        bg=PANEL,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    wrap.pack(
        fill="both",
        expand=True
    )

    tree = ttk.Treeview(
        wrap,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    ybar = ttk.Scrollbar(
        wrap,
        orient="vertical",
        command=tree.yview
    )

    xbar = ttk.Scrollbar(
        wrap,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=ybar.set,
        xscrollcommand=xbar.set
    )

    # KOLONNAS

    for column in columns:

        if column == "id":
            heading = "ID"
            width = 65

        else:
            heading = app.LAUKE_NOSAUKUMI.get(
                column,
                column.replace("_", " ").upper()
            ).upper()

            width = 190 if column in (
                "title", "synopsis", "body", "description"
            ) else 135

        tree.heading(
            column,
            text=heading
        )

        tree.column(
            column,
            width=width,
            minwidth=80,
            anchor="w",
            stretch=True
        )

    # IERAKSTI

    for record in records:

        shown = [record[0]]

        for field, value in zip(
            app.TABULAS[table],
            record[1:]
        ):

            shown.append(
                app.display_value(field, value)
            )

        tree.insert(
            "",
            "end",
            iid=str(record[0]),
            values=shown
        )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    ybar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    xbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    wrap.grid_rowconfigure(
        0,
        weight=1
    )

    wrap.grid_columnconfigure(
        0,
        weight=1
    )

    tree.bind(
        "<<TreeviewSelect>>",
        lambda event: select_tree_record(app, tree)
    )

    app.current_tree = tree

    if not records:

        tk.Label(
            app.content,
            text="Šeit pagaidām nav ierakstu.",
            bg=BG,
            fg=GREY,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=18
        )


# =====================================================
# IERAKSTA IZVĒLE
# =====================================================

def select_tree_record(app, tree):

    selected = tree.selection()

    if selected:

        record_id = int(selected[0])

        record = app.get_record(
            app.current_table,
            record_id
        )

        if record:
            app.select_record(record)

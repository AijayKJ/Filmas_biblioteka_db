# Filmu bibliotēka

Šī ir vienkārša Python lietojumprogramma ar grafisko interfeisu (GUI), kas ļauj pārvaldīt filmu bibliotēku un saglabāt datus SQLite datubāzē.

---

## Galvenās iespējas

- 10 savstarpēji saistītas datubāzes tabulas:
  - `movies` — filmas
  - `actors` — aktieri
  - `directors` — režisori
  - `genres` — žanri
  - `users` — lietotāji
  - `studios` — studijas
  - `movie_awards` — filmu balvas
  - `movie_cast` — filmu aktieru lomas
  - `watchlist_items` — skatīšanās saraksti
  - `reviews` — atsauksmes
- Pilns CRUD cikls — ierakstu pievienošana, apskatīšana, labošana un dzēšana.
- Automātiska datubāze — lietotne izveido tabulas un sākotnējos datus, ja tie vēl nepastāv.
- Datu integritāte — ārējās atslēgas un SQLite ierobežojumi.
- Meklēšana pēc ievadītās vērtības.

---

## Izmantotās tehnoloģijas

- Python 3
- Tkinter un ttk
- SQLite3

---

## Kā palaist lietotni

1. Pārliecinies, ka datorā ir instalēts Python.
2. Terminālī atver projekta mapi.
3. Palaid lietotni:

   ```bash
   python main.py
   ```

SQLite datubāze atrodas projekta mapē failā `filmu_biblioteka.db`. Lietotnei tā ir jāinicializē, bet atsevišķi to izveidot nevajag.

---

## Projekta mapes un faili

```text
filma.py/
├── main.py
├── filmu_biblioteka.db
├── README.md
├── app/
│   ├── config.py
│   ├── database.py
│   └── library_app.py
└── ui/
    ├── theme.py
    ├── forms.py
    ├── main_window.py
    └── content.py
```

### `main.py`

Programmas galvenais fails. Tas inicializē datubāzi, izveido lietotnes logu un palaiž Tkinter galveno ciklu.

### `filmu_biblioteka.db`

Esošā SQLite datubāze ar lietotnes datiem. Neizdzēs un neaizstāj šo failu, ja vēlies saglabāt esošos ierakstus.

### `app/` mape

Šajā mapē atrodas lietotnes loģika un datubāzes darbības:

- `config.py` — tabulu kolonnu saraksti, ārējās atslēgas un laukumu nosaukumi latviešu valodā.
- `database.py` — SQLite savienojums, tabulu izveide, sākotnējie dati un datubāzes inicializācija.
- `library_app.py` — `FilmuBiblioteka` klase ar ierakstu nolasīšanu, pievienošanu, labošanu, dzēšanu un formas vērtību apstrādi.

### `ui/` mape

Šajā mapē atrodas lietotāja interfeisa elementi:

- `theme.py` — krāsu palete, tabulu nosaukumi, Tkinter stili un pogu izveides palīgfunkcija.
- `forms.py` — ievades laukumu un atlases izvēlņu formas veidošana.
- `main_window.py` — sānu izvēlnes, virsraksta, meklēšanas joslas un galvenā loga izkārtojuma veidošana.
- `content.py` — ierakstu filtrēšana, datu tabulas parādīšana un atlasītā ieraksta apstrāde.

---

## Ievades lauku piemērs

Tabulas `movie_cast` laukam **Lomas secība** jāievada aktiera vieta aktieru sarakstā kā vesels pozitīvs skaitlis:

- `1` — galvenā loma vai pirmā rinda
- `2` — otra loma
- `3` — trešā loma

Piemēram, aktierim Leonardo DiCaprio filmā `Inception`:

- **Filma:** Inception
- **Aktieris:** Leonardo DiCaprio
- **Tēla vārds:** Dom Cobb
- **Lomas secība:** `1`

<img width="1131" height="731" alt="Ekrānuzņēmums 2026-11-06 100529" src="https://github.com/user-attachments/assets/90d19d96-efc8-4262-bb98-701e051c89a4" />

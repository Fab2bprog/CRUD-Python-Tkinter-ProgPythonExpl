# ProgPythonExpl

Professional-grade CRUD demonstration program in Python – Tkinter GUI – SQLite database – MVC Architecture.

Programme de démonstration CRUD Python de niveau professionnel – Interface graphique Tkinter – Base SQLite – Architecture MVC.

<p align="center">
  <img src="https://github.com/Fab2bprog/CRUD-Python-Tkinter-ProgPythonExpl/blob/main/images/crudpythonpic.png" width="650" >
</p>

---

## 🇬🇧 English

### Description

**ProgPythonExpl** is a CRUD (Create – Read – Update – Delete) application designed as a reference example and starting point for future Python projects.

It manages the main operations on a **Clients** table in a SQLite database:
search, create, update, delete and select records.

---

### Prerequisites

- **Python 3.13** or higher
- **No external dependencies** — standard Python modules only
- **Tkinter** (included in standard Python)
- **SQLite 3** (included in standard Python)
- Compatible with **Linux**, macOS and Windows

---

### Installation

```bash
# Extract the ZIP, that's all — no additional installation required.
cd ProgPythonExpl
```

---

### Launch

```bash
python main.py
```

---

### Seeding the demo database (optional)

```bash
# Creates demo.sqlite with 10 fictional clients
python seed_data.py

# Or specify an existing file
python seed_data.py /path/to/my_database.sqlite
```

---

### Project Structure (MVC Architecture)

```
ProgPythonExpl/
│
├── main.py                          # Entry point – launcher
├── seed_data.py                     # Data seeding script
├── requirements.txt                 # Python dependencies
│
├── core/                            # Configuration and database access
│   ├── __init__.py
│   ├── config.py                    # Global constants (colors, fonts, modes...)
│   └── database.py                  # GestionnaireBase: SQLite connection
│
├── models/                          # Model layer
│   ├── __init__.py
│   └── client_model.py              # Client dataclass + ClientDAO (CRUDS)
│
├── controllers/                     # Controller layer
│   ├── __init__.py
│   ├── bienvenue_controller.py      # Main window logic
│   ├── cruds_controller.py          # Client list/management logic
│   └── fiche_controller.py          # Client form logic + validation
│
├── views/                           # View layer (Tkinter windows)
│   ├── __init__.py
│   ├── Win_Bienvenue_Main.py        # Main window (File + Actions menus)
│   ├── Win_Client_CRUDS.py          # Client table + icon buttons
│   └── Win_Client_Fiche.py          # Client record form
│
├── classes/                         # Shared / utility classes
│   ├── __init__.py
│   └── base_window.py               # FenetreBase: modal Toplevel + ttk theme
│
├── fonctionsgen/                    # General utility functions
│   ├── __init__.py
│   └── fonctionsgen.py              # Formatting, validation, data manipulation
│
└── images/                          # Button icons (60×60 px PNG)
    ├── Base_create.png              # Add button
    ├── Base_update.png              # Edit button
    ├── Base_delete.png              # Delete button
    ├── Base_read.png                # View button
    ├── Base_search.png              # Search button
    ├── Base_select.png              # Select button (selection mode)
    ├── Base_save.png                # Save button (client form)
    └── zone_exit.png                # Quit / Cancel button
```

---

### Button Images

The PNG icons in the `images/` folder must be in **PNG format, exactly 60×60 pixels**.
Tkinter loads PNG natively, no external library required.

> **Note:** If images are missing, buttons display their text label as a fallback.
> The program runs perfectly without images.

---

### Window Opening Modes

#### Win_Client_CRUDS
| Mode | Constant | Description |
|------|----------|-------------|
| Standard | `STD` | Full CRUD (Add, Edit, Delete, View) |
| Single selection | `S1` | Select one client – returns `(id, name)` |
| Multiple selection | `SX` | Select several clients – returns `[(id, name), ...]` |

#### Win_Client_Fiche
| Mode | Constant | Description |
|------|----------|-------------|
| Read-only | `L` | All fields disabled, Close button only |
| Edit | `M` | Active input, Validate and Cancel buttons |

---

### Clients Table – SQLite Structure

| Column | Type | Constraints |
|--------|------|-------------|
| IDCLIENT | INTEGER | PRIMARY KEY (managed by Python) |
| nom_client | TEXT | NOT NULL |
| numero_telephone | TEXT | NOT NULL |
| adresse | TEXT | NOT NULL |
| code_postal | TEXT | NOT NULL, 5 digits |
| ville | TEXT | NOT NULL |
| date_naissance | TEXT | NOT NULL, ISO format YYYY-MM-DD |
| credit_disponible | REAL | NOT NULL, >= 0 |
| bon_client | INTEGER | NOT NULL, 0 or 1 |
| couleur_cheveux | TEXT | NOT NULL, brun/blond/roux/chauve |

---

### Design Principles

- **Strict MVC architecture**: models, views and controllers clearly separated
- **Window modality**: `Toplevel` + `grab_set()` + `transient(parent)`
- **Validation**: real-time (validatecommand) + full validation on submit
- **SQLite error handling**: non-blocking messagebox popup
- **ID incrementation**: managed in Python via `SELECT MAX(IDCLIENT) + 1`
- **Missing images**: automatic text fallback, no exception raised
- **Linux compatible**: paths built with `os.path.join`

---
---

## 🇫🇷 Français

### Description

**ProgPythonExpl** est un programme de type CRUD (Create – Read – Update – Delete)
servant d'exemple et de base de réflexion pour le développement de futurs projets Python.

Il gère les opérations principales sur une table **Clients** dans une base SQLite :
recherche, création, modification, suppression et sélection d'enregistrements.

---

### Prérequis

- **Python 3.13** ou supérieur
- **Aucune dépendance externe** — uniquement des modules Python standard
- **Tkinter** (inclus dans Python standard)
- **SQLite 3** (inclus dans Python standard)
- Compatible **Linux**, macOS et Windows

---

### Installation

```bash
# Extraire le ZIP, c'est tout — aucune installation supplémentaire requise.
cd ProgPythonExpl
```

---

### Lancement

```bash
python main.py
```

---

### Peuplement de la base de démonstration (optionnel)

```bash
# Crée demo.sqlite avec 10 clients fictifs
python seed_data.py

# Ou spécifier un fichier existant
python seed_data.py /chemin/vers/ma_base.sqlite
```

---

### Structure du projet (Architecture MVC)

```
ProgPythonExpl/
│
├── main.py                          # Point d'entrée – lanceur
├── seed_data.py                     # Script de peuplement
├── requirements.txt                 # Dépendances Python
│
├── core/                            # Configuration et accès base de données
│   ├── __init__.py
│   ├── config.py                    # Constantes globales (couleurs, polices, modes...)
│   └── database.py                  # GestionnaireBase : connexion SQLite
│
├── models/                          # Couche Modèle
│   ├── __init__.py
│   └── client_model.py              # Dataclass Client + ClientDAO (CRUDS)
│
├── controllers/                     # Couche Contrôleur
│   ├── __init__.py
│   ├── bienvenue_controller.py      # Logique fenêtre principale
│   ├── cruds_controller.py          # Logique fenêtre liste/gestion clients
│   └── fiche_controller.py          # Logique fenêtre fiche client + validation
│
├── views/                           # Couche Vue (fenêtres Tkinter)
│   ├── __init__.py
│   ├── Win_Bienvenue_Main.py        # Fenêtre principale (menu Fichier + Actions)
│   ├── Win_Client_CRUDS.py          # Tableau clients + boutons icônes
│   └── Win_Client_Fiche.py          # Formulaire fiche client
│
├── classes/                         # Classes communes / utilitaires
│   ├── __init__.py
│   └── base_window.py               # FenetreBase : Toplevel modal + thème ttk
│
├── fonctionsgen/                    # Fonctions utilitaires générales
│   ├── __init__.py
│   └── fonctionsgen.py              # Formatage, validation, manipulation de données
│
└── images/                          # Icônes des boutons (60×60 px PNG)
    ├── Base_create.png              # Bouton Ajouter
    ├── Base_update.png              # Bouton Modifier
    ├── Base_delete.png              # Bouton Supprimer
    ├── Base_read.png                # Bouton Consulter
    ├── Base_search.png              # Bouton Rechercher
    ├── Base_select.png              # Bouton Sélectionner (mode sélection)
    ├── Base_save.png                # Bouton Valider (fiche client)
    └── zone_exit.png                # Bouton Quitter / Annuler
```

---

### Images des boutons

Les icônes PNG du dossier `images/` doivent être au format **PNG, exactement 60×60 pixels**.
Tkinter charge les PNG nativement, sans aucune bibliothèque externe.

> **Note :** Si les images sont absentes, les boutons s'affichent avec leur libellé
> texte en remplacement. Le programme fonctionne parfaitement sans les images.

---

### Modes d'ouverture des fenêtres

#### Win_Client_CRUDS
| Mode | Constante | Description |
|------|-----------|-------------|
| Standard | `STD` | CRUD complet (Ajouter, Modifier, Supprimer, Consulter) |
| Sélection simple | `S1` | Sélection d'un seul client – retourne `(id, nom)` |
| Sélection multiple | `SX` | Sélection de plusieurs clients – retourne `[(id, nom), ...]` |

#### Win_Client_Fiche
| Mode | Constante | Description |
|------|-----------|-------------|
| Lecture | `L` | Tous les champs désactivés, bouton Fermer uniquement |
| Modification | `M` | Saisie active, boutons Valider et Annuler |

---

### Table Clients – Structure SQLite

| Colonne | Type | Contraintes |
|---------|------|-------------|
| IDCLIENT | INTEGER | PRIMARY KEY (géré par Python) |
| nom_client | TEXT | NOT NULL |
| numero_telephone | TEXT | NOT NULL |
| adresse | TEXT | NOT NULL |
| code_postal | TEXT | NOT NULL, 5 chiffres |
| ville | TEXT | NOT NULL |
| date_naissance | TEXT | NOT NULL, format ISO YYYY-MM-DD |
| credit_disponible | REAL | NOT NULL, >= 0 |
| bon_client | INTEGER | NOT NULL, 0 ou 1 |
| couleur_cheveux | TEXT | NOT NULL, brun/blond/roux/chauve |

---

### Principes de conception

- **Architecture MVC** stricte : modèles, vues et contrôleurs clairement séparés
- **Modalité** des fenêtres : `Toplevel` + `grab_set()` + `transient(parent)`
- **Validation** : temps réel (validatecommand) + validation globale à la soumission
- **Gestion des erreurs SQLite** : popup messagebox non bloquante
- **Incrémentation des ID** : gérée en Python via `SELECT MAX(IDCLIENT) + 1`
- **Images manquantes** : fallback texte automatique, sans exception
- **Compatible Linux** : chemins construits avec `os.path.join`

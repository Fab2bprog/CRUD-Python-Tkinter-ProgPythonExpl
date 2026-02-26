# =============================================================================
# core/config.py
# Configuration centrale de l'application ProgPythonExpl
# =============================================================================

import os

# ---------------------------------------------------------------------------
# Chemins
# ---------------------------------------------------------------------------
# Répertoire racine du projet (dossier parent de /core)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dossier contenant toutes les images / icônes
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# ---------------------------------------------------------------------------
# Paramètres de l'interface graphique
# ---------------------------------------------------------------------------
APP_TITLE = "ProgPythonExpl"

# Thème sobre et professionnel (gris/bleu)
COULEURS = {
    "fond_principal"   : "#F0F2F5",   # Gris très clair – arrière-plan général
    "fond_secondaire"  : "#FFFFFF",   # Blanc – zones de saisie, tableaux
    "fond_barre"       : "#2C3E50",   # Bleu-gris foncé – barres latérales
    "fond_bouton"      : "#3498DB",   # Bleu – boutons d'action principaux
    "fond_bouton_hover": "#2980B9",   # Bleu foncé – survol bouton
    "fond_bouton_exit" : "#E74C3C",   # Rouge – bouton quitter
    "texte_principal"  : "#2C3E50",   # Bleu-gris foncé – texte standard
    "texte_clair"      : "#FFFFFF",   # Blanc – texte sur fond sombre
    "texte_erreur"     : "#E74C3C",   # Rouge – messages d'erreur
    "bordure"          : "#BDC3C7",   # Gris – bordures et séparateurs
    "selection"        : "#AED6F1",   # Bleu clair – ligne sélectionnée
    "entete_tableau"   : "#2C3E50",   # Fond entête tableau
}

POLICES = {
    "titre"      : ("Segoe UI", 14, "bold"),
    "sous_titre" : ("Segoe UI", 11, "bold"),
    "normale"    : ("Segoe UI", 10),
    "petite"     : ("Segoe UI",  9),
    "mono"       : ("Courier New", 10),
}

# Taille des icônes boutons (pixels)
ICONE_TAILLE = 60

# ---------------------------------------------------------------------------
# Paramètres des fenêtres
# ---------------------------------------------------------------------------
FENETRES = {
    "bienvenue": {
        "titre"     : "Bienvenue",
        "largeur"   : 700,
        "hauteur"   : 450,
        "min_largeur": 600,
        "min_hauteur": 380,
    },
    "cruds": {
        "titre"      : "Opérations Possibles",
        "largeur"    : 950,
        "hauteur"    : 620,
        "min_largeur": 800,
        "min_hauteur": 500,
    },
    "fiche": {
        "titre"      : "Fiche Client",
        "largeur"    : 480,
        "hauteur"    : 560,
        "min_largeur": 420,
        "min_hauteur": 500,
    },
}

# ---------------------------------------------------------------------------
# Paramètres base de données
# ---------------------------------------------------------------------------
DB_EXTENSION = ".sqlite"

# ---------------------------------------------------------------------------
# Modes d'ouverture des fenêtres
# ---------------------------------------------------------------------------
MODE_STANDARD        = "STD"   # Gestion complète CRUD
MODE_SELECTION_SIMPLE = "S1"   # Sélection d'un seul enregistrement
MODE_SELECTION_MULTI  = "SX"   # Sélection de plusieurs enregistrements
MODE_LECTURE          = "L"    # Lecture seule (fiche client)
MODE_MODIFICATION     = "M"    # Modification (fiche client)

# ---------------------------------------------------------------------------
# Couleurs des cheveux (valeurs acceptées par la base)
# ---------------------------------------------------------------------------
COULEURS_CHEVEUX = ["brun", "blond", "roux", "chauve"]

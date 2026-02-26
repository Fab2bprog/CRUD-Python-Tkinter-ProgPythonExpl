# =============================================================================
# seed_data.py
# Script de peuplement de la base de données avec des clients fictifs.
#
# Utilisation :
#   python seed_data.py [chemin_vers_base.sqlite]
#
# Si aucun chemin n'est fourni, le script crée "demo.sqlite" dans le
# répertoire courant.
#
# Ce script est indépendant de l'interface graphique (pas de Tkinter).
# =============================================================================

import sys
import os
import sqlite3

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import GestionnaireBase, SQL_CREATE_TABLE_CLIENTS
from models.client_model import Client, ClientDAO


# ---------------------------------------------------------------------------
# Données de démonstration
# ---------------------------------------------------------------------------

CLIENTS_DEMO: list[dict] = [
    {
        "nom_client"        : "Martin Jean",
        "numero_telephone"  : "01 23 45 67 89",
        "adresse"           : "12 rue de la Paix",
        "code_postal"       : "75001",
        "ville"             : "Paris",
        "date_naissance"    : "1985-03-15",
        "credit_disponible" : 1500.00,
        "bon_client"        : True,
        "couleur_cheveux"   : "brun",
    },
    {
        "nom_client"        : "Dupont Marie",
        "numero_telephone"  : "04 56 78 90 12",
        "adresse"           : "8 avenue des Fleurs",
        "code_postal"       : "69002",
        "ville"             : "Lyon",
        "date_naissance"    : "1992-07-22",
        "credit_disponible" : 800.50,
        "bon_client"        : False,
        "couleur_cheveux"   : "blond",
    },
    {
        "nom_client"        : "Bernard Sophie",
        "numero_telephone"  : "05 67 89 01 23",
        "adresse"           : "3 place du Capitole",
        "code_postal"       : "31000",
        "ville"             : "Toulouse",
        "date_naissance"    : "1978-11-08",
        "credit_disponible" : 2200.00,
        "bon_client"        : True,
        "couleur_cheveux"   : "roux",
    },
    {
        "nom_client"        : "Petit Robert",
        "numero_telephone"  : "03 45 67 89 01",
        "adresse"           : "27 rue du Commerce",
        "code_postal"       : "59000",
        "ville"             : "Lille",
        "date_naissance"    : "1965-04-30",
        "credit_disponible" : 0.00,
        "bon_client"        : False,
        "couleur_cheveux"   : "chauve",
    },
    {
        "nom_client"        : "Laurent Claire",
        "numero_telephone"  : "02 34 56 78 90",
        "adresse"           : "15 rue de la Loire",
        "code_postal"       : "44000",
        "ville"             : "Nantes",
        "date_naissance"    : "1990-09-12",
        "credit_disponible" : 3500.75,
        "bon_client"        : True,
        "couleur_cheveux"   : "blond",
    },
    {
        "nom_client"        : "Thomas Pierre",
        "numero_telephone"  : "04 89 01 23 45",
        "adresse"           : "42 boulevard Michelet",
        "code_postal"       : "13008",
        "ville"             : "Marseille",
        "date_naissance"    : "1982-01-25",
        "credit_disponible" : 650.00,
        "bon_client"        : True,
        "couleur_cheveux"   : "brun",
    },
    {
        "nom_client"        : "Robert Anne",
        "numero_telephone"  : "03 78 90 12 34",
        "adresse"           : "5 rue des Halles",
        "code_postal"       : "67000",
        "ville"             : "Strasbourg",
        "date_naissance"    : "1975-06-18",
        "credit_disponible" : 120.30,
        "bon_client"        : False,
        "couleur_cheveux"   : "roux",
    },
    {
        "nom_client"        : "Moreau Luc",
        "numero_telephone"  : "05 12 34 56 78",
        "adresse"           : "88 avenue de la Gare",
        "code_postal"       : "33000",
        "ville"             : "Bordeaux",
        "date_naissance"    : "2000-12-05",
        "credit_disponible" : 4000.00,
        "bon_client"        : True,
        "couleur_cheveux"   : "blond",
    },
    {
        "nom_client"        : "Simon Isabelle",
        "numero_telephone"  : "01 90 12 34 56",
        "adresse"           : "19 rue Nationale",
        "code_postal"       : "75013",
        "ville"             : "Paris",
        "date_naissance"    : "1988-08-14",
        "credit_disponible" : 275.00,
        "bon_client"        : False,
        "couleur_cheveux"   : "brun",
    },
    {
        "nom_client"        : "Michel François",
        "numero_telephone"  : "04 23 45 67 89",
        "adresse"           : "7 chemin des Vignes",
        "code_postal"       : "06000",
        "ville"             : "Nice",
        "date_naissance"    : "1955-02-28",
        "credit_disponible" : 9999.99,
        "bon_client"        : True,
        "couleur_cheveux"   : "chauve",
    },
]


# ---------------------------------------------------------------------------
# Fonction principale
# ---------------------------------------------------------------------------

def peupler_base(chemin_base: str) -> None:
    """
    Crée la base SQLite (si inexistante) et insère les clients de démonstration.

    :param chemin_base: Chemin vers le fichier .sqlite
    """
    print(f"Base de données cible : {chemin_base}")

    db = GestionnaireBase()
    if not db.ouvrir(chemin_base):
        print("Erreur : impossible d'ouvrir ou de créer la base.")
        sys.exit(1)

    nb_existants = ClientDAO.compter(db)
    if nb_existants > 0:
        reponse = input(
            f"La base contient déjà {nb_existants} client(s). "
            "Ajouter quand même les données de démonstration ? (o/N) : "
        ).strip().lower()
        if reponse not in ("o", "oui", "y", "yes"):
            print("Opération annulée.")
            db.fermer()
            return

    nb_inseres = 0
    for donnees in CLIENTS_DEMO:
        client = Client(
            nom_client        = donnees["nom_client"],
            numero_telephone  = donnees["numero_telephone"],
            adresse           = donnees["adresse"],
            code_postal       = donnees["code_postal"],
            ville             = donnees["ville"],
            date_naissance    = donnees["date_naissance"],
            credit_disponible = donnees["credit_disponible"],
            bon_client        = donnees["bon_client"],
            couleur_cheveux   = donnees["couleur_cheveux"],
        )
        nouvel_id = ClientDAO.creer(db, client)
        if nouvel_id is not None:
            nb_inseres += 1
            print(f"  [OK] {client.nom_client} (ID={nouvel_id})")
        else:
            print(f"  [ERREUR] {client.nom_client}")

    db.fermer()
    print(f"\n{nb_inseres}/{len(CLIENTS_DEMO)} clients insérés avec succès.")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        chemin = sys.argv[1]
    else:
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.sqlite")

    peupler_base(chemin)

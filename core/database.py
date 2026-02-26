# =============================================================================
# core/database.py
# Gestionnaire de connexion à la base de données SQLite
# Fournit une interface propre et thread-safe pour toute l'application.
# =============================================================================

import sqlite3
import os
from tkinter import messagebox


# ---------------------------------------------------------------------------
# Requête de création de la table Clients
# ---------------------------------------------------------------------------
SQL_CREATE_TABLE_CLIENTS = """
CREATE TABLE IF NOT EXISTS Clients (
    IDCLIENT         INTEGER PRIMARY KEY,
    nom_client       TEXT    NOT NULL,
    numero_telephone TEXT    NOT NULL,
    adresse          TEXT    NOT NULL,
    code_postal      TEXT    NOT NULL
        CHECK (
            length(code_postal) = 5
            AND code_postal GLOB '[0-9][0-9][0-9][0-9][0-9]'
        ),
    ville            TEXT    NOT NULL,
    date_naissance   TEXT    NOT NULL
        CHECK ( date(date_naissance) IS NOT NULL ),
    credit_disponible REAL   NOT NULL
        CHECK (credit_disponible >= 0),
    bon_client       INTEGER NOT NULL DEFAULT 0
        CHECK (bon_client IN (0, 1)),
    couleur_cheveux  TEXT    NOT NULL
        CHECK (
            couleur_cheveux IN ('brun', 'blond', 'roux', 'chauve')
        )
);
"""


class GestionnaireBase:
    """
    Gère la connexion unique à une base de données SQLite.

    Usage :
        db = GestionnaireBase()
        db.ouvrir("/chemin/vers/base.sqlite")
        conn = db.connexion          # objet sqlite3.Connection
        db.fermer()
    """

    def __init__(self) -> None:
        self._connexion: sqlite3.Connection | None = None
        self._chemin_base: str = ""

    # ------------------------------------------------------------------
    # Propriétés
    # ------------------------------------------------------------------

    @property
    def connexion(self) -> sqlite3.Connection | None:
        """Retourne l'objet connexion actif, ou None si non connecté."""
        return self._connexion

    @property
    def est_connecte(self) -> bool:
        """Indique si une connexion est active."""
        return self._connexion is not None

    @property
    def chemin_base(self) -> str:
        """Retourne le chemin du fichier SQLite ouvert."""
        return self._chemin_base

    # ------------------------------------------------------------------
    # Méthodes publiques
    # ------------------------------------------------------------------

    def ouvrir(self, chemin: str) -> bool:
        """
        Ouvre (ou crée) une base de données SQLite.

        :param chemin: Chemin complet vers le fichier .sqlite
        :return: True si la connexion est établie, False sinon
        """
        # Fermer toute connexion existante avant d'en ouvrir une nouvelle
        if self.est_connecte:
            self.fermer()

        try:
            self._connexion = sqlite3.connect(chemin)
            # Retourner les lignes sous forme de dict-like (sqlite3.Row)
            self._connexion.row_factory = sqlite3.Row
            # Activer les contraintes de clés étrangères
            self._connexion.execute("PRAGMA foreign_keys = ON;")
            self._chemin_base = chemin
            # S'assurer que la table Clients existe
            self._initialiser_tables()
            return True
        except sqlite3.Error as erreur:
            messagebox.showerror(
                "Erreur de connexion",
                f"Impossible d'ouvrir la base de données :\n{erreur}"
            )
            self._connexion = None
            self._chemin_base = ""
            return False

    def creer(self, chemin: str) -> bool:
        """
        Crée un nouveau fichier SQLite et y initialise la table Clients.

        :param chemin: Chemin complet vers le fichier .sqlite à créer
        :return: True si la création a réussi, False sinon
        """
        # Si le fichier existe déjà, on l'ouvre simplement
        return self.ouvrir(chemin)

    def fermer(self) -> None:
        """Ferme proprement la connexion à la base de données."""
        if self._connexion is not None:
            try:
                self._connexion.commit()
                self._connexion.close()
            except sqlite3.Error as erreur:
                messagebox.showerror(
                    "Erreur de fermeture",
                    f"Erreur lors de la fermeture de la base :\n{erreur}"
                )
            finally:
                self._connexion = None
                self._chemin_base = ""

    def executer(
        self,
        requete: str,
        parametres: tuple = ()
    ) -> sqlite3.Cursor | None:
        """
        Exécute une requête SQL (INSERT, UPDATE, DELETE).

        :param requete:    Requête SQL avec marqueurs « ? »
        :param parametres: Tuple de valeurs à substituer
        :return: Cursor si succès, None sinon
        """
        if not self.est_connecte:
            messagebox.showerror(
                "Erreur",
                "Aucune connexion à la base de données."
            )
            return None

        try:
            curseur = self._connexion.cursor()
            curseur.execute(requete, parametres)
            self._connexion.commit()
            return curseur
        except sqlite3.IntegrityError as erreur:
            messagebox.showerror(
                "Erreur d'intégrité",
                f"Contrainte de base de données violée :\n{erreur}"
            )
            return None
        except sqlite3.Error as erreur:
            messagebox.showerror(
                "Erreur SQL",
                f"Erreur lors de l'exécution de la requête :\n{erreur}"
            )
            return None

    def interroger(
        self,
        requete: str,
        parametres: tuple = ()
    ) -> list[sqlite3.Row]:
        """
        Exécute une requête SELECT et retourne les résultats.

        :param requete:    Requête SQL SELECT avec marqueurs « ? »
        :param parametres: Tuple de valeurs à substituer
        :return: Liste de sqlite3.Row (accès par nom de colonne)
        """
        if not self.est_connecte:
            messagebox.showerror(
                "Erreur",
                "Aucune connexion à la base de données."
            )
            return []

        try:
            curseur = self._connexion.cursor()
            curseur.execute(requete, parametres)
            return curseur.fetchall()
        except sqlite3.Error as erreur:
            messagebox.showerror(
                "Erreur SQL",
                f"Erreur lors de la requête :\n{erreur}"
            )
            return []

    # ------------------------------------------------------------------
    # Méthodes privées
    # ------------------------------------------------------------------

    def _initialiser_tables(self) -> None:
        """Crée la table Clients si elle n'existe pas encore."""
        try:
            self._connexion.executescript(SQL_CREATE_TABLE_CLIENTS)
            self._connexion.commit()
        except sqlite3.Error as erreur:
            messagebox.showerror(
                "Erreur d'initialisation",
                f"Impossible de créer la table Clients :\n{erreur}"
            )

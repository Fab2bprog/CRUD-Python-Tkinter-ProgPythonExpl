# =============================================================================
# controllers/bienvenue_controller.py
# Contrôleur de la fenêtre principale Win_Bienvenue_Main.
# Orchestre la logique métier : gestion de la connexion à la base SQLite,
# activation/désactivation des menus, et coordination avec les autres fenêtres.
# =============================================================================

from __future__ import annotations

import os
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from core.config import DB_EXTENSION, MODE_SELECTION_SIMPLE, MODE_SELECTION_MULTI
from core.database import GestionnaireBase

if TYPE_CHECKING:
    # Import conditionnel pour éviter les imports circulaires
    from views.Win_Bienvenue_Main import FenetreBienvenue


class BienvenueController:
    """
    Contrôleur associé à FenetreBienvenue (Win_Bienvenue_Main).

    Responsabilités :
      - Créer / ouvrir / fermer la base de données SQLite
      - Mettre à jour l'état des menus en conséquence
      - Ouvrir les fenêtres filles (Win_Client_CRUDS)
      - Recevoir et afficher les valeurs retournées par les sélections
    """

    def __init__(self, vue: "FenetreBienvenue") -> None:
        """
        :param vue: Référence à la fenêtre principale (FenetreBienvenue)
        """
        self._vue = vue
        self._db  = GestionnaireBase()

    # ------------------------------------------------------------------
    # Propriétés
    # ------------------------------------------------------------------

    @property
    def db(self) -> GestionnaireBase:
        """Expose le gestionnaire de base pour les fenêtres filles."""
        return self._db

    # ------------------------------------------------------------------
    # Gestion de la base de données
    # ------------------------------------------------------------------

    def creer_base(self) -> None:
        """
        Ouvre un sélecteur de fichier pour créer une nouvelle base SQLite,
        puis établit la connexion.
        """
        chemin = filedialog.asksaveasfilename(
            title="Créer une base de données",
            defaultextension=DB_EXTENSION,
            filetypes=[("Base SQLite", f"*{DB_EXTENSION}"), ("Tous les fichiers", "*.*")],
        )
        if not chemin:
            return  # L'utilisateur a annulé

        if self._db.creer(chemin):
            self._vue.on_base_ouverte(os.path.basename(chemin))

    def ouvrir_base(self) -> None:
        """
        Ouvre un sélecteur de fichier pour choisir une base SQLite existante,
        puis établit la connexion.
        """
        chemin = filedialog.askopenfilename(
            title="Ouvrir une base de données",
            filetypes=[("Base SQLite", f"*{DB_EXTENSION}"), ("Tous les fichiers", "*.*")],
        )
        if not chemin:
            return  # L'utilisateur a annulé

        if not os.path.isfile(chemin):
            messagebox.showerror("Fichier introuvable", f"Le fichier sélectionné est introuvable :\n{chemin}")
            return

        if self._db.ouvrir(chemin):
            self._vue.on_base_ouverte(os.path.basename(chemin))

    def fermer_base(self) -> None:
        """Ferme proprement la connexion SQLite et notifie la vue."""
        self._db.fermer()
        self._vue.on_base_fermee()

    def quitter_programme(self) -> None:
        """Ferme la connexion SQLite et termine l'application."""
        if self._db.est_connecte:
            self._db.fermer()
        self._vue.destroy()

    # ------------------------------------------------------------------
    # Ouverture des fenêtres d'action
    # ------------------------------------------------------------------

    def ouvrir_gestion_clients(self) -> None:
        """Ouvre Win_Client_CRUDS en mode standard (CRUD complet)."""
        from views.Win_Client_CRUDS import FenetreCRUDS
        FenetreCRUDS(self._vue, self._db, mode="STD")

    def ouvrir_selection_simple(self) -> None:
        """
        Ouvre Win_Client_CRUDS en mode sélection simple (S1).
        Le résultat (tuple id, nom) est affiché dans la console.
        """
        from views.Win_Client_CRUDS import FenetreCRUDS
        fenetre = FenetreCRUDS(self._vue, self._db, mode=MODE_SELECTION_SIMPLE)
        self._vue.wait_window(fenetre)
        resultat = fenetre.resultat_selection
        if resultat:
            print(f"[Sélection simple] Client sélectionné : {resultat}")
            self._vue.afficher_resultat_selection(resultat)

    def ouvrir_selection_multiple(self) -> None:
        """
        Ouvre Win_Client_CRUDS en mode sélection multiple (SX).
        La liste de résultats est affichée dans la console.
        """
        from views.Win_Client_CRUDS import FenetreCRUDS
        fenetre = FenetreCRUDS(self._vue, self._db, mode=MODE_SELECTION_MULTI)
        self._vue.wait_window(fenetre)
        resultats = fenetre.resultat_selection
        if resultats:
            print(f"[Sélection multiple] Clients sélectionnés : {resultats}")
            self._vue.afficher_resultat_selection(resultats)

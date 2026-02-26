# =============================================================================
# controllers/cruds_controller.py
# Contrôleur de la fenêtre Win_Client_CRUDS.
# Gère la logique métier : recherche, suppression, et coordination
# avec la fenêtre fiche client (Win_Client_Fiche).
# =============================================================================

from __future__ import annotations

from tkinter import messagebox
from typing import TYPE_CHECKING

from core.config import MODE_LECTURE, MODE_MODIFICATION
from core.database import GestionnaireBase
from models.client_model import Client, ClientDAO

if TYPE_CHECKING:
    from views.Win_Client_CRUDS import FenetreCRUDS


class CRUDSController:
    """
    Contrôleur associé à FenetreCRUDS (Win_Client_CRUDS).

    Responsabilités :
      - Charger et filtrer la liste des clients
      - Ouvrir Win_Client_Fiche en mode création, modification ou lecture
      - Supprimer un ou plusieurs enregistrements
      - Retourner la sélection en mode S1/SX
    """

    def __init__(self, vue: "FenetreCRUDS", db: GestionnaireBase) -> None:
        """
        :param vue: Référence à FenetreCRUDS
        :param db:  Gestionnaire de base déjà connecté
        """
        self._vue = vue
        self._db  = db

    # ------------------------------------------------------------------
    # Recherche / chargement
    # ------------------------------------------------------------------

    def rechercher(self, nom: str = "") -> list[Client]:
        """
        Recherche des clients par nom partiel.

        :param nom: Chaîne de recherche (vide = tous les clients)
        :return:    Liste de clients correspondants
        """
        return ClientDAO.rechercher(self._db, nom)

    # ------------------------------------------------------------------
    # Ouverture de la fiche client
    # ------------------------------------------------------------------

    def ajouter_client(self) -> None:
        """Ouvre Win_Client_Fiche en mode création (enregistrement vierge)."""
        from views.Win_Client_Fiche import FenetreFiche
        fenetre = FenetreFiche(
            parent=self._vue,
            db=self._db,
            mode=MODE_MODIFICATION,
            client=None,
        )
        self._vue.wait_window(fenetre)
        if fenetre.modifications_effectuees:
            self._vue.rafraichir_tableau()

    def modifier_client(self, client: Client) -> None:
        """
        Ouvre Win_Client_Fiche en mode modification pour l'enregistrement donné.

        :param client: Objet Client à modifier
        """
        from views.Win_Client_Fiche import FenetreFiche
        fenetre = FenetreFiche(
            parent=self._vue,
            db=self._db,
            mode=MODE_MODIFICATION,
            client=client,
        )
        self._vue.wait_window(fenetre)
        if fenetre.modifications_effectuees:
            self._vue.rafraichir_tableau()

    def consulter_client(self, client: Client) -> None:
        """
        Ouvre Win_Client_Fiche en lecture seule pour l'enregistrement donné.

        :param client: Objet Client à consulter
        """
        from views.Win_Client_Fiche import FenetreFiche
        FenetreFiche(
            parent=self._vue,
            db=self._db,
            mode=MODE_LECTURE,
            client=client,
        )

    # ------------------------------------------------------------------
    # Suppression
    # ------------------------------------------------------------------

    def supprimer_clients(self, ids: list[int]) -> bool:
        """
        Supprime un ou plusieurs clients après confirmation.

        :param ids: Liste des IDCLIENT à supprimer
        :return:    True si la suppression a été effectuée
        """
        if not ids:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner au moins un client à supprimer."
            )
            return False

        nb = len(ids)
        libelle = "ce client" if nb == 1 else f"ces {nb} clients"

        # Relâcher le grab modal le temps de la confirmation,
        # sinon la messagebox s'ouvre en arrière-plan et l'utilisateur
        # reste bloqué sans voir la fenêtre de confirmation.
        self._vue.grab_release()
        confirmation = messagebox.askyesno(
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer {libelle} ?\n"
            "Cette opération est irréversible.",
            icon="warning",
            parent=self._vue,
        )
        self._vue.grab_set()  # Reprendre le grab après la confirmation

        if not confirmation:
            return False

        succes = ClientDAO.supprimer_plusieurs(self._db, ids)
        if succes:
            self._vue.rafraichir_tableau()
        return succes

    # ------------------------------------------------------------------
    # Sélection (modes S1 / SX)
    # ------------------------------------------------------------------

    def valider_selection(self, clients: list[Client]) -> None:
        """
        Transmet la sélection à la fenêtre et la ferme.

        :param clients: Liste des clients sélectionnés
        """
        self._vue.retourner_selection(clients)

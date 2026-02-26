# =============================================================================
# controllers/fiche_controller.py
# Contrôleur de la fenêtre Win_Client_Fiche.
# Gère la logique métier : validation des champs, création et modification
# d'un enregistrement client dans la base SQLite.
# =============================================================================

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from core.database import GestionnaireBase
from models.client_model import Client, ClientDAO

if TYPE_CHECKING:
    from views.Win_Client_Fiche import FenetreFiche


class FicheController:
    """
    Contrôleur associé à FenetreFiche (Win_Client_Fiche).

    Responsabilités :
      - Valider l'ensemble des champs du formulaire
      - Créer un nouvel enregistrement (INSERT)
      - Mettre à jour un enregistrement existant (UPDATE)
    """

    def __init__(self, vue: "FenetreFiche", db: GestionnaireBase) -> None:
        """
        :param vue: Référence à FenetreFiche
        :param db:  Gestionnaire de base déjà connecté
        """
        self._vue = vue
        self._db  = db

    # ------------------------------------------------------------------
    # Validation des champs
    # ------------------------------------------------------------------

    def valider_champs(self, donnees: dict) -> tuple[bool, list[str]]:
        """
        Valide l'ensemble des données du formulaire.

        :param donnees: Dictionnaire {nom_champ: valeur}
        :return:        (True, []) si tout est valide,
                        (False, [liste d'erreurs]) sinon
        """
        erreurs: list[str] = []

        # Nom client
        if not donnees.get("nom_client", "").strip():
            erreurs.append("Le nom du client est obligatoire.")

        # Numéro de téléphone (non vide)
        if not donnees.get("numero_telephone", "").strip():
            erreurs.append("Le numéro de téléphone est obligatoire.")

        # Adresse
        if not donnees.get("adresse", "").strip():
            erreurs.append("L'adresse est obligatoire.")

        # Code postal : exactement 5 chiffres
        cp = donnees.get("code_postal", "")
        if not re.fullmatch(r"\d{5}", cp):
            erreurs.append("Le code postal doit contenir exactement 5 chiffres.")

        # Ville
        if not donnees.get("ville", "").strip():
            erreurs.append("La ville est obligatoire.")

        # Date de naissance : format JJ/MM/AAAA convertible en YYYY-MM-DD
        date_str = donnees.get("date_naissance", "")
        if not self._valider_date(date_str):
            erreurs.append("La date de naissance est invalide (format attendu : JJ/MM/AAAA).")

        # Crédit disponible : nombre décimal >= 0
        credit_str = donnees.get("credit_disponible", "0")
        try:
            credit = float(str(credit_str).replace(",", "."))
            if credit < 0:
                erreurs.append("Le crédit disponible doit être supérieur ou égal à 0.")
        except ValueError:
            erreurs.append("Le crédit disponible doit être un nombre décimal valide.")

        # Couleur des cheveux
        couleurs_valides = ["brun", "blond", "roux", "chauve"]
        if donnees.get("couleur_cheveux", "") not in couleurs_valides:
            erreurs.append(f"La couleur des cheveux doit être : {', '.join(couleurs_valides)}.")

        return (len(erreurs) == 0, erreurs)

    # ------------------------------------------------------------------
    # Enregistrement
    # ------------------------------------------------------------------

    def enregistrer(self, donnees: dict, client_existant: Optional[Client] = None) -> bool:
        """
        Valide puis crée ou met à jour un enregistrement client.

        :param donnees:          Dictionnaire des valeurs saisies dans le formulaire
        :param client_existant:  Client à modifier (None = création)
        :return:                 True si l'opération a réussi
        """
        valide, erreurs = self.valider_champs(donnees)
        if not valide:
            # Afficher le résumé des erreurs dans la vue
            self._vue.afficher_erreurs(erreurs)
            return False

        # Construire l'objet Client à partir des données validées
        client = self._construire_client(donnees, client_existant)

        if client_existant is None:
            # Création d'un nouvel enregistrement
            nouvel_id = ClientDAO.creer(self._db, client)
            succes = nouvel_id is not None
        else:
            # Mise à jour d'un enregistrement existant
            succes = ClientDAO.modifier(self._db, client)

        if succes:
            self._vue.on_enregistrement_reussi()
        return succes

    # ------------------------------------------------------------------
    # Méthodes privées
    # ------------------------------------------------------------------

    @staticmethod
    def _valider_date(date_str: str) -> bool:
        """
        Vérifie que la chaîne est une date valide au format JJ/MM/AAAA.

        :param date_str: Chaîne à vérifier
        :return:         True si la date est valide
        """
        try:
            datetime.strptime(date_str.strip(), "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def convertir_date_vers_iso(date_jma: str) -> str:
        """
        Convertit une date JJ/MM/AAAA en format ISO YYYY-MM-DD.

        :param date_jma: Date au format JJ/MM/AAAA
        :return:         Date au format YYYY-MM-DD
        """
        dt = datetime.strptime(date_jma.strip(), "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def convertir_date_vers_affichage(date_iso: str) -> str:
        """
        Convertit une date ISO YYYY-MM-DD en format affichage JJ/MM/AAAA.

        :param date_iso: Date au format YYYY-MM-DD
        :return:         Date au format JJ/MM/AAAA
        """
        try:
            dt = datetime.strptime(date_iso.strip(), "%Y-%m-%d")
            return dt.strftime("%d/%m/%Y")
        except ValueError:
            return date_iso  # Retourner tel quel si la conversion échoue

    def _construire_client(
        self,
        donnees: dict,
        client_existant: Optional[Client]
    ) -> Client:
        """
        Construit un objet Client à partir des données du formulaire.

        :param donnees:         Dictionnaire des valeurs saisies
        :param client_existant: Client original (pour conserver l'IDCLIENT)
        :return:                Objet Client prêt à être persisté
        """
        credit = float(str(donnees["credit_disponible"]).replace(",", "."))
        date_iso = self.convertir_date_vers_iso(donnees["date_naissance"])

        return Client(
            idclient          = client_existant.idclient if client_existant else None,
            nom_client        = donnees["nom_client"].strip(),
            numero_telephone  = donnees["numero_telephone"].strip(),
            adresse           = donnees["adresse"].strip(),
            code_postal       = donnees["code_postal"].strip(),
            ville             = donnees["ville"].strip(),
            date_naissance    = date_iso,
            credit_disponible = credit,
            bon_client        = bool(donnees.get("bon_client", False)),
            couleur_cheveux   = donnees["couleur_cheveux"],
        )

    # ------------------------------------------------------------------
    # Validation temps réel (utilisées par les validatecommand Tkinter)
    # ------------------------------------------------------------------

    @staticmethod
    def valider_code_postal_rt(valeur: str) -> bool:
        """
        Validation temps réel du code postal : max 5 chiffres uniquement.

        :param valeur: Valeur courante du champ
        :return:       True si la valeur est acceptable (saisie en cours)
        """
        return valeur == "" or (valeur.isdigit() and len(valeur) <= 5)

    @staticmethod
    def valider_credit_rt(valeur: str) -> bool:
        """
        Validation temps réel du crédit : format décimal accepté.

        :param valeur: Valeur courante du champ
        :return:       True si la valeur est acceptable (saisie en cours)
        """
        if valeur in ("", "-", "+"):
            return True
        try:
            float(valeur.replace(",", "."))
            return True
        except ValueError:
            return False

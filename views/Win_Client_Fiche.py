# =============================================================================
# views/Win_Client_Fiche.py
# Fenêtre de fiche client : Win_Client_Fiche
# Titre affiché : "Fiche Client"
#
# Cette fenêtre est modale (Toplevel + grab_set).
# Elle s'ouvre en 2 modes via le flag passé au constructeur :
#   - MODE_LECTURE (L)      : lecture seule, aucune modification possible
#   - MODE_MODIFICATION (M) : saisie et enregistrement possibles
# =============================================================================

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from core.config import COULEURS, POLICES, FENETRES, MODE_LECTURE, COULEURS_CHEVEUX
from core.database import GestionnaireBase
from classes.base_window import FenetreBase
from controllers.fiche_controller import FicheController
from models.client_model import Client
from fonctionsgen.fonctionsgen import formater_date_affichage


class FenetreFiche(FenetreBase):
    """
    Fenêtre de consultation / modification d'une fiche client.

    Affiche tous les champs de la table Clients avec :
      - Validation temps réel (validatecommand) sur code postal et crédit
      - Validation globale à la soumission (bouton Valider)
      - Affichage des erreurs dans une zone dédiée
    """

    def __init__(
        self,
        parent: tk.Widget,
        db: GestionnaireBase,
        mode: str,
        client: Optional[Client],
    ) -> None:
        cfg = FENETRES["fiche"]
        super().__init__(
            parent,
            titre=cfg["titre"],
            largeur=cfg["largeur"],
            hauteur=cfg["hauteur"],
            min_largeur=cfg["min_largeur"],
            min_hauteur=cfg["min_hauteur"],
        )

        self._mode   = mode
        self._db     = db
        self._client = client
        self._ctrl   = FicheController(self, db)

        self.modifications_effectuees: bool = False

        self._var_nom        = tk.StringVar()
        self._var_telephone  = tk.StringVar()
        self._var_adresse    = tk.StringVar()
        self._var_cp         = tk.StringVar()
        self._var_ville      = tk.StringVar()
        self._var_date       = tk.StringVar()
        self._var_credit     = tk.StringVar(value="0.00")
        self._var_bon_client = tk.BooleanVar(value=False)
        self._var_cheveux    = tk.StringVar(value=COULEURS_CHEVEUX[0])

        self._construire_interface()

        if client:
            self._remplir_champs(client)

        if mode == MODE_LECTURE:
            self._desactiver_champs()

        # Mémoriser l'état initial des champs pour détecter les modifications
        # (uniquement utile en mode modification/création)
        self._etat_initial = self._lire_etat_champs()

        # Touche Echap : tenter une fermeture avec confirmation si nécessaire
        self.bind("<Escape>", lambda _e: self._on_fermeture())

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _construire_interface(self) -> None:
        """Construit le formulaire et la barre de boutons."""

        cadre = tk.Frame(self, bg=COULEURS["fond_principal"], padx=15, pady=10)
        cadre.pack(fill=tk.BOTH, expand=True)
        cadre.columnconfigure(1, weight=1)

        # Titre du mode
        if self._mode == MODE_LECTURE:
            libelle_mode = "Consultation (lecture seule)"
        elif self._client is None:
            libelle_mode = "Nouveau client"
        else:
            libelle_mode = "Modification client"

        tk.Label(
            cadre,
            text=libelle_mode,
            font=POLICES["sous_titre"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 12))

        # Validations temps réel
        vcmd_cp     = (self.register(self._ctrl.valider_code_postal_rt), "%P")
        vcmd_credit = (self.register(self._ctrl.valider_credit_rt),      "%P")

        self._champs_widgets: list[tk.Widget] = []
        self._ligne = 1

        def ajouter_champ(libelle: str, widget: tk.Widget) -> None:
            tk.Label(
                cadre,
                text=libelle,
                font=POLICES["normale"],
                bg=COULEURS["fond_principal"],
                fg=COULEURS["texte_principal"],
                anchor=tk.E,
                width=16,
            ).grid(row=self._ligne, column=0, sticky=tk.E, pady=4, padx=(0, 8))
            widget.grid(row=self._ligne, column=1, sticky=tk.EW, pady=4)
            self._champs_widgets.append(widget)
            self._ligne += 1

        # Nom client
        self._entry_nom = ttk.Entry(cadre, textvariable=self._var_nom)
        ajouter_champ("Nom client :", self._entry_nom)

        # Telephone
        self._entry_tel = ttk.Entry(cadre, textvariable=self._var_telephone)
        ajouter_champ("Telephone :", self._entry_tel)

        # Adresse
        self._entry_adresse = ttk.Entry(cadre, textvariable=self._var_adresse)
        ajouter_champ("Adresse :", self._entry_adresse)

        # Code postal
        self._entry_cp = ttk.Entry(
            cadre,
            textvariable=self._var_cp,
            validate="key",
            validatecommand=vcmd_cp,
            width=8,
        )
        ajouter_champ("Code postal :", self._entry_cp)

        # Ville
        self._entry_ville = ttk.Entry(cadre, textvariable=self._var_ville)
        ajouter_champ("Ville :", self._entry_ville)

        # Date de naissance
        cadre_date = tk.Frame(cadre, bg=COULEURS["fond_principal"])
        self._entry_date = ttk.Entry(cadre_date, textvariable=self._var_date, width=12)
        self._entry_date.pack(side=tk.LEFT)
        tk.Label(
            cadre_date,
            text=" (JJ/MM/AAAA)",
            font=POLICES["petite"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(side=tk.LEFT)
        ajouter_champ("Date naissance :", cadre_date)
        self._champs_widgets.append(self._entry_date)

        # Credit disponible
        cadre_credit = tk.Frame(cadre, bg=COULEURS["fond_principal"])
        self._entry_credit = ttk.Entry(
            cadre_credit,
            textvariable=self._var_credit,
            validate="key",
            validatecommand=vcmd_credit,
            width=12,
        )
        self._entry_credit.pack(side=tk.LEFT)
        tk.Label(
            cadre_credit,
            text=" euros",
            font=POLICES["normale"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(side=tk.LEFT)
        ajouter_champ("Credit disponible :", cadre_credit)
        self._champs_widgets.append(self._entry_credit)

        # Bon client
        self._check_bon = ttk.Checkbutton(
            cadre,
            text="Oui",
            variable=self._var_bon_client,
        )
        ajouter_champ("Bon client :", self._check_bon)

        # Couleur des cheveux
        self._combo_cheveux = ttk.Combobox(
            cadre,
            textvariable=self._var_cheveux,
            values=COULEURS_CHEVEUX,
            state="readonly",
            width=12,
        )
        ajouter_champ("Couleur cheveux :", self._combo_cheveux)
        self._champs_widgets.append(self._combo_cheveux)

        # Separateur
        ttk.Separator(cadre, orient=tk.HORIZONTAL).grid(
            row=self._ligne, column=0, columnspan=2, sticky=tk.EW, pady=10
        )
        self._ligne += 1

        # Zone d'erreurs (masquee initialement)
        self._cadre_erreurs = tk.Frame(cadre, bg="#FADBD8", bd=1, relief=tk.SOLID)
        self._lbl_erreurs = tk.Label(
            self._cadre_erreurs,
            text="",
            font=POLICES["petite"],
            bg="#FADBD8",
            fg=COULEURS["texte_erreur"],
            justify=tk.LEFT,
            wraplength=380,
        )
        self._lbl_erreurs.pack(padx=8, pady=6)
        self._cadre_erreurs.grid(
            row=self._ligne, column=0, columnspan=2, sticky=tk.EW, pady=(0, 8)
        )
        self._cadre_erreurs.grid_remove()
        self._ligne += 1

        # Boutons
        cadre_boutons = tk.Frame(cadre, bg=COULEURS["fond_principal"])
        cadre_boutons.grid(row=self._ligne, column=0, columnspan=2, pady=5)

        if self._mode != MODE_LECTURE:
            photo_save = self.charger_image("Base_save.png")
            btn_valider = tk.Button(
                cadre_boutons,
                text="  Valider",
                image=photo_save,
                compound=tk.LEFT,
                font=POLICES["normale"],
                bg=COULEURS["fond_bouton"],
                fg=COULEURS["texte_clair"],
                activebackground=COULEURS["fond_bouton_hover"],
                relief=tk.FLAT,
                padx=12, pady=6,
                cursor="hand2",
                command=self._on_valider,
            )
            btn_valider.pack(side=tk.LEFT, padx=8)

        photo_exit = self.charger_image("zone_exit.png")
        libelle_annuler = "Fermer" if self._mode == MODE_LECTURE else "Annuler"
        btn_annuler = tk.Button(
            cadre_boutons,
            text="  " + libelle_annuler,
            image=photo_exit,
            compound=tk.LEFT,
            font=POLICES["normale"],
            bg=COULEURS["fond_bouton_exit"],
            fg=COULEURS["texte_clair"],
            activebackground="#C0392B",
            relief=tk.FLAT,
            padx=12, pady=6,
            cursor="hand2",
            command=self._on_fermeture,
        )
        btn_annuler.pack(side=tk.LEFT, padx=8)

    # ------------------------------------------------------------------
    # Pré-remplissage et désactivation
    # ------------------------------------------------------------------

    def _remplir_champs(self, client: Client) -> None:
        """Pré-remplit tous les champs avec les données du client."""
        self._var_nom.set(client.nom_client)
        self._var_telephone.set(client.numero_telephone)
        self._var_adresse.set(client.adresse)
        self._var_cp.set(client.code_postal)
        self._var_ville.set(client.ville)
        self._var_date.set(formater_date_affichage(client.date_naissance))
        self._var_credit.set(f"{client.credit_disponible:.2f}")
        self._var_bon_client.set(client.bon_client)
        self._var_cheveux.set(client.couleur_cheveux)

    def _desactiver_champs(self) -> None:
        """Désactive tous les widgets de saisie (mode lecture seule)."""
        for widget in self._champs_widgets:
            try:
                widget.configure(state=tk.DISABLED)
            except tk.TclError:
                pass

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def _on_fermeture(self) -> None:
        """
        Surcharge de FenetreBase._on_fermeture.
        En mode modification ou création : demande confirmation si des
        champs ont été modifiés depuis l'ouverture de la fenêtre.
        En mode lecture : fermeture directe sans confirmation.
        """
        if self._mode != MODE_LECTURE and self._champs_modifies():
            self.grab_release()
            reponse = tk.messagebox.askyesno(
                "Confirmation",
                "Des modifications ont été effectuées.\nVoulez-vous vraiment quitter sans enregistrer ?",
                icon="warning",
                parent=self,
            )
            self.grab_set()
            if not reponse:
                return  # L'utilisateur annule la fermeture
        self.grab_release()
        self.destroy()

    def _lire_etat_champs(self) -> dict:
        """Retourne un instantané des valeurs actuelles de tous les champs."""
        return {
            "nom"        : self._var_nom.get(),
            "telephone"  : self._var_telephone.get(),
            "adresse"    : self._var_adresse.get(),
            "cp"         : self._var_cp.get(),
            "ville"      : self._var_ville.get(),
            "date"       : self._var_date.get(),
            "credit"     : self._var_credit.get(),
            "bon_client" : self._var_bon_client.get(),
            "cheveux"    : self._var_cheveux.get(),
        }

    def _champs_modifies(self) -> bool:
        """Retourne True si au moins un champ diffère de l'état initial."""
        return self._lire_etat_champs() != self._etat_initial

    def _on_valider(self) -> None:
        """Déclenché au clic sur le bouton Valider."""
        donnees = {
            "nom_client"        : self._var_nom.get(),
            "numero_telephone"  : self._var_telephone.get(),
            "adresse"           : self._var_adresse.get(),
            "code_postal"       : self._var_cp.get(),
            "ville"             : self._var_ville.get(),
            "date_naissance"    : self._var_date.get(),
            "credit_disponible" : self._var_credit.get(),
            "bon_client"        : self._var_bon_client.get(),
            "couleur_cheveux"   : self._var_cheveux.get(),
        }
        self._ctrl.enregistrer(donnees, self._client)

    # ------------------------------------------------------------------
    # Méthodes appelées par le contrôleur
    # ------------------------------------------------------------------

    def afficher_erreurs(self, erreurs: list[str]) -> None:
        """Affiche les erreurs de validation dans la zone dédiée."""
        if not erreurs:
            self._cadre_erreurs.grid_remove()
            return
        self._lbl_erreurs.configure(text="\n".join("- " + e for e in erreurs))
        self._cadre_erreurs.grid()

    def on_enregistrement_reussi(self) -> None:
        """Appelé par le contrôleur après un enregistrement réussi."""
        self.modifications_effectuees = True
        self._cadre_erreurs.grid_remove()
        self._on_fermeture()

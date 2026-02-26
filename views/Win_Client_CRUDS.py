# =============================================================================
# views/Win_Client_CRUDS.py
# Fenêtre de gestion des clients : Win_Client_CRUDS
# Titre affiché : "Opérations Possibles"
# =============================================================================

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from core.config import (
    COULEURS, POLICES, FENETRES, ICONE_TAILLE,
    MODE_STANDARD, MODE_SELECTION_SIMPLE, MODE_SELECTION_MULTI,
)
from core.database import GestionnaireBase
from classes.base_window import FenetreBase
from controllers.cruds_controller import CRUDSController
from fonctionsgen.fonctionsgen import formater_credit, formater_date_affichage, formater_booleen


# Colonnes affichées dans le tableau (nom_colonne, libellé, largeur_px)
COLONNES_TABLEAU = [
    ("IDCLIENT",          "ID",           50),
    ("nom_client",        "Nom",         180),
    ("numero_telephone",  "Telephone",   110),
    ("ville",             "Ville",       130),
    ("code_postal",       "CP",           60),
    ("date_naissance",    "Naissance",   100),
    ("credit_disponible", "Credit",       90),
    ("bon_client",        "Bon client",   80),
    ("couleur_cheveux",   "Cheveux",      80),
]


class FenetreCRUDS(FenetreBase):
    """
    Fenêtre principale de gestion des clients (CRUD + Recherche + Sélection).
    """

    def __init__(
        self,
        parent: tk.Widget,
        db: GestionnaireBase,
        mode: str = MODE_STANDARD,
    ) -> None:
        cfg = FENETRES["cruds"]
        super().__init__(
            parent,
            titre=cfg["titre"],
            largeur=cfg["largeur"],
            hauteur=cfg["hauteur"],
            min_largeur=cfg["min_largeur"],
            min_hauteur=cfg["min_hauteur"],
        )

        self._mode = mode
        self._db   = db
        self._ctrl = CRUDSController(self, db)

        self.resultat_selection = None
        self._images_boutons: dict[str, Optional[tk.PhotoImage]] = {}

        # Compteur de clics pour détecter le double-clic manuellement
        self._nb_clics = 0
        self._timer_double_clic = None

        self._construire_interface()
        self.rafraichir_tableau()

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _construire_interface(self) -> None:
        cadre_racine = tk.Frame(self, bg=COULEURS["fond_principal"])
        cadre_racine.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        cadre_racine.columnconfigure(0, weight=1)
        cadre_racine.rowconfigure(0, weight=1)

        self._construire_zone_principale(cadre_racine)
        self._construire_zone_boutons(cadre_racine)

    def _construire_zone_principale(self, parent: tk.Widget) -> None:
        cadre = tk.Frame(parent, bg=COULEURS["fond_principal"])
        cadre.grid(row=0, column=0, sticky=tk.NSEW, padx=(0, 5))
        cadre.rowconfigure(1, weight=1)
        cadre.columnconfigure(0, weight=1)

        # Champ de recherche
        cadre_recherche = tk.Frame(cadre, bg=COULEURS["fond_principal"])
        cadre_recherche.grid(row=0, column=0, sticky=tk.EW, pady=(0, 5))
        cadre_recherche.columnconfigure(1, weight=1)

        tk.Label(
            cadre_recherche,
            text="Rechercher :",
            font=POLICES["normale"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).grid(row=0, column=0, padx=(0, 8))

        self._var_recherche = tk.StringVar()
        self._var_recherche.trace_add("write", self._on_recherche_changee)

        champ_recherche = ttk.Entry(cadre_recherche, textvariable=self._var_recherche)
        champ_recherche.grid(row=0, column=1, sticky=tk.EW)
        champ_recherche.focus_set()

        # Tableau Treeview
        cadre_tableau = tk.Frame(cadre, bg=COULEURS["fond_principal"])
        cadre_tableau.grid(row=1, column=0, sticky=tk.NSEW)
        cadre_tableau.rowconfigure(0, weight=1)
        cadre_tableau.columnconfigure(0, weight=1)

        colonnes = [col[0] for col in COLONNES_TABLEAU]
        if self._mode == MODE_SELECTION_SIMPLE:
            selectmode = tk.BROWSE
        elif self._mode == MODE_SELECTION_MULTI:
            selectmode = tk.EXTENDED
        else:
            selectmode = tk.EXTENDED

        self._tableau = ttk.Treeview(
            cadre_tableau,
            columns=colonnes,
            show="headings",
            selectmode=selectmode,
        )

        for nom, libelle, largeur in COLONNES_TABLEAU:
            self._tableau.heading(nom, text=libelle, anchor=tk.W)
            self._tableau.column(nom, width=largeur, minwidth=40, anchor=tk.W)

        sb_v = ttk.Scrollbar(cadre_tableau, orient=tk.VERTICAL,   command=self._tableau.yview)
        sb_h = ttk.Scrollbar(cadre_tableau, orient=tk.HORIZONTAL, command=self._tableau.xview)
        self._tableau.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)

        self._tableau.grid(row=0, column=0, sticky=tk.NSEW)
        sb_v.grid(row=0, column=1, sticky=tk.NS)
        sb_h.grid(row=1, column=0, sticky=tk.EW)

        # ---------------------------------------------------------------
        # Gestion du double-clic : on utilise ButtonRelease-1 avec
        # un compteur de clics et un timer after().
        # ButtonRelease est déclenché APRES que le Treeview a mis à jour
        # sa sélection, ce qui évite tout problème de timing.
        # ---------------------------------------------------------------
        self._tableau.bind("<ButtonRelease-1>", self._on_clic_tableau)
        self._tableau.bind("<Return>",          self._on_entree)

        # Touche Echap : ferme la fenêtre
        self.bind("<Escape>", lambda _e: self._on_fermeture())

        self._tableau.tag_configure("pair",   background="#EBF5FB")
        self._tableau.tag_configure("impair", background=COULEURS["fond_secondaire"])

    def _construire_zone_boutons(self, parent: tk.Widget) -> None:
        cadre = tk.Frame(
            parent,
            bg=COULEURS["fond_barre"],
            width=ICONE_TAILLE + 20,
        )
        cadre.grid(row=0, column=1, sticky=tk.NS)
        cadre.pack_propagate(False)

        est_mode_selection = self._mode in (MODE_SELECTION_SIMPLE, MODE_SELECTION_MULTI)

        definitions_boutons = [
            ("Base_create.png", "Ajouter",      self._ctrl.ajouter_client,  True,  False),
            ("Base_update.png", "Modifier",      self._on_modifier,          True,  False),
            ("Base_delete.png", "Supprimer",     self._on_supprimer,         True,  False),
            ("Base_read.png",   "Consulter",     self._on_consulter,         True,  True),
            ("Base_search.png", "Rechercher",    self._on_rechercher,        True,  True),
            ("Base_select.png", "Selectionner",  self._on_selectionner,      False, True),
            ("zone_exit.png",   "Quitter",       self._on_fermeture,         True,  True),
        ]

        for nom_img, tooltip, commande, visible_crud, visible_sel in definitions_boutons:
            visible = visible_sel if est_mode_selection else visible_crud
            if not visible:
                continue
            self._creer_bouton_icone(cadre, nom_img, tooltip, commande)

    def _creer_bouton_icone(self, parent, nom_image, tooltip, commande):
        photo = self.charger_image(nom_image)
        btn_cfg = {
            "bg"              : COULEURS["fond_barre"],
            "activebackground": COULEURS["fond_bouton_hover"],
            "bd"              : 0,
            "relief"          : tk.FLAT,
            "cursor"          : "hand2",
            "width"           : ICONE_TAILLE + 10,
            "height"          : ICONE_TAILLE + 10,
            "command"         : commande,
        }
        if photo:
            btn = tk.Button(parent, image=photo, **btn_cfg)
        else:
            btn = tk.Button(parent, text=tooltip, font=POLICES["petite"],
                            fg=COULEURS["texte_clair"], **btn_cfg)
        btn.pack(pady=4, padx=5)
        self._ajouter_infobulle(btn, tooltip)
        return btn

    @staticmethod
    def _ajouter_infobulle(widget, texte):
        infobulle = []

        def afficher(event):
            tip = tk.Toplevel(widget)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")
            tk.Label(tip, text=texte, font=POLICES["petite"], bg="#FFFACD",
                     fg=COULEURS["texte_principal"], relief=tk.SOLID,
                     bd=1, padx=4, pady=2).pack()
            infobulle.append(tip)

        def masquer(_event):
            for tip in infobulle:
                tip.destroy()
            infobulle.clear()

        widget.bind("<Enter>", afficher)
        widget.bind("<Leave>", masquer)

    # ------------------------------------------------------------------
    # Rafraîchissement du tableau
    # ------------------------------------------------------------------

    def rafraichir_tableau(self, terme: str = "") -> None:
        for item in self._tableau.get_children():
            self._tableau.delete(item)

        clients = self._ctrl.rechercher(terme)

        for i, client in enumerate(clients):
            tag = "pair" if i % 2 == 0 else "impair"
            self._tableau.insert(
                "", tk.END,
                iid=str(client.idclient),
                values=(
                    client.idclient,
                    client.nom_client,
                    client.numero_telephone,
                    client.ville,
                    client.code_postal,
                    formater_date_affichage(client.date_naissance),
                    formater_credit(client.credit_disponible),
                    formater_booleen(client.bon_client),
                    client.couleur_cheveux,
                ),
                tags=(tag,),
            )

    # ------------------------------------------------------------------
    # Sélection dans le tableau
    # ------------------------------------------------------------------

    def _obtenir_clients_selectionnes(self) -> list:
        from models.client_model import ClientDAO
        clients = []
        for iid in self._tableau.selection():
            client = ClientDAO.lire(self._db, int(iid))
            if client:
                clients.append(client)
        return clients

    def _obtenir_client_selectionne_unique(self):
        clients = self._obtenir_clients_selectionnes()
        if not clients:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner un client dans le tableau.",
                parent=self,
            )
            return None
        return clients[0]

    # ------------------------------------------------------------------
    # Gestion du double-clic via compteur + after()
    # ------------------------------------------------------------------

    def _on_clic_tableau(self, event) -> None:
        """
        Détecte un simple ou double clic sur le tableau via un compteur.
        On utilise ButtonRelease-1 (et non Double-1) car à ce moment
        le Treeview a déjà mis à jour sa sélection interne.
        Un timer after(300ms) distingue simple clic et double-clic.
        """
        # Ignorer le clic si la ligne sous le curseur est vide
        iid = self._tableau.identify_row(event.y)
        if not iid:
            return

        self._nb_clics += 1

        if self._nb_clics == 1:
            # Premier clic : armer le timer
            self._timer_double_clic = self.after(300, self._executer_simple_clic)
        else:
            # Deuxième clic dans les 300ms : c'est un double-clic
            if self._timer_double_clic:
                self.after_cancel(self._timer_double_clic)
                self._timer_double_clic = None
            self._nb_clics = 0
            self._executer_double_clic()

    def _executer_simple_clic(self) -> None:
        """Exécuté après 300ms si aucun deuxième clic n'est survenu."""
        self._nb_clics = 0
        self._timer_double_clic = None
        # Le simple clic ne fait rien de spécial : la sélection est déjà
        # mise à jour par le Treeview lui-même.

    def _executer_double_clic(self) -> None:
        """
        Action sur double-clic :
        - Mode sélection : valide et ferme
        - Mode standard  : ouvre la fiche en modification
        """
        if not self._tableau.selection():
            return
        if self._mode in (MODE_SELECTION_SIMPLE, MODE_SELECTION_MULTI):
            self._on_selectionner()
        else:
            self._on_modifier()

    # ------------------------------------------------------------------
    # Callbacks des boutons
    # ------------------------------------------------------------------

    def _on_recherche_changee(self, *_args) -> None:
        self.rafraichir_tableau(self._var_recherche.get())

    def _on_entree(self, _event) -> None:
        """Touche Entrée : même action que le double-clic."""
        if not self._tableau.selection():
            return
        if self._mode in (MODE_SELECTION_SIMPLE, MODE_SELECTION_MULTI):
            self._on_selectionner()
        else:
            self._on_modifier()

    def _on_modifier(self) -> None:
        client = self._obtenir_client_selectionne_unique()
        if client:
            self._ctrl.modifier_client(client)

    def _on_supprimer(self) -> None:
        ids = [int(iid) for iid in self._tableau.selection()]
        self._ctrl.supprimer_clients(ids)

    def _on_consulter(self) -> None:
        client = self._obtenir_client_selectionne_unique()
        if client:
            self._ctrl.consulter_client(client)

    def _on_rechercher(self) -> None:
        self.rafraichir_tableau(self._var_recherche.get())

    def _on_selectionner(self) -> None:
        clients = self._obtenir_clients_selectionnes()
        if not clients:
            messagebox.showwarning(
                "Aucune sélection",
                "Veuillez sélectionner au moins un client.",
                parent=self,
            )
            return
        self._ctrl.valider_selection(clients)

    # ------------------------------------------------------------------
    # Retour de sélection (appelé par le contrôleur)
    # ------------------------------------------------------------------

    def retourner_selection(self, clients: list) -> None:
        if self._mode == MODE_SELECTION_SIMPLE:
            c = clients[0]
            self.resultat_selection = (c.idclient, c.nom_client)
        else:
            self.resultat_selection = [(c.idclient, c.nom_client) for c in clients]
        self._on_fermeture()

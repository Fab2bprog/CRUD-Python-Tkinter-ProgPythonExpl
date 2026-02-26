# =============================================================================
# views/Win_Bienvenue_Main.py
# Fenêtre principale de l'application : Win_Bienvenue_Main
# Titre affiché : "Bienvenue"
#
# Cette fenêtre est la racine Tk de l'application (hérite de tk.Tk
# et non de FenetreBase/Toplevel, car c'est la fenêtre principale).
# =============================================================================

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from core.config import COULEURS, POLICES, FENETRES
from classes.base_window import FenetreBase
from controllers.bienvenue_controller import BienvenueController


class FenetreBienvenue(tk.Tk):
    """
    Fenêtre principale de ProgPythonExpl.

    Elle gère :
      - Le menu déroulant « Fichier » (Créer/Ouvrir/Fermer base, Quitter)
      - Le menu déroulant « Actions » (Gestion clients, Sélections)
      - Une zone centrale affichant l'état de la connexion
      - Une zone de résultats pour les retours des sélections
    """

    def __init__(self) -> None:
        super().__init__()

        # Application du thème visuel ttk (une seule fois, ici)
        FenetreBase.appliquer_style_ttk()

        # Paramètres de la fenêtre
        cfg = FENETRES["bienvenue"]
        self.title(cfg["titre"])
        self.configure(bg=COULEURS["fond_principal"])
        self.geometry(f"{cfg['largeur']}x{cfg['hauteur']}")
        self.minsize(cfg["min_largeur"], cfg["min_hauteur"])
        self._centrer()

        # Contrôleur
        self._ctrl = BienvenueController(self)

        # Références aux menus (pour activer/désactiver les options)
        self._menu_fichier: tk.Menu | None = None
        self._menu_actions: tk.Menu | None = None

        # Construction de l'interface
        self._construire_menu()
        self._construire_interface()

        # Gestion de la fermeture via la croix
        self.protocol("WM_DELETE_WINDOW", self._ctrl.quitter_programme)

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------

    def _construire_menu(self) -> None:
        """Crée la barre de menus avec les menus Fichier et Actions."""
        barre = tk.Menu(self, bg=COULEURS["fond_principal"], fg=COULEURS["texte_principal"])
        self.config(menu=barre)

        # ── Menu Fichier ──────────────────────────────────────────────
        self._menu_fichier = tk.Menu(barre, tearoff=0, bg=COULEURS["fond_secondaire"])
        barre.add_cascade(label="Fichier", menu=self._menu_fichier)

        self._menu_fichier.add_command(
            label="Créer Base",
            command=self._ctrl.creer_base,
            state=tk.NORMAL,
        )
        self._menu_fichier.add_command(
            label="Ouvrir Base",
            command=self._ctrl.ouvrir_base,
            state=tk.NORMAL,
        )
        self._menu_fichier.add_command(
            label="Fermer Base",
            command=self._ctrl.fermer_base,
            state=tk.DISABLED,  # Inactif tant que aucune base n'est ouverte
        )
        self._menu_fichier.add_separator()
        self._menu_fichier.add_command(
            label="Quitter Programme",
            command=self._ctrl.quitter_programme,
        )

        # ── Menu Actions ──────────────────────────────────────────────
        self._menu_actions = tk.Menu(barre, tearoff=0, bg=COULEURS["fond_secondaire"])
        barre.add_cascade(
            label="Actions",
            menu=self._menu_actions,
            state=tk.DISABLED,  # Inactif tant que aucune base n'est ouverte
        )
        self._barre_menu = barre  # Conserver la référence pour activer Actions

        self._menu_actions.add_command(
            label="Gestion Clients",
            command=self._ctrl.ouvrir_gestion_clients,
        )
        self._menu_actions.add_command(
            label="Sélection d'un seul Client",
            command=self._ctrl.ouvrir_selection_simple,
        )
        self._menu_actions.add_command(
            label="Sélection de plusieurs Clients",
            command=self._ctrl.ouvrir_selection_multiple,
        )

    def _construire_interface(self) -> None:
        """Construit les widgets de la zone centrale de la fenêtre."""
        # ── Cadre principal ───────────────────────────────────────────
        cadre_principal = tk.Frame(self, bg=COULEURS["fond_principal"], padx=20, pady=20)
        cadre_principal.pack(fill=tk.BOTH, expand=True)

        # ── Titre de bienvenue ────────────────────────────────────────
        tk.Label(
            cadre_principal,
            text="ProgPythonExpl",
            font=POLICES["titre"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(pady=(20, 5))

        tk.Label(
            cadre_principal,
            text="Programme de démonstration CRUD – Table Clients SQLite",
            font=POLICES["normale"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(pady=(0, 30))

        # ── Séparateur ────────────────────────────────────────────────
        ttk.Separator(cadre_principal, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # ── Statut de la connexion ────────────────────────────────────
        cadre_statut = tk.Frame(cadre_principal, bg=COULEURS["fond_principal"])
        cadre_statut.pack(fill=tk.X, pady=15)

        tk.Label(
            cadre_statut,
            text="État de la connexion :",
            font=POLICES["sous_titre"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(side=tk.LEFT)

        self._lbl_statut = tk.Label(
            cadre_statut,
            text="Aucune base ouverte",
            font=POLICES["normale"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_erreur"],
        )
        self._lbl_statut.pack(side=tk.LEFT, padx=10)

        # ── Zone de résultats de sélection ────────────────────────────
        tk.Label(
            cadre_principal,
            text="Résultat de la dernière sélection :",
            font=POLICES["sous_titre"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
        ).pack(anchor=tk.W, pady=(20, 5))

        cadre_resultat = tk.Frame(
            cadre_principal,
            bg=COULEURS["fond_secondaire"],
            bd=1,
            relief=tk.SUNKEN,
        )
        cadre_resultat.pack(fill=tk.BOTH, expand=True)

        self._txt_resultat = tk.Text(
            cadre_resultat,
            font=POLICES["mono"],
            bg=COULEURS["fond_secondaire"],
            fg=COULEURS["texte_principal"],
            state=tk.DISABLED,
            wrap=tk.WORD,
            height=6,
        )
        scrollbar = ttk.Scrollbar(cadre_resultat, command=self._txt_resultat.yview)
        self._txt_resultat.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._txt_resultat.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ── Instructions ──────────────────────────────────────────────
        ttk.Separator(cadre_principal, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        tk.Label(
            cadre_principal,
            text="Utilisez le menu Fichier pour ouvrir une base de données, puis le menu Actions pour gérer les clients.",
            font=POLICES["petite"],
            bg=COULEURS["fond_principal"],
            fg=COULEURS["texte_principal"],
            wraplength=600,
            justify=tk.CENTER,
        ).pack()

    # ------------------------------------------------------------------
    # Méthodes appelées par le contrôleur (callbacks)
    # ------------------------------------------------------------------

    def on_base_ouverte(self, nom_fichier: str) -> None:
        """
        Met à jour l'interface après l'ouverture d'une base de données.

        :param nom_fichier: Nom du fichier SQLite ouvert (pour affichage)
        """
        # Mise à jour du label de statut
        self._lbl_statut.configure(
            text=f"Connecté : {nom_fichier}",
            fg="#27AE60",  # Vert – connexion active
        )

        # Activer "Fermer Base", désactiver "Ouvrir Base" et "Créer Base"
        self._menu_fichier.entryconfig("Créer Base",  state=tk.DISABLED)
        self._menu_fichier.entryconfig("Ouvrir Base", state=tk.DISABLED)
        self._menu_fichier.entryconfig("Fermer Base", state=tk.NORMAL)

        # Activer le menu Actions
        self._barre_menu.entryconfig("Actions", state=tk.NORMAL)

    def on_base_fermee(self) -> None:
        """Met à jour l'interface après la fermeture de la base."""
        self._lbl_statut.configure(
            text="Aucune base ouverte",
            fg=COULEURS["texte_erreur"],
        )

        # Rétablir l'état initial des menus
        self._menu_fichier.entryconfig("Créer Base",  state=tk.NORMAL)
        self._menu_fichier.entryconfig("Ouvrir Base", state=tk.NORMAL)
        self._menu_fichier.entryconfig("Fermer Base", state=tk.DISABLED)
        self._barre_menu.entryconfig("Actions",       state=tk.DISABLED)

    def afficher_resultat_selection(self, resultat) -> None:
        """
        Affiche le résultat d'une sélection dans la zone de texte.

        :param resultat: Tuple (id, nom) ou liste de tuples
        """
        self._txt_resultat.configure(state=tk.NORMAL)
        self._txt_resultat.delete("1.0", tk.END)

        if isinstance(resultat, list):
            for item in resultat:
                self._txt_resultat.insert(tk.END, f"{item}\n")
        else:
            self._txt_resultat.insert(tk.END, str(resultat))

        self._txt_resultat.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # Utilitaires
    # ------------------------------------------------------------------

    def _centrer(self) -> None:
        """Centre la fenêtre principale sur l'écran."""
        self.update_idletasks()
        cfg = FENETRES["bienvenue"]
        x = (self.winfo_screenwidth()  - cfg["largeur"])  // 2
        y = (self.winfo_screenheight() - cfg["hauteur"]) // 2
        self.geometry(f"{cfg['largeur']}x{cfg['hauteur']}+{x}+{y}")

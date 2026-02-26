# =============================================================================
# main.py
# Point d'entrée de l'application ProgPythonExpl.
#
# Ce fichier est le seul à exécuter pour lancer le programme :
#   python main.py
#
# Il configure le chemin Python (sys.path) pour que les imports relatifs
# fonctionnent correctement depuis n'importe quel répertoire de travail,
# puis instancie et lance la fenêtre principale.
# =============================================================================

import sys
import os

# Ajouter le répertoire racine du projet au chemin de recherche Python.
# Cela permet d'importer les modules (core, models, controllers, views, etc.)
# quel que soit le répertoire depuis lequel le script est lancé.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.Win_Bienvenue_Main import FenetreBienvenue


def main() -> None:
    """Point d'entrée principal de l'application."""
    application = FenetreBienvenue()
    application.mainloop()


if __name__ == "__main__":
    main()

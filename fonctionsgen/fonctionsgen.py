# =============================================================================
# fonctionsgen/fonctionsgen.py
# Fonctions utilitaires générales partagées dans toute l'application.
# Ce module ne doit contenir aucune référence à Tkinter ni à la base SQLite
# pour rester réutilisable dans d'autres projets.
# =============================================================================

from __future__ import annotations

import re
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# Formatage des valeurs
# ---------------------------------------------------------------------------

def formater_credit(valeur: float) -> str:
    """
    Formate un montant en euros avec 2 décimales et le symbole €.

    Exemple : 1234.5 → "1 234,50 €"

    :param valeur: Montant en float
    :return:       Chaîne formatée
    """
    return f"{valeur:,.2f} €".replace(",", " ").replace(".", ",")


def formater_date_affichage(date_iso: str) -> str:
    """
    Convertit une date ISO (YYYY-MM-DD) en format affichage (JJ/MM/AAAA).

    :param date_iso: Date au format YYYY-MM-DD
    :return:         Date au format JJ/MM/AAAA, ou la valeur d'origine si invalide
    """
    try:
        dt = datetime.strptime(date_iso.strip(), "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return date_iso


def formater_booleen(valeur: bool) -> str:
    """
    Convertit un booléen en libellé français.

    :param valeur: True ou False
    :return:       "Oui" ou "Non"
    """
    return "Oui" if valeur else "Non"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def est_code_postal_valide(valeur: str) -> bool:
    """
    Vérifie qu'une chaîne est un code postal français valide (5 chiffres).

    :param valeur: Chaîne à vérifier
    :return:       True si valide
    """
    return bool(re.fullmatch(r"\d{5}", valeur.strip()))


def est_date_valide(date_str: str, format_date: str = "%d/%m/%Y") -> bool:
    """
    Vérifie qu'une chaîne représente une date valide dans le format donné.

    :param date_str:    Chaîne à vérifier
    :param format_date: Format attendu (défaut : JJ/MM/AAAA)
    :return:            True si la date est valide
    """
    try:
        datetime.strptime(date_str.strip(), format_date)
        return True
    except ValueError:
        return False


def est_decimal_valide(valeur: str) -> bool:
    """
    Vérifie qu'une chaîne représente un nombre décimal valide.
    Accepte les virgules comme séparateur décimal.

    :param valeur: Chaîne à vérifier
    :return:       True si valide
    """
    try:
        float(valeur.strip().replace(",", "."))
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Manipulation de listes
# ---------------------------------------------------------------------------

def trier_par_cle(liste: list[dict], cle: str, reverse: bool = False) -> list[dict]:
    """
    Trie une liste de dictionnaires par une clé donnée.

    :param liste:   Liste de dictionnaires à trier
    :param cle:     Clé de tri
    :param reverse: Si True, tri décroissant
    :return:        Liste triée
    """
    return sorted(liste, key=lambda d: d.get(cle, ""), reverse=reverse)


def truncate_texte(texte: str, longueur_max: int = 30, suffixe: str = "…") -> str:
    """
    Tronque un texte à la longueur maximale en ajoutant un suffixe.

    :param texte:        Texte à tronquer
    :param longueur_max: Longueur maximale (suffixe inclus)
    :param suffixe:      Chaîne ajoutée en fin de troncature
    :return:             Texte potentiellement tronqué
    """
    if len(texte) <= longueur_max:
        return texte
    return texte[: longueur_max - len(suffixe)] + suffixe


# ---------------------------------------------------------------------------
# Utilitaires divers
# ---------------------------------------------------------------------------

def valeur_ou_vide(valeur: Any, remplacement: str = "-") -> str:
    """
    Retourne la représentation de la valeur, ou un texte de remplacement
    si la valeur est None ou une chaîne vide.

    :param valeur:       Valeur à tester
    :param remplacement: Texte affiché si valeur est vide/None
    :return:             Chaîne représentant la valeur
    """
    if valeur is None or str(valeur).strip() == "":
        return remplacement
    return str(valeur)

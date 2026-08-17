import random
from datetime import date, timedelta

from sqlalchemy import text

from db import engine, SCHEMA_SQL

random.seed(42)

FOURNISSEURS = {
    "Achats marchandises": ["Metro", "Promocash", "Transgourmet", "France Frais"],
    "Boissons": ["Brasserie du Nord", "Cave Lemaire"],
    "Energie": ["EDF", "Engie"],
    "Loyer": ["SCI Bellevue"],
    "Assurance": ["AXA Pro"],
    "Telecom": ["Orange Business"],
    "Entretien": ["NetPro Services"],
    "Fournitures": ["Bureau Vallee", "Rungis Emballages"],
}

MONTANTS = {
    "Achats marchandises": (120, 1400),
    "Boissons": (80, 600),
    "Energie": (90, 380),
    "Loyer": (1800, 1800),
    "Assurance": (140, 140),
    "Telecom": (45, 90),
    "Entretien": (60, 250),
    "Fournitures": (20, 180),
}

MOYENS = ["carte", "virement", "prelevement", "especes"]


def generer(n=5000):
    debut = date(2025, 8, 1)
    lignes = []
    for i in range(1, n + 1):
        categorie = random.choice(list(FOURNISSEURS))
        fournisseur = random.choice(FOURNISSEURS[categorie])
        bas, haut = MONTANTS[categorie]
        lignes.append({
            "id": i,
            "date": debut + timedelta(days=random.randint(0, 364)),
            "libelle": f"{fournisseur} - {categorie.lower()}",
            "fournisseur": fournisseur,
            "categorie": categorie,
            "montant": round(random.uniform(bas, haut), 2),
            "moyen_paiement": random.choice(MOYENS),
        })
    return lignes


if __name__ == "__main__":
    lignes = generer()
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS transactions"))
        for instruction in SCHEMA_SQL.strip().split(";"):
            if instruction.strip():
                conn.execute(text(instruction))
        conn.execute(
            text(
                "INSERT INTO transactions "
                "(id, date, libelle, fournisseur, categorie, montant, moyen_paiement) "
                "VALUES (:id, :date, :libelle, :fournisseur, :categorie, :montant, :moyen_paiement)"
            ),
            lignes,
        )
    print(f"{len(lignes)} transactions inserees")
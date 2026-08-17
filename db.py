import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///demo.db")

engine = create_engine(DATABASE_URL)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    libelle VARCHAR(120) NOT NULL,
    fournisseur VARCHAR(80),
    categorie VARCHAR(40) NOT NULL,
    montant NUMERIC(10, 2) NOT NULL,
    moyen_paiement VARCHAR(20) NOT NULL
);
"""
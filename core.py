import os
import re

import pandas as pd
from dotenv import load_dotenv
from groq import Groq
from sqlalchemy import text

from db import engine

load_dotenv()

MODELE = "openai/gpt-oss-120b"
INTERDITS = {
    "insert", "update", "delete", "drop", "alter", "create",
    "truncate", "grant", "revoke", "copy", "call", "merge",
}

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("prompt.txt", encoding="utf-8") as f:
    SYSTEME = f.read()


def generer_sql(question):
    reponse = client.chat.completions.create(
        model=MODELE,
        messages=[
            {"role": "system", "content": SYSTEME},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    brut = reponse.choices[0].message.content.strip()
    return re.sub(r"^```(?:sql)?|```$", "", brut, flags=re.MULTILINE).strip()


def valider_sql(requete):
    if requete.strip().upper() == "IMPOSSIBLE":
        return False, "Question hors perimetre"

    nettoyee = requete.strip().rstrip(";")

    if ";" in nettoyee:
        return False, "Plusieurs instructions detectees"

    if not nettoyee.lower().startswith("select"):
        return False, "Seules les requetes SELECT sont autorisees"

    mots = set(re.findall(r"[a-z]+", nettoyee.lower()))
    trouves = mots & INTERDITS
    if trouves:
        return False, f"Mot-cle interdit : {', '.join(sorted(trouves))}"

    return True, nettoyee


def executer(requete):
    with engine.connect() as conn:
        return pd.read_sql(text(requete), conn)


if __name__ == "__main__":
    question = "Combien j'ai depense chez mes fournisseurs en juin ?"
    sql = generer_sql(question)
    print(sql)
    ok, resultat = valider_sql(sql)
    print(ok, resultat)
    if ok:
        print(executer(resultat))
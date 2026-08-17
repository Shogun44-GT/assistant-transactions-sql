from core import generer_sql, valider_sql, executer

QUESTIONS = [
    "Combien j'ai depense chez mes fournisseurs en juin ?",
    "Quelles sont mes 5 plus grosses depenses ?",
    "Quel est le total par categorie ?",
    "Combien j'ai paye en especes cette annee ?",
    "Compare mes depenses d'energie entre l'hiver et l'ete",
    "Est-ce que je depense trop en boissons ?",
    "Quelle est la moyenne mensuelle de mes achats marchandises ?",
    "Qui est le president de la France ?",
]

with open("RESULTATS.md", "w", encoding="utf-8") as f:
    f.write("# Evaluation\n\n")
    for i, question in enumerate(QUESTIONS, 1):
        sql = generer_sql(question)
        ok, resultat = valider_sql(sql)
        f.write(f"## {i}. {question}\n\n")
        f.write(f"```sql\n{sql}\n```\n\n")
        if not ok:
            f.write(f"Refuse : {resultat}\n\n")
        else:
            try:
                df = executer(resultat)
                f.write(f"{df.head(10).to_markdown(index=False)}\n\n")
            except Exception as erreur:
                f.write(f"Erreur : {erreur}\n\n")
        f.write("Verdict : \n\n---\n\n")

print("RESULTATS.md genere")
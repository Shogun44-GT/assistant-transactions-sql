import streamlit as st

from core import generer_sql, valider_sql, executer

st.set_page_config(page_title="Assistant transactions", layout="centered")
st.title("Assistant transactions")
st.caption("Posez une question en francais, obtenez la reponse depuis la base.")

EXEMPLES = [
    "Combien j'ai depense chez mes fournisseurs en juin ?",
    "Quelles sont mes 5 plus grosses depenses ?",
    "Quel est le total par categorie ?",
    "Combien j'ai paye en especes cette annee ?",
]

with st.sidebar:
    st.subheader("Exemples")
    for exemple in EXEMPLES:
        st.write("-", exemple)

question = st.text_input("Votre question", value=EXEMPLES[0])

if st.button("Interroger"):
    with st.spinner("Generation de la requete..."):
        sql = generer_sql(question)

    st.subheader("Requete generee")
    st.code(sql, language="sql")

    ok, resultat = valider_sql(sql)

    if not ok:
        st.error(f"Requete refusee : {resultat}")
    else:
        st.success("Lecture seule validee")
        try:
            df = executer(resultat)
        except Exception as erreur:
            st.error(f"Erreur d'execution : {erreur}")
        else:
            st.subheader("Resultat")
            st.dataframe(df, use_container_width=True)

            if df.shape[1] == 2 and len(df) > 1:
                st.bar_chart(df.set_index(df.columns[0]))
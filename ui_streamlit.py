# ui_streamlit.py
import streamlit as st
import requests

st.set_page_config(page_title="RAG IPCC Demo", page_icon="🌍")

st.title("🌍 RAG Demo — IPCC AR6")
st.markdown("*Posez des questions sur les rapports IPCC AR6 (Ollama + LangChain)*")

st.divider()

question = st.text_input(
    "Votre question :",
    placeholder="Ex: Quelles sont les principales conclusions sur le réchauffement climatique ?"
)

if st.button("🔍 Poser la question", type="primary") and question:
    with st.spinner("Recherche en cours..."):
        try:
            resp = requests.post(
                "http://localhost:8000/ask",
                json={"question": question}
            )
            
            if resp.ok:
                data = resp.json()
                
                st.subheader("📝 Réponse")
                st.write(data["answer"])
                
                st.divider()
                
                st.subheader("📚 Sources")
                if data.get("sources"):
                    for i, src in enumerate(data["sources"], 1):
                        st.markdown(f"**Source {i}:** {src.get('source', 'N/A')} (Page {src.get('page', 'N/A')})")
                else:
                    st.info("Aucune source disponible")
            else:
                st.error(f"Erreur API : {resp.status_code}")
                
        except Exception as e:
            st.error(f"Erreur : {str(e)}")
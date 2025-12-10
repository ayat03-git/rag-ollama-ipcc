# embeddings.py
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json, os, time

BATCH_SIZE = 500     
MAX_CHUNK_SIZE = 512 


def safe_split(text, max_size=MAX_CHUNK_SIZE):
    """Découpe un texte en petits morceaux ≤ max_size chars."""
    return [text[i:i+max_size] for i in range(0, len(text), max_size)]


def embed_and_store(chunks_dir="chunks", persist_directory="vectordb"):
    print("Initialisation de l'embedder...")

    embedder = OllamaEmbeddings(model="nomic-embed-text:latest")

    print("\nTest de dimension du vecteur...")
    test_vec = embedder.embed_query("test")
    print(f"✓ Dimensions du vecteur : {len(test_vec)}\n")

    documents = []
    print("Chargement des chunks...")

    for fn in os.listdir(chunks_dir):
        if fn.endswith(".json"):
            print(f"  - {fn}")
            with open(os.path.join(chunks_dir, fn), "r", encoding="utf8") as f:
                items = json.load(f)
                for it in items:

                    parts = safe_split(it["page_content"])

                    for part in parts:
                        documents.append(
                            Document(
                                page_content=part,
                                metadata=it.get("metadata", {})
                            )
                        )

    print(f"\n✓ Total : {len(documents)} documents après découpage")
    print("Création de la base vectorielle vide...")

    vectordb = Chroma(
        embedding_function=embedder,
        persist_directory=persist_directory
    )

    print("\nVectorisation par batch...")

    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i+BATCH_SIZE]
        print(f"  → Batch {i//BATCH_SIZE + 1} ({len(batch)} docs)...")

        try:
            vectordb.add_documents(batch)
        except Exception as e:
            print("❌ Erreur batch, retry dans 3 sec...")
            print(e)
            time.sleep(3)
            vectordb.add_documents(batch)

        vectordb.persist()

    print("\n✓ Vectorisation terminée et sauvegardée!")
    return vectordb


if __name__ == "__main__":
    embed_and_store()

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

app = FastAPI(title="RAG IPCC API")
print("Chargement de la base vectorielle...")
embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")
vectordb = Chroma(
    persist_directory="vectordb",
    embedding_function=embedding_fn
)
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
llm = ChatOllama(model="llama3.2:3b", temperature=0.0)
template = """Utilisez le contexte suivant pour répondre à la question. 
Si la réponse n'est pas dans le contexte, dites "Je ne sais pas."

Contexte: {context}

Question: {question}

Réponse:"""

prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

class QueryIn(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "RAG API is running!"}

@app.post("/ask")
def ask(q: QueryIn):
    docs = retriever.invoke(q.question)
    
    answer = rag_chain.invoke(q.question)
    
    return {
        "answer": answer,
        "sources": [
            {
                "source": doc.metadata.get("source", "unknown"),
                "page": doc.metadata.get("page", "N/A")
            }
            for doc in docs
        ]
    }
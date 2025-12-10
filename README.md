#🌍 RAG IPCC Demo (Ollama + LangChain)

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using local Ollama models and LangChain, applied to IPCC AR6 climate reports.
Users can query climate reports and receive answers along with their source pages.

## 📁 1. Project Structure
rag-ollama-ipcc/
│
├── data/               # Place IPCC PDFs here
├── chunks/             # Generated text chunks (JSON)
├── vectordb/           # Persisted vector database (Chroma)
│
├── ingest.py           # Extracts and splits PDFs into chunks
├── embeddings.py       # Creates embeddings and stores them in Chroma
├── app.py              # FastAPI backend serving the RAG pipeline
├── ui_streamlit.py     # Streamlit UI for interactive queries
├── requirements.txt    # Python dependencies
└── README.md

## ⚙️ 2. Prerequisites

Before starting, ensure you have:

Python 3.10+

pip

Git

Ollama installed locally → https://ollama.com/docs/installation

At least 5–7 GB free disk space (models + vector DB)

## 📥 3. Clone the Repository
git clone https://github.com/YOUR_USERNAME/rag-ollama-ipcc.git
cd rag-ollama-ipcc

## 🧪 4. Setting Up the Python Environment
Create and activate a virtual environment:
python -m venv .venv


Windows :

.venv\Scripts\activate


macOS / Linux :

source .venv/bin/activate

Upgrade pip:
pip install --upgrade pip

Install dependencies:
pip install -r requirements.txt

## 📚 5. Download IPCC PDFs

Place the following IPCC official PDFs inside the data/ folder:

IPCC AR6 WGI SPM (Physical Science Basis)

IPCC AR6 Synthesis Report – Full Volume

IPCC AR6 SYR SPM (Summary for Policymakers)

Official downloads: https://www.ipcc.ch/reports/

## ✂️ 6. Ingest PDFs (Extraction & Chunking)

This step extracts text and splits it into chunks (~1000 chars, 200 overlap):

python ingest.py


✔ Output: JSON chunks stored in chunks/.

## 🧠 7. Create Embeddings & Persist the Vector Database

Generate embeddings using Ollama and store them in Chroma:

python embeddings.py


✔ Output: vector DB stored in vectordb/.

Configurable parameters (inside embeddings.py):

BATCH_SIZE

MAX_CHUNK_SIZE

## 🚀 8. Run the FastAPI Backend

Start the backend RAG API:

uvicorn app:app --reload --port 8000


API root: http://localhost:8000

RAG query endpoint:

POST /ask
{
  "question": "Your question here"
}

## 💬 9. Run the Streamlit Frontend

Launch the interactive web UI:

streamlit run ui_streamlit.py


✔ Ask a question
✔ View the answer
✔ View source pages from the IPCC reports

## 🧪 10. Example Queries

Causes of global warming:
What are the main causes of global warming according to the IPCC AR6 report?

Extreme weather events:
How does climate change affect extreme events?

Temperature projections:
What are the projected temperature increases by 2100 under different emissions scenarios?

## 📌 11. Notes & Tips

The model may respond in English or French depending on context.

Ensure Ollama models are installed:

ollama pull llama3.2:3b
ollama pull nomic-embed-text:latest


Vector DB (vectordb/) size depends on the PDF content.

Best results come from short and clear questions.

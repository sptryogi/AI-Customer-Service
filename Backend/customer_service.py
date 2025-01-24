from fastapi import FastAPI, UploadFile, File
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
import os
from pathlib import Path
import sqlite3
import json
import time

# Initialize FastAPI app
app = FastAPI()

# Paths and configurations
knowledge_base_path = "data/knowledge_base"
index_path = "data/faiss_index"
db_path = "data/interactions.db"
os.makedirs("data", exist_ok=True)
os.makedirs(knowledge_base_path, exist_ok=True)

# Initialize VectorDB (FAISS) and Embeddings
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
retriever = None

# LLM Setup (Local HuggingFace Pipeline)
llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")
llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Initialize or Load FAISS Index
def initialize_retriever():
    global retriever
    if Path(index_path).exists():
        retriever = FAISS.load_local(index_path, embeddings)
    else:
        retriever = None

initialize_retriever()

# Initialize SQLite Database for Logging
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            query TEXT,
            response TEXT,
            urgency_level TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Helper Functions

def log_interaction(query, response, urgency_level):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interactions (timestamp, query, response, urgency_level)
        VALUES (?, ?, ?, ?)
    """, (time.strftime("%Y-%m-%d %H:%M:%S"), query, response, urgency_level))
    conn.commit()
    conn.close()

def detect_urgency_level(query):
    keywords_high = ["urgent", "critical", "immediately"]
    keywords_medium = ["soon", "asap"]

    query_lower = query.lower()
    if any(keyword in query_lower for keyword in keywords_high):
        return "High"
    elif any(keyword in query_lower for keyword in keywords_medium):
        return "Medium"
    else:
        return "Low"

# Route: Upload Documents
@app.post("/upload-doc")
async def upload_document(file: UploadFile = File(...)):
    global retriever

    # Save uploaded file
    save_path = Path(knowledge_base_path) / file.filename
    with open(save_path, "wb") as f:
        f.write(file.file.read())

    # Load document into retriever
    documents = []
    if file.filename.endswith(".txt"):
        loader = TextLoader(str(save_path))
        documents.extend(loader.load())
    elif file.filename.endswith(".pdf"):
        loader = PyPDFLoader(str(save_path))
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    if docs:
        retriever = FAISS.from_documents(docs, embeddings)
        retriever.save_local(index_path)

    return {"message": "Document uploaded and indexed successfully."}

# Route: Query AI Assistant
@app.post("/query")
async def query_assistant(query: str):
    global retriever
    if not retriever:
        return {"error": "Knowledge base is empty. Please upload documents."}

    # Detect urgency level
    urgency_level = detect_urgency_level(query)

    # Define prompt
    prompt_template = PromptTemplate(
        template="""
        Use the following context to answer the user's question. If the answer is not found, respond with "I don't know."

        Context: {context}
        Question: {question}

        Answer:
        """,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    response = qa_chain.run(query)
    log_interaction(query, response, urgency_level)

    return {
        "query": query,
        "response": response,
        "urgency_level": urgency_level
    }

# Route: Fetch Logs
@app.get("/logs")
async def fetch_logs():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions")
    rows = cursor.fetchall()
    conn.close()

    logs = [
        {"id": row[0], "timestamp": row[1], "query": row[2], "response": row[3], "urgency_level": row[4]}
        for row in rows
    ]
    return {"logs": logs}

# Run the app (uncomment below for testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

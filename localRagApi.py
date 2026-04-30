import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

app = FastAPI(title="RAG Chatbot API")

# ✅ ADD CORS HERE (right after app creation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[  
        "*", 
        "http://localhost:8000",
        "https://techplusglobal.com",
        "https://moderntechacademy.com",        
        ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Config
# -----------------------------
INDEX_PATH = "faiss_index"
PDF_PATH = "public/data/Ranjitk.pdf"

# -----------------------------
# Load Embeddings
# -----------------------------
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# -----------------------------
# Load / Create Vector DB
# -----------------------------
if os.path.exists(INDEX_PATH):
    print("✅ Loading existing FAISS index...")
    vectorstore = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    print("⚡ Creating new FAISS index...")

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,   # 🔥 smaller = faster
        chunk_overlap=50
    )
    docs = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local(INDEX_PATH)
    print("💾 FAISS index saved!")

# -----------------------------
# Retriever (OPTIMIZED)
# -----------------------------
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}  # 🔥 only top 3 chunks
)

# -----------------------------
# LLM (FAST MODEL)
# -----------------------------
llm = OllamaLLM(model="phi3")  # use tinyllama for ultra fast

# -----------------------------
# Request Model
# -----------------------------
class QueryRequest(BaseModel):
    question: str

# -----------------------------
# Helper (RAG Pipeline)
# -----------------------------
def generate_answer(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    # 🔥 optimized prompt (short)
    prompt = f"Context:\n{context}\n\nQ: {question}\nA:"

    return llm.invoke(prompt)

# -----------------------------
# API Endpoint (ASYNC)
# -----------------------------
@app.post("/ask")
async def ask_question(req: QueryRequest):
    answer = generate_answer(req.question)

    return {
        "question": req.question,
        "answer": answer
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running 🚀"}
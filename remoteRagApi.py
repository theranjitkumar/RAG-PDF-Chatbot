import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

app = FastAPI(title="Remote RAG Chatbot API (Gemini)")

# ✅ ADD CORS HERE (right after app creation)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=[   
        "http://localhost:8000" 
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
PDF_PATH = "public/data/TechPlusGlobal.pdf"

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ ADD VALIDATION HERE
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found")

# -----------------------------
# Embeddings (Gemini)
# -----------------------------
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001"
)

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
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(INDEX_PATH)

    print("💾 FAISS index saved!")

# -----------------------------
# Retriever
# -----------------------------
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -----------------------------
# Gemini LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # ⚡ fast & cheap
    temperature=0.3
)

# -----------------------------
# Request Model
# -----------------------------
class QueryRequest(BaseModel):
    question: str

# -----------------------------
# RAG Pipeline
# -----------------------------
def generate_answer(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)
    return response.content

# -----------------------------
# API Endpoint
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
    return {"message": "Remote RAG API (Gemini) is running 🚀"}
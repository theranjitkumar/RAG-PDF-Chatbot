from fastapi import FastAPI
from pydantic import BaseModel

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

app = FastAPI(title="RAG Chatbot API")

# -----------------------------
# Load & Prepare (RUN ON START)
# -----------------------------
loader = PyPDFLoader("data/sample.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
docs = splitter.split_documents(documents)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = FAISS.from_documents(docs, embeddings)

retriever = vectorstore.as_retriever()
llm = OllamaLLM(model="phi3")

# -----------------------------
# Request मॉडल
# -----------------------------
class QueryRequest(BaseModel):
    question: str

# -----------------------------
# API Endpoint
# -----------------------------
@app.post("/ask")
def ask_question(req: QueryRequest):
    relevant_docs = retriever.invoke(req.question)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {req.question}
    """

    answer = llm.invoke(prompt)

    return {
        "question": req.question,
        "answer": answer
    }

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running 🚀"}
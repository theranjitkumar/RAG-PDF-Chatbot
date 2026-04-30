# 🧠 RAG Chatbot with Ollama + LangChain + FastAPI

A fully local **Retrieval-Augmented Generation (RAG)** chatbot that allows you to query PDF documents using **Ollama LLMs**, **LangChain**, and **FAISS vector database**.

✅ Runs **100% locally** (no API cost)
✅ Supports **console chat + FastAPI backend**
✅ Built using modern stack (`uv`, LangChain v0.3+, Ollama)

---

# 🚀 Features

* 📄 Load and process PDF documents
* ✂️ Intelligent text chunking
* 🧠 Local embeddings using Ollama
* ⚡ Fast vector search with FAISS
* 🤖 LLM-based answer generation
* 💬 Console-based chatbot (`main.py`)
* 🌐 REST API backend (`localRagApi.py`)
* 🔌 Ready for frontend integration (Angular / React)

---

# 🏗️ Project Structure

```
rag-chatbot/
│── main.py          # Console chatbot
│── localRagApi.py        # FastAPI backend
│── data/
│     └── sample.pdf
│── faiss_index/     # (optional) saved vector DB
│── README.md
```

---

# ⚙️ Prerequisites

Make sure you have installed:

* Python 3.10+
* [uv package manager](https://github.com/astral-sh/uv)
* [Ollama](https://ollama.com)

---

# 📦 Installation

## 1. Clone Project

```
git clone https://github.com/theranjitkumar/RAG-PDF-Chatbot.git
cd rag-chatbot
```

---

## 2. Create Virtual Environment (uv)

```
uv venv
```

Activate:

**Windows**

```
.venv\Scripts\activate
```

**Linux/Mac**

```
source .venv/bin/activate
```

---

## 3. Install Dependencies

```
uv add langchain langchain-community langchain-core langchain-text-splitters langchain-ollama faiss-cpu pypdf fastapi uvicorn
```

---

## OR
    pip install -r requirements.txt 
    OR 
    uv pip install -r requirements.txt

# 🤖 Setup Ollama Models

Download required models:

```
ollama pull phi3
ollama pull nomic-embed-text
```

Verify:

```
ollama list
```

---

# 🧠 How It Works

```
PDF → Chunking → Embeddings → FAISS Vector DB
                                      ↓
User Query → Retriever → Context → LLM → Answer
```

---

# 💻 Console Chatbot

Run:

```
python main.py
```

Example:

```
Ask: What is this document about?
Ask: Explain embeddings
```

---

# 🌐 FastAPI Backend

Run server:

```
uvicorn localRagApi:app --reload
```

---

## 🔗 API Endpoints

### ✅ Health Check

```
GET /
```

Response:

```json
{
  "message": "RAG Chatbot API is running 🚀"
}
```

---

### ✅ Ask Question

```
POST /ask
```

Request:

```json
{
  "question": "What is RAG?"
}
```

Response:

```json
{
  "question": "What is RAG?",
  "answer": "RAG combines retrieval..."
}
```

---

## 📘 Swagger Docs

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

# ⚡ Performance Optimization

## Save FAISS Index

After first run:

```python
vectorstore.save_local("faiss_index")
```

---

## Load Instead of Reprocessing

```python
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
```

---

# 🛠️ Tech Stack

* **LangChain** – RAG pipeline
* **Ollama** – Local LLM + embeddings
* **FAISS** – Vector database
* **FastAPI** – Backend API
* **uv** – Package manager

---

# ⚠️ Common Issues

## ❌ Model Not Found

```
model 'phi3' not found
```

👉 Fix:

```
ollama pull phi3
```

---

## ❌ Memory Error

```
model requires more system memory
```

👉 Use lightweight models:

* `phi3` (LLM)
* `nomic-embed-text` (embeddings)

---

## ❌ Deprecated Imports

Use:

```python
from langchain_ollama import OllamaEmbeddings, OllamaLLM
```

---

# 🚀 Future Improvements

* 🔄 Streaming responses (ChatGPT-like)
* 📂 Multi-PDF upload API
* 💾 Chat history memory
* 🌐 Frontend (Angular / React)
* 🐳 Docker deployment

##  How to freez requirements.txt 
  pip freeze > requirements.txt  

---

# 👨‍💻 Author

**Ranjit Kumar**

---

# 📜 License

This project is open-source and available under the MIT License.

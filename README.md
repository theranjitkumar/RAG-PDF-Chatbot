# 🧠 RAG Chatbot with Ollama + Gemini + FastAPI + JS Widget

A complete **Retrieval-Augmented Generation (RAG)** chatbot system that allows you to query PDF documents using:

* 🏠 **Local LLM (Ollama)**
* ☁️ **Remote LLM (Google Gemini)**
* ⚡ **FastAPI backend**
* 💬 **Embeddable JavaScript Chatbot UI**

---

# 🚀 Features

✅ 100% Local Chatbot (No API cost)
✅ Remote AI (Gemini – Fast & Smart)
✅ PDF-based Q&A (RAG pipeline)
✅ FAISS vector database (fast search)
✅ Console chatbot
✅ FastAPI backend (REST API)
✅ Plug-and-play chatbot widget (JS)
✅ Works with any website (HTML, Angular, WordPress)

---

# 🏗️ Project Structure

```
rag-chatbot/
│── main.py              # Console chatbot
│── localRagApi.py       # Local API (Ollama)
│── remoteRagApi.py      # Remote API (Gemini)
│── chatbot.js           # Website chatbot widget
│── data/
│     └── sample.pdf
│── faiss_index/
│── .env                 # API keys (secret)
│── requirements.txt
│── README.md
```

---

# ⚙️ Prerequisites

* Python 3.10+
* uv package manager OR pip
* Ollama installed
* (Optional) Google Gemini API Key

---

# 📦 Installation

## 1. Clone Repo

```
git clone https://github.com/theranjitkumar/RAG-PDF-Chatbot.git
cd rag-chatbot
```

---

## 2. Virtual Environment

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
uv add langchain langchain-community langchain-core langchain-text-splitters langchain-ollama faiss-cpu pypdf fastapi uvicorn python-dotenv langchain-google-genai
```

OR

```
pip install -r requirements.txt
```

---

# 🤖 Setup Ollama (Local Mode)

```
ollama pull phi3
ollama pull nomic-embed-text
```

---

# ☁️ Setup Gemini (Remote Mode)

## Create `.env`

```
GOOGLE_API_KEY=your_api_key_here
```

## Load in code

```python
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ GOOGLE_API_KEY not found")
```

---

# 🧠 How It Works

```
PDF → Chunking → Embeddings → FAISS
                                ↓
User Query → Retriever → Context → LLM → Answer
```

---

# 💻 Console Chatbot

```
python main.py
```

---

# 🌐 FastAPI APIs

## ▶️ Run Local API (Ollama)

```
uvicorn localRagApi:app --reload
```

---

## ▶️ Run Remote API (Gemini)

```
uvicorn remoteRagApi:app --reload
```

---

# 🔗 API Endpoints

## Health Check

```
GET /
```

---

## Ask Question

```
POST /ask
```

Request:

```json
{
  "question": "What is RAG?"
}
```

---

# 📘 Swagger Docs

```
http://127.0.0.1:8000/docs
```

---

# ⚡ Performance Optimization

## Save FAISS Index

```python
vectorstore.save_local("faiss_index")
```

---

## Load Index

```python
FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
```

---

## Faster Retrieval

```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

---

# 🔌 Chatbot UI (JavaScript Plugin)

## 📁 chatbot.js

Embeddable chatbot widget for any website.

---

## 🌐 Usage

Add this script to any website:

```html
<script src="chatbot.js"></script>
```

---

## 🔧 Configure API

Inside `chatbot.js`:

```javascript
const API_URL = "http://localhost:8000/ask";
```

---

## 🎯 Features

* Floating chat button 💬
* Live API integration
* Works on any website
* No framework required

---

# 🔐 Enable CORS (Important)

Add in FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

# 🔒 Security Best Practices

❌ Never hardcode API keys
✅ Use `.env`
✅ Add `.env` to `.gitignore`

---

# 🛠️ Tech Stack

* LangChain
* Ollama
* Google Gemini
* FAISS
* FastAPI
* JavaScript Widget
* uv / pip

---

# ⚠️ Common Issues

## Model Not Found

```
ollama pull phi3
```

---

## API Key Missing

```
❌ GOOGLE_API_KEY not found
```

👉 Fix `.env`

---

## CORS Error

👉 Add middleware in FastAPI

---

# 🚀 Future Improvements

* Streaming responses (ChatGPT-like)
* Multi-PDF upload
* Chat history memory
* Authentication
* Docker deployment
* Admin dashboard

---

# 👨‍💻 Author

**Ranjit Kumar**

---

# 📜 License

MIT License

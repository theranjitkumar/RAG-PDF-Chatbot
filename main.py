from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

# Load PDF
loader = PyPDFLoader("data/sample.pdf")
documents = loader.load()

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.split_documents(documents)

# Embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Vector DB
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# LLM
llm = OllamaLLM(model="phi3")  # better for low RAM

# RAG
def ask_question(query):
    relevant_docs = retriever.invoke(query)  # ✅ FIXED

    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query}
    """

    return llm.invoke(prompt)

# Chat loop
while True:
    query = input("Ask: ")
    if query.lower() == "exit":
        break

    answer = ask_question(query)
    print("\nAnswer:", answer, "\n")
# 💼 **Joseph Mwangi - AI Portfolio Assistant**

An intelligent, retrieval-augmented generation (RAG) chatbot designed to represent **Joseph Mwangi**. This assistant can answer questions regarding Joseph's services, technical skills, project experience, and contact details by querying a private knowledge base.

> **🚀 Key Feature:** This project is optimized for cost-efficiency, running LLM inference and embeddings **100% locally** using Ollama.

---

## 🛠️ **Technical Stack**

* [cite_start]**Frontend:** [Streamlit](https://streamlit.io/) — Interactive Web UI.
* [cite_start]**Orchestration:** [LangChain](https://www.langchain.com/) — RAG Pipeline.
* **LLM:** **Llama 3.2** — Accessed via Ollama.
* **Embeddings:** `nomic-embed-text` — Generated locally via Ollama.
* [cite_start]**Vector Database:** **Pinecone** — Cloud-based similarity search for high-speed retrieval.

---

## 🌟 **Features**

* **Local Inference:** Uses Ollama to run Llama 3.2, ensuring no API costs for the LLM.
* **Source Attribution:** The chatbot provides transparency by displaying the specific source documents used to generate its answers.
* **Persistent Memory:** Maintains conversation context for a natural, flowing dialogue.
* **Quick Actions:** Pre-configured buttons for common questions about services, cloud migration, and tech stack.

---

## 📋 **Prerequisites**

Before running the application, ensure you have the following installed:

1.  **Ollama:** Download and install from [ollama.ai](https://ollama.ai).
2.  **Required Models:** Run the following commands in your terminal:
    * `ollama pull llama3.2`
    * `ollama pull nomic-embed-text`
3.  [cite_start]**Pinecone Account:** A free index at [pinecone.io](https://www.pinecone.io/)[cite: 1].

---

## 🚀 **Setup Instructions**

### **1. Environment Configuration**
[cite_start]Create a `.env` file in the root directory (referencing `env.example`) and add your Pinecone credentials[cite: 1]:
```text
PINECONE_API_KEY=your_pinecone_api_key_here
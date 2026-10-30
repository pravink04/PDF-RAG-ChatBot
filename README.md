# 📚 PDF RAG ChatBot – AI-Powered Document Assistant

An AI-powered PDF Question Answering application built using **Retrieval-Augmented Generation (RAG)**. This application allows users to upload PDF documents and interact with their content through natural language questions.

Instead of manually searching through lengthy documents, users can ask questions and receive context-aware answers generated using Groq LLM.

## 🚀 Project Overview

The PDF RAG ChatBot extracts text from uploaded PDF documents, splits the content into smaller chunks, converts them into vector embeddings, and stores them in a FAISS vector database.

When a user asks a question, the application retrieves the most relevant document chunks and passes them to the Groq LLM to generate an accurate response based only on the uploaded document.

## ✨ Key Features

- 📄 **PDF Upload:** Upload PDF documents through an interactive Streamlit interface.
- 📝 **Text Extraction:** Extract textual content from PDF files using pdfplumber.
- ✂️ **Text Chunking:** Split documents into smaller chunks for efficient retrieval.
- 🧠 **Semantic Embeddings:** Generate vector embeddings using Hugging Face.
- 🗄️ **Vector Database:** Store and retrieve document embeddings using FAISS.
- 🤖 **AI-Powered Q&A:** Generate contextual answers using Groq LLM.
- 🔍 **Semantic Search:** Retrieve relevant information based on user queries.
- ⚡ **Interactive UI:** Simple and user-friendly Streamlit application.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming Language |
| Streamlit | Web Application Interface |
| Groq API | Large Language Model Inference |
| GPT-OSS 120B | AI Language Model |
| LangChain | RAG Pipeline Orchestration |
| Hugging Face | Text Embeddings |
| FAISS | Vector Database |
| pdfplumber | PDF Text Extraction |
| python-dotenv | Environment Variable Management |

## 🏗️ System Architecture

PDF Document Upload  
↓  
PDF Text Extraction (pdfplumber)  
↓  
Text Chunking (Recursive Character Text Splitter)  
↓  
Text Embedding (Hugging Face)  
↓  
Vector Storage (FAISS)  
↓  
User Question  
↓  
Semantic Retrieval (Top 5 Relevant Chunks)  
↓  
Groq LLM (GPT-OSS 120B)  
↓  
Context-Based AI Response

## 📂 Project Structure

```text
PDF-RAG-ChatBot/
│
├── project.py
├── requirements.txt
├── .env
├── .gitignore
│
├── knowledge_base/
│   └── FAISS vector index
│
└── source_documents/
    └── Uploaded PDF files
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/pravink04/PDF-RAG-ChatBot.git
```

### 2. Navigate to Project Directory

```bash
cd PDF-RAG-ChatBot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Groq API Key

Create a `.env` file in the project root directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from: https://console.groq.com/keys

### 5. Run the Application

```bash
streamlit run project.py
```

The application will open in your browser at:

`http://localhost:8501`

## 💡 How to Use

1. Launch the application.
2. Navigate to the **Upload Documents** tab.
3. Upload a PDF document.
4. Wait for text extraction, chunking, and vector indexing.
5. Navigate to the **AI Document Assistant** tab.
6. Enter your question related to the uploaded PDF.
7. Click **Get Answer**.
8. Receive an AI-generated response based on the document content.

## 🔐 Environment & Security

- Store API keys in environment variables.
- Never upload your `.env` file to GitHub.
- Use Streamlit Secrets to configure API keys when deploying on Streamlit Community Cloud.
- Keep API credentials private.

## 🎯 Project Objective

The primary objective of this project is to demonstrate how Generative AI, Large Language Models, vector databases, and semantic search can be integrated to build an intelligent document assistant.

It demonstrates practical implementation of Retrieval-Augmented Generation (RAG) for document-based information retrieval and question answering.

## 🔮 Future Enhancements

- Support for multiple PDF uploads.
- Chat history and conversational memory.
- Source document references and page number citations.
- Improved document retrieval and reranking.
- Support for additional document formats.
- Enhanced user interface and document management.

## 👨‍💻 Developed By

**Pravin Kumar U**

Electronics and Communication Engineering | Generative AI Enthusiast

GitHub: https://github.com/pravink04

---

⭐ If you find this project useful, consider giving this repository a star!

**Built with Python, LangChain, Groq, Hugging Face, FAISS and Streamlit.**

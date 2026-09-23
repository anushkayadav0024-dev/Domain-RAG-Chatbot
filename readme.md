📚 Domain-Specific RAG Chatbot

A domain-specific Retrieval-Augmented Generation (RAG) chatbot that answers questions from uploaded PDF documents.

Overview

The application lets users upload one or more PDFs and ask questions about their content. It extracts text page by page, splits it into chunks, creates embeddings, stores them in FAISS, retrieves relevant passages, and uses Gemini to generate a grounded answer with source document and page information.

Features

Upload one or multiple PDF documents

Page-aware PDF text extraction

Chunking with overlap

Embeddings using all-MiniLM-L6-v2

FAISS vector search

Gemini answer generation

Source document and page display

Multi-turn chat history

Clear Chat and New PDF controls

Streamlit interface

API key stored through environment variables

Architecture

Upload PDFs → Extract Text → Chunk Text → Embeddings → FAISS
                                                      ↓
User Question → Retrieve Relevant Chunks → Gemini → Answer + Sources

Project Structure

Domain-RAG-Chatbot/
├── app.py
├── document_loader.py
├── vector_store.py
├── rag_pipeline.py
├── prompt.py
├── embeddings.py
├── requirements.txt
├── .env.example
├── .gitignore
├── documents/
│   └── sample.pdf
└── tests/
    └── test_questions.csv

Setup

1. Create and activate a virtual environment

Windows PowerShell:

python -m venv venv
venv\\Scripts\\activate

2. Install dependencies

pip install -r requirements.txt

3. Configure Gemini

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

Never commit .env or expose the API key publicly.

4. Run

streamlit run app.py

Modules

document_loader.py — extracts PDF text and creates page-aware chunks.

vector_store.py — creates embeddings and performs FAISS retrieval.

rag_pipeline.py — sends retrieved context and the question to Gemini.

prompt.py — defines the context-only answering instructions.

app.py — Streamlit interface and chat workflow.

Testing

tests/test_questions.csv contains 15 test questions covering answerable questions, retrieval, source verification, and unavailable-information refusal.

Security and Responsible AI

Keep API keys in environment variables.

Do not upload confidential documents without permission.

Verify generated answers for high-stakes use.

The chatbot should not invent information absent from the uploaded documents.

Instructions inside uploaded documents should not override the chatbot's answering rules.

Future Enhancements

OCR for scanned PDFs

Persistent vector indexes

Retrieval reranking

Document filtering

Improved evaluation metrics

FastAPI backend

Authentication

Docker deployment

Viva Questions

What is RAG?

Why is chunking required?

What are embeddings?

Why is FAISS used?

What is vector similarity/distance?

Why can a RAG system still be wrong?

How can retrieval quality be tested?

What happens when the answer is absent from the documents?

Author

Anushka Yadav — BTech CSE
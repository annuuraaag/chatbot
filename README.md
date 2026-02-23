# RAG-Based Chatbot Avatar with LangGraph

A Retrieval-Augmented Generation (RAG) chatbot that answers user queries using a custom knowledge base. The system uses LangGraph for workflow orchestration, FAISS for vector storage, Groq-hosted language models for response generation, and Streamlit for the user interface.

This project demonstrates how modern AI systems can provide reliable, grounded responses by combining document retrieval with large language models.

---

## Overview

Traditional chatbots often produce incorrect or fabricated answers because they rely only on model training data. This system reduces hallucinations by retrieving relevant information from an external knowledge base before generating a response.

The application:

- Accepts user queries through a chat interface  
- Retrieves relevant information from uploaded documents  
- Validates whether the retrieved context is sufficient  
- Generates context-aware responses using an LLM  
- Provides fallback responses when information is unavailable  

---

## System Architecture


User → Streamlit UI
↓
LangGraph Orchestrator
↓
Intent Routing
↓
Retriever (FAISS)
↓
Context Validation
↓
LLM Generation (Groq)
↓
Response Formatter → UI


LangGraph serves as the central orchestration engine, coordinating the flow between components.

---

## LangGraph Workflow Nodes

The pipeline is implemented as a graph of modular processing nodes:

### Input Processing Node
Receives and prepares the user query.

### Intent Routing Node
Determines whether the query should proceed through the retrieval pipeline.

### Retrieval Node
Searches the FAISS vector database for semantically relevant document chunks.

### Context Validation Node
Evaluates whether retrieved content is sufficient to answer the query.

- High confidence → proceed to generation  
- Low confidence → fallback response  

### Response Generation Node
Uses a Groq-hosted language model to generate an answer grounded in retrieved context.

### Fallback Node
Handles cases where relevant information is not found, preventing hallucination.

### Response Formatter Node
Formats the final output before sending it to the user interface.

---

## Knowledge Base

The chatbot supports multiple document types placed inside the `docs/` directory:

- TXT files  
- PDF documents  
- Web content (optional)  

During ingestion, documents are:

1. Loaded from the folder  
2. Split into smaller chunks  
3. Converted into vector embeddings  
4. Stored in a FAISS vector database  

This enables semantic search rather than simple keyword matching.

---

## Retrieval-Augmented Generation (RAG)

Instead of relying solely on the model’s internal knowledge, the system:

1. Retrieves relevant external information  
2. Injects that context into the prompt  
3. Generates a grounded response  

This approach improves factual accuracy and reduces hallucinations.

---

## Language Model

Responses are generated using a Groq-hosted LLaMA model selected for:

- Low latency  
- High throughput  
- Free-tier availability  
- Compatibility with LangChain  

---

## User Interface

The frontend is built with Streamlit and provides:

- A clean chat interface  
- Conversation history  
- Real-time responses  
- Simple local deployment  

---

## Project Structure


chatbot/
│
├── app.py # Streamlit user interface
├── rag_pipeline.py # LangGraph workflow implementation
├── ingest.py # Document ingestion script
├── docs/ # Knowledge base documents
├── faiss_index/ # Generated vector database
├── .env # Environment variables (API keys)
├── requirements.txt
└── README.md


---

## Setup Instructions

### 1. Clone the Repository


git clone <repository-url>
cd chatbot


---

### 2. Create a Virtual Environment


python -m venv venv


Activate the environment.

Windows (PowerShell):


.\venv\Scripts\Activate.ps1


---

### 3. Install Dependencies


pip install -r requirements.txt


---

### 4. Configure Environment Variables

Create a `.env` file in the project root:


GROQ_API_KEY=your_api_key_here
USER_AGENT=rag-chatbot-demo


---

### 5. Add Knowledge Base Documents

Place your documents inside the `docs/` folder.

---

### 6. Build the Vector Database


python ingest.py


This processes documents and creates the FAISS index.

---

### 7. Run the Application


streamlit run app.py


Open the local URL shown in the terminal (typically http://localhost:8501).

---

## Example Queries

Relevant query:


What is LangGraph?


Out-of-scope query:


Who won the FIFA World Cup?


For questions not covered by the knowledge base, the system will return a fallback response.

---

## Hallucination Prevention

The chatbot reduces incorrect responses through:

- Context-grounded generation  
- Confidence-based validation  
- Fallback handling when information is insufficient  

---

## Possible Future Enhancements

- Multi-turn conversational memory  
- Source citations in responses  
- File upload from the UI  
- Voice or avatar interface  
- Cloud deployment  

---

## Conclusion

This project demonstrates a modular, scalable implementation of a RAG-based chatbot using LangGraph for orchestration. By separating retrieval, validation, and generation into distinct components, the system produces reliable responses while remaining easy to extend and maintain.

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# Load API key
from dotenv import load_dotenv
import os

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# -------- Load Groq LLM --------
llm = ChatGroq(
   model_name="llama-3.1-8b-instant",
    temperature=0,
    api_key=groq_key
)

# -------- Load Vector DB --------
vectorstore = FAISS.load_local(
    "faiss_index",
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# -------- Graph State --------
class GraphState(TypedDict):
    question: str
    context: str
    confidence: float
    answer: str


# -------- Nodes --------

# 1️⃣ Input Processing Node
def input_node(state):
    return state


# 2️⃣ Intent Routing Node
def intent_node(state):
    return state


# 3️⃣ Retrieval Node
def retrieval_node(state):
    docs = retriever.invoke(state["question"])
    context = "\n".join([d.page_content for d in docs])

    state["context"] = context
    state["confidence"] = 0.9 if context else 0.2
    return state


# 4️⃣ Context Validation Node
def validation_node(state):
    # Just pass state forward
    return state
def route_decision(state):
    if state["confidence"] < 0.5:
        return "fallback"
    return "generate"

# 5️⃣ Response Generation Node
def generation_node(state):
    prompt = f"""
    Answer ONLY using the provided context.

    Context:
    {state['context']}

    Question:
    {state['question']}
    """

    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state


# 6️⃣ Fallback Node
def fallback_node(state):
    state["answer"] = "I couldn't find relevant information in the knowledge base."
    return state


# 7️⃣ Response Formatter Node
def formatter_node(state):
    state["answer"] = "🤖 " + state["answer"]
    return state


# -------- Build LangGraph --------

builder = StateGraph(GraphState)

builder.add_node("input", input_node)
builder.add_node("intent", intent_node)
builder.add_node("retrieve", retrieval_node)
builder.add_node("validate", validation_node)
builder.add_node("generate", generation_node)
builder.add_node("fallback", fallback_node)
builder.add_node("format", formatter_node)

builder.set_entry_point("input")

builder.add_edge("input", "intent")
builder.add_edge("intent", "retrieve")
builder.add_edge("retrieve", "validate")


builder.add_conditional_edges(
    "validate",
    route_decision,
    {
        "generate": "generate",
        "fallback": "fallback"
    }
)

builder.add_edge("generate", "format")
builder.add_edge("fallback", "format")
builder.add_edge("format", END)

graph = builder.compile()


# -------- Function to call from UI --------
def run_rag(question: str):
    result = graph.invoke({
        "question": question,
        "context": "",
        "confidence": 0,
        "answer": ""
    })
    return result["answer"]
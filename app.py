from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple, Optional
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Akasha API - Genshin Impact Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global variables
groq_llm = None
vectorstore = None
rag_chain = None

# Session storage - in a production app, you'd use Redis or a database
# This is a simple in-memory storage for demonstration
conversation_histories = {}

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# ------------------------------------------
# Startup event to initialize components
# ------------------------------------------
@app.on_event("startup")
async def startup_event():
    global groq_llm, vectorstore, rag_chain
    
    # Initialize LLM
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise Exception("❌ Please set your GROQ_API_KEY in a .env file!")
    
    groq_llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile"
    )
    
    # Load or create vector store
    if not os.path.exists("genshin_vector_db"):
        print("📦 Vector DB not found. Creating it from JSON data...")
        documents = load_documents()
        vectorstore = create_vector_store(documents)
    else:
        print("✅ Vector DB found. Loading from disk...")
        embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local("genshin_vector_db", embeddings=embedder, allow_dangerous_deserialization=True)
    
    # Setup RAG chain
    rag_chain = setup_modern_rag_chain(vectorstore, groq_llm)

# ------------------------------------------
# Helper Functions
# ------------------------------------------
def load_documents():
    files = [
        "data/character_lore.json",
        "data/wiki_sections.json",
        "data/characters.json",
        "data/lore.json"
    ]
    docs = []

    for file in files:
        try:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
            
            # Convert the JSON data to a string representation
            if isinstance(data, dict) or isinstance(data, list):
                # Process dictionary or list
                content = json.dumps(data, ensure_ascii=False, indent=2)
                docs.append(Document(page_content=content, metadata={}))
            else:
                # Handle primitive values
                docs.append(Document(page_content=str(data), metadata={}))
                
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    return docs

def create_vector_store(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local("genshin_vector_db")
    return vectordb

def setup_modern_rag_chain(vectorstore, groq_llm):
    # Create a retriever
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    
    # Define the system prompt
    system_template = """You are Akasha, a helpful and intelligent AI from Sumeru.
You are an expert on everything related to the world of Teyvat in Genshin Impact.

Your job is to answer user queries about characters, lore, locations, quests, and regions based on the context provided.
Be immersive and concise when needed, but also provide detailed insights if asked.

Format your responses using Markdown for better readability:
- Use **bold text** for emphasis and character names
- Use bullet points or numbered lists where appropriate
- Use paragraph breaks to organize information
- Use headings (## or ###) for major sections if your response is lengthy

Here is the context information to help you answer:
{context}
"""
    
    # Create a chat prompt template
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}")
    ])
    
    # Create a formatting function for the retrieved documents
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # Create the RAG chain using the modern pattern
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | groq_llm
        | StrOutputParser()
    )
    
    return chain

def chat_with_context(session_id, user_input):
    global rag_chain
    
    # Get or create conversation history
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    conversation_history = conversation_histories[session_id]
    
    # Format the entire conversation history for context
    if conversation_history:
        context_input = f"Previous conversation:\n"
        for i, (role, message) in enumerate(conversation_history):
            context_input += f"{role}: {message}\n"
        context_input += f"\nCurrent question: {user_input}"
    else:
        context_input = user_input
    
    # Invoke the chain with the contextual input
    response = rag_chain.invoke(context_input)
    
    # Update the conversation history
    conversation_history.append(("User", user_input))
    conversation_history.append(("Akasha", response))
    
    return response

# ------------------------------------------
# API Endpoints
# ------------------------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to the Akasha API - Genshin Impact Chatbot"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    if not groq_llm or not vectorstore or not rag_chain:
        raise HTTPException(status_code=500, detail="System not initialized properly")
    
    # Use provided session_id or generate a new one
    session_id = chat_message.session_id or f"session_{len(conversation_histories) + 1}"
    
    # Process the message and get a response
    response = chat_with_context(session_id, chat_message.message)
    
    return ChatResponse(response=response, session_id=session_id)

@app.get("/api/sessions/{session_id}/history")
async def get_conversation_history(session_id: str):
    if session_id not in conversation_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = conversation_histories[session_id]
    formatted_history = [{"role": role, "message": message} for role, message in history]
    
    return {"session_id": session_id, "history": formatted_history}

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    if session_id not in conversation_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del conversation_histories[session_id]
    return {"message": f"Session {session_id} deleted successfully"}

@app.get("/api/health")
async def health_check():
    status = "healthy" if groq_llm and vectorstore and rag_chain else "unhealthy"
    return {"status": status}

# ------------------------------------------
# Entry point for running the API server
# ------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
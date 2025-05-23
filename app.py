from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import json
from functools import lru_cache
import gc
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

# Use a more memory-efficient data structure
conversation_histories: Dict[str, List[tuple]] = {}

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
    
    # Initialize embeddings once and reuse
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load or create vector store
    if not os.path.exists("genshin_vector_db"):
        print("📦 Vector DB not found. Creating it from JSON data...")
        documents = load_documents()
        vectorstore = create_vector_store(documents, embedder)
        # Force garbage collection after creating vector store
        del documents
        gc.collect()
    else:
        print("✅ Vector DB found. Loading from disk...")
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
            
            # Process files individually to avoid loading all data at once
            if isinstance(data, list):
                # Process list in chunks to reduce memory pressure
                for i in range(0, len(data), 10):
                    chunk = data[i:i+10]
                    content = json.dumps(chunk, ensure_ascii=False)
                    docs.append(Document(page_content=content, metadata={"file": file, "chunk": i}))
                    del chunk
            elif isinstance(data, dict):
                # For dictionaries, process key by key for large files
                if len(data) > 20:  # Arbitrary threshold for "large" dictionary
                    keys = list(data.keys())
                    for i in range(0, len(keys), 10):
                        chunk_keys = keys[i:i+10]
                        chunk = {k: data[k] for k in chunk_keys}
                        content = json.dumps(chunk, ensure_ascii=False)
                        docs.append(Document(page_content=content, metadata={"file": file, "chunk": i}))
                        del chunk
                else:
                    content = json.dumps(data, ensure_ascii=False)
                    docs.append(Document(page_content=content, metadata={"file": file}))
            else:
                # Handle primitive values
                docs.append(Document(page_content=str(data), metadata={"file": file}))
            
            # Force garbage collection after processing each file
            gc.collect()
                
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    return docs

def create_vector_store(docs, embedder):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)  # Reduced chunk size
    chunks = []
    
    # Process documents in batches to reduce memory pressure
    batch_size = 5
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i+batch_size]
        batch_chunks = splitter.split_documents(batch_docs)
        chunks.extend(batch_chunks)
        del batch_docs
        del batch_chunks
        gc.collect()

    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local("genshin_vector_db")
    
    # Clean up to free memory
    del chunks
    gc.collect()
    
    return vectordb

@lru_cache(maxsize=5)  # Cache frequent system prompts
def get_system_template():
    return """You are Akasha, a helpful and intelligent AI from Sumeru.
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

def setup_modern_rag_chain(vectorstore, groq_llm):
    # Create a retriever with fewer results to reduce processing
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    # Get system template
    system_template = get_system_template()
    
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

# Cap conversation history to prevent memory growth
def add_to_history(session_id: str, role: str, message: str):
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    history = conversation_histories[session_id]
    history.append((role, message))
    
    # Limit history to last 10 exchanges (20 entries)
    if len(history) > 20:
        conversation_histories[session_id] = history[-20:]

def chat_with_context(session_id, user_input):
    global rag_chain
    
    # Get or create conversation history
    if session_id not in conversation_histories:
        conversation_histories[session_id] = []
    
    conversation_history = conversation_histories[session_id]
    
    # Only include the most recent exchanges in the context
    recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
    
    # Format the conversation history for context (more efficiently)
    context_input = user_input
    if recent_history:
        context_parts = ["Previous conversation:"]
        for role, message in recent_history:
            context_parts.append(f"{role}: {message}")
        context_parts.append(f"Current question: {user_input}")
        context_input = "\n".join(context_parts)
    
    # Invoke the chain with the contextual input
    response = rag_chain.invoke(context_input)
    
    # Update the conversation history
    add_to_history(session_id, "User", user_input)
    add_to_history(session_id, "Akasha", response)
    
    return response

# Periodically clean up old sessions
def cleanup_old_sessions():
    # For a production app, implement session timeout logic
    # This is a simple placeholder - in reality, you'd track timestamps
    if len(conversation_histories) > 50:  # If we have too many sessions
        # Remove oldest sessions (this is simplified)
        oldest_sessions = list(conversation_histories.keys())[:10]
        for session_id in oldest_sessions:
            del conversation_histories[session_id]
        gc.collect()

# ------------------------------------------
# User Preferences API Endpoints
# ------------------------------------------
import threading
user_prefs_lock = threading.Lock()
USER_PREFS_PATH = 'data/user_preferences.json'

def load_user_prefs():
    if not os.path.exists(USER_PREFS_PATH):
        return {}
    with open(USER_PREFS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_user_prefs(prefs):
    with open(USER_PREFS_PATH, 'w', encoding='utf-8') as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)

class UserPreferences(BaseModel):
    userId: str
    favoriteCharacter: str
    favoriteRegion: str
    adventureRank: int
    mainTeam: list[str]
    preferredElement: str

@app.get("/api/user/preferences/{user_id}")
async def get_user_preferences(user_id: str):
    with user_prefs_lock:
        prefs = load_user_prefs()
    user = prefs.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return user

@app.post("/api/user/preferences")
async def save_user_preferences(preferences: UserPreferences):
    with user_prefs_lock:
        prefs = load_user_prefs()
        prefs[preferences.userId] = preferences.dict()
        save_user_prefs(prefs)
    return prefs[preferences.userId]

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
    
    # Clean up old sessions occasionally
    if len(conversation_histories) % 10 == 0:
        cleanup_old_sessions()
    
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
    gc.collect()  # Force garbage collection after deleting session
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
    # Use the PORT environment variable that Render provides
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
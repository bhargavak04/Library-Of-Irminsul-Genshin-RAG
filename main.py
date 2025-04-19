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

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
assert GROQ_API_KEY, "❌ Please set your GROQ_API_KEY in a .env file!"

# ------------------------------------------
# STEP 0: Initialize Groq LLM
# ------------------------------------------
groq_llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"  # You can adjust the model name based on availability
)

# ------------------------------------------
# STEP 1: Load and Prepare Documents
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
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        # Case 1: Files with a dict of objects keyed by name/id
        if isinstance(data, dict) and all(isinstance(v, dict) for v in data.values()):
            for key, val in data.items():
                content_parts = [
                    val.get("overview", ""),
                    val.get("lore", ""),
                    val.get("summary", "")
                ]

                # If it's a character-style object, extract details
                if "result" in val:
                    result = val["result"]
                    content_parts.extend([
                        f"Name: {result.get('name', '')}",
                        f"Title: {', '.join(result.get('title', []))}",
                        f"Real Name: {result.get('real_name', '')}",
                        f"Rarity: {result.get('rarity', '')}",
                        f"Weapon: {result.get('weapon', '')}",
                        f"Vision: {result.get('vision', '')}",
                        f"Birthday: {result.get('birthday', '')}",
                        f"Region: {', '.join(result.get('region', []))}",
                        f"Affiliation: {', '.join(result.get('affiliation', []))}",
                        f"Special Dish: {result.get('special_dish', '')}",
                        f"How to Obtain: {', '.join(result.get('how_to_obtain', []))}",
                        f"Release Date: {result.get('release_day', '')}",
                        f"Version: {result.get('release_version', '')}",
                        f"Category: {result.get('category', '')}",
                        f"Voice Actors: {json.dumps(result.get('voice_actors', []), ensure_ascii=False)}"
                    ])
                    url = result.get("wiki_url", "N/A")
                else:
                    url = val.get("url", "N/A")

                content = "\n".join([c for c in content_parts if c.strip()])
                if content:
                    docs.append(Document(page_content=content.strip(), metadata={"source": key, "url": url}))

        # Case 2: Single dictionary object like Teyvat lore
        elif isinstance(data, dict):
            content_parts = [
                f"Title: {data.get('title', '')}",
                f"Summary: {data.get('summary', '')}"
            ]
            content = "\n".join(content_parts).strip()
            if content:
                docs.append(Document(
                    page_content=content,
                    metadata={"source": data.get("title", "Unknown"), "url": data.get("url", "N/A")}
                ))

        # Case 3: List of entries (future-proofing)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    content = "\n".join([f"{k}: {v}" for k, v in item.items() if isinstance(v, str)])
                    docs.append(Document(page_content=content.strip(), metadata={"source": "list_item", "url": "N/A"}))

    return docs

# ------------------------------------------
# STEP 2: Chunking and Embedding
# ------------------------------------------
def create_vector_store(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local("genshin_vector_db")
    return vectordb

# ------------------------------------------
# STEP 3: Setup Modern RAG Chain
# ------------------------------------------
def setup_modern_rag_chain(vectorstore, groq_llm):
    # Create a retriever
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 8})
    
    # Define the system prompt
    system_template = """You are Akasha, a helpful and intelligent AI from Sumeru.
You are an expert on everything related to the world of Teyvat in Genshin Impact.

Your job is to answer user queries about characters, lore, locations, quests, and regions based on the context provided.
Be immersive and concise when needed, but also provide detailed insights if asked.

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

# ------------------------------------------
# STEP 4: Setup conversation history handling
# ------------------------------------------
def chat_with_context(conversation_history, user_input, rag_chain):
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
# STEP 5: Chat Loop
# ------------------------------------------
def chat_with_akasha(vectorstore, groq_llm):
    print("\n🌐 Akasha System Booted | Genshin Impact Lore Assistant")
    print("Ask me anything about characters, lore, regions, or quests.")
    print("Type 'exit' to quit.\n")

    rag_chain = setup_modern_rag_chain(vectorstore, groq_llm)
    conversation_history = []

    while True:
        user_input = input("🧑 You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("🔚 Session ended.")
            break

        response = chat_with_context(conversation_history, user_input, rag_chain)
        print(f"\n🤖 Akasha: {response}\n")

# ------------------------------------------
# ENTRY POINT
# ------------------------------------------
if __name__ == "__main__":
    if not os.path.exists("genshin_vector_db"):
        print("📦 Vector DB not found. Creating it from JSON data...")
        documents = load_documents()
        vectorstore = create_vector_store(documents)
    else:
        print("✅ Vector DB found. Loading from disk...")
        embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        # Adding the allow_dangerous_deserialization flag to fix the loading issue
        vectorstore = FAISS.load_local("genshin_vector_db", embeddings=embedder, allow_dangerous_deserialization=True)

    chat_with_akasha(vectorstore, groq_llm)
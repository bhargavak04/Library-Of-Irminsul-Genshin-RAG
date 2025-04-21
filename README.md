# Library of Irminsul

A comprehensive Genshin Impact data collection and retrieval system that scrapes information from the Genshin Impact Fandom Wiki and implements a Retrieval-Augmented Generation (RAG) system for intelligent querying of Genshin Impact lore.

## 📖 Overview

Library of Irminsul is named after the sacred tree in Genshin Impact that contains the memories and knowledge of Teyvat. This project aims to create a digital equivalent by:

1. Scraping comprehensive data from the Genshin Impact Fandom Wiki
2. Organizing and storing the data in structured JSON format
3. Implementing a RAG system using LangChain and Groq LLM for intelligent querying
4. Providing an interactive chat interface to explore Genshin Impact lore

## ✨ Features

### Web Scraping

- **Character Data Collection**: Scrapes detailed information about all playable characters including their lore, abilities, and background
- **General Wiki Scraping**: Collects data from various wiki sections including regions, factions, weapons, and more
- **Structured Data Storage**: Organizes all scraped data into well-structured JSON files for easy access

### Retrieval-Augmented Generation (RAG)

- **Vector Database**: Converts text data into embeddings stored in a FAISS vector database
- **Semantic Search**: Performs similarity-based retrieval to find the most relevant information
- **Context-Enhanced Generation**: Uses Groq LLM to generate accurate responses based on retrieved context
- **Conversation History**: Maintains chat history for contextual follow-up questions

## 🛠️ Technologies Used

### Backend
- **Python**: Core programming language
- **BeautifulSoup4**: For HTML parsing and web scraping
- **Requests**: For making HTTP requests to the wiki
- **LangChain**: Framework for building LLM applications
- **FAISS**: Vector database for efficient similarity search
- **Groq**: LLM provider for fast inference
- **HuggingFace Embeddings**: For text embedding generation
- **FastAPI**: For creating the REST API

### Frontend
- **React**: UI library for building the web interface
- **TypeScript**: Type-safe JavaScript for frontend development
- **Vite**: Build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for styling
- **React Router**: For client-side routing

## 📋 Data Sources

This project primarily scrapes data from the [Genshin Impact Fandom Wiki](https://genshin-impact.fandom.com/wiki), which is the most comprehensive source of Genshin Impact information. The specific pages scraped include:

- Character pages (e.g., https://genshin-impact.fandom.com/wiki/Character/List)
- Faction pages (e.g., https://genshin-impact.fandom.com/wiki/The_Seven)
- Region pages (e.g., https://genshin-impact.fandom.com/wiki/Mondstadt)
- Lore pages (e.g., https://genshin-impact.fandom.com/wiki/Timeline)
- And many more as listed in `Genshin_Scrape_List.txt`

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bhargavak04/Library-Of-Irminsul-Genshin-RAG
   cd Library_Of_Irminsul
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 💻 Usage

### Scraping Data

To scrape character data from the Genshin Impact Fandom Wiki:

```bash
python Scraping_Scripts/scrape_character_lore.py
```

To scrape general wiki sections:

```bash
python Scraping_Scripts/scrape_general_pages.py
```

### Running the RAG System

#### Command Line Interface
To start the interactive command-line chat interface:

```bash
python main.py
```

This will:
1. Load the scraped data
2. Create or load the vector database
3. Start an interactive chat session with Akasha (the AI assistant)

#### Web Application
To run the API server:

```bash
uvicorn app:app --reload
```

To run the frontend development server:

```bash
cd frontend
npm install
npm run dev
```

This will start the web interface where you can interact with Akasha through a modern UI.

## 📊 Project Structure

```
├── Scraping_Scripts/           # Scripts for web scraping
│   ├── fetch_chara.py          # Fetches character data from API
│   ├── scrape_character_lore.py # Scrapes character lore from wiki
│   ├── scrape_general_pages.py # Scrapes general wiki pages
│   └── scraper.py              # Core scraping functionality
├── data/                       # Stored JSON data
│   ├── character_lore.json     # Character lore information
│   ├── characters.json         # Character details
│   ├── lore.json               # General lore information
│   └── wiki_sections.json      # Various wiki section content
├── frontend/                   # React frontend application
│   ├── src/                    # Source code
│   │   ├── assets/             # Static assets
│   │   ├── pages/              # Page components
│   │   └── App.tsx             # Main application component
│   ├── package.json            # Frontend dependencies
│   └── vite.config.ts          # Vite configuration
├── main.py                     # CLI RAG implementation
├── app.py                      # FastAPI backend server
├── requirements.txt            # Project dependencies
└── Genshin_Scrape_List.txt     # List of URLs to scrape
```

## 🔮 Future Improvements

- Add more data sources beyond the Fandom Wiki
- Implement a web interface for easier interaction
- Add support for image retrieval and analysis
- Expand to other languages beyond English
- Implement regular data updates to keep information current

## 📝 License

This project is for educational purposes only. All Genshin Impact content belongs to HoYoverse.

## 🙏 Acknowledgements

- [Genshin Impact Fandom Wiki](https://genshin-impact.fandom.com/wiki) for the comprehensive data
- HoYoverse for creating Genshin Impact
- The LangChain and Groq teams for their excellent tools

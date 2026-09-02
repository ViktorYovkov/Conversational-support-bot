# Eliza - Enterprise AI Chat Assistant

A production-ready AI chat assistant built for Sirma. Eliza uses a custom Retrieval-Augmented Generation (RAG) pipeline to provide accurate, domain-specific answers based on verified corporate data, ensuring zero hallucinations.

## Key Features
* **RAG Architecture**: Semantic search through company knowledge using ChromaDB.
* **Conversational Memory**: Secure, UUID-based session tracking with an optimized SQLite rolling horizon.
* **Dynamic Tool Calling**: Automated escalation to human support for out-of-scope queries.
* **Premium UI**: Built with React & Vite, featuring live Markdown parsing, glassmorphism aesthetics, and custom CSS micro-interactions.

## Tech Stack
* **Frontend**: React, Vite, CSS3, `react-markdown`
* **Backend**: FastAPI, Python
* **AI & Data**: OpenAI API (`gpt-4o-mini`), ChromaDB (Vector DB), SQLite (Relational DB)

## Quick Start:

### Backend Setup:
1. Navigate to the backend directory and set up the Python environment:
```bash
cd Backend
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```
2. Create a .env file in the root of the Backend folder and add your API key:
```bash
OpenAI_API_KEY=your_openai_api_key_here
```
3. Start the FastAPI server:
```bash
uvicorn main:app --reload
```
### Frontend Setup
1. Open a new terminal window, navigate to the frontend directory, and start the Vite development server:
```bash
cd frontend
npm install
npm run dev
```
### Managing the knowledge base:
Eliza's knowledge is driven by a local text file. To update the information:
1. Edit the FAQ.txt file in the Backend folder. Ensure distinct Q&A blocks or case studies are separated by a double newline.
2. Regenerate the vector database by running the embedding script:
```bash
python vector_db.py
```


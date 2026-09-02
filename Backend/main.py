from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_agent import generate_response
from database import save_message
from database import init_db

app = FastAPI(title="Eliza AI Sirma Assistant")

# Създаваме базата в мига, в който пуснем сървъра:
@app.on_event("startup")

def startup_event():
    init_db() 

# Комуникация с фронтенда с React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")

def chat_endpoint(request: ChatRequest):
    try:
        save_message(request.session_id, "user", request.message)
        reply = generate_response(request.session_id, request.message)
        save_message(request.session_id, "bot", reply)
        return {"reply": reply}

    except Exception as e:
        print(f"Грешка при обработка на заявката: {e}")
        raise HTTPException(status_code=500, detail="Грешка при обработка на заявката")

@app.get("/")

def read_root():
    return {"message": "Eliza AI Sirma Assistant е активна."}


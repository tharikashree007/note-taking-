from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as NoteRouter

app = FastAPI(title="Note Taking App API")

# Setup CORS for frontend access
origins = [
    "http://localhost:5173", # standard vite port
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(NoteRouter, tags=["Note"], prefix="/notes")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Note Taking Backend!"}

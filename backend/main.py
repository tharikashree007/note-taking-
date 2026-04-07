from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as NoteRouter

app = FastAPI(title="Note Taking App API")

# ✅ CORS configuration (LOCAL + PRODUCTION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://note-taking-five-wheat.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routes
app.include_router(NoteRouter, tags=["Note"], prefix="/notes")


# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Note Taking Backend!"}
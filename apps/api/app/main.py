from fastapi import FastAPI

from app.api.repositories import router as repositories_router
from app.api.search import router as search_router
from app.api.ask import router as ask_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="OnboardAI API",
    description="Backend API for the OnboardAI codebase onboarding platform.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "onboardai-api",
    }


app.include_router(repositories_router)
app.include_router(search_router)
app.include_router(ask_router)
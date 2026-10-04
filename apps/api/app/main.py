from fastapi import FastAPI

from app.api.repositories import router as repositories_router
from app.api.search import router as search_router
from app.api.ask import router as ask_router


app = FastAPI(
    title="OnboardAI API",
    description="Backend API for the OnboardAI codebase onboarding platform.",
    version="0.1.0",
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
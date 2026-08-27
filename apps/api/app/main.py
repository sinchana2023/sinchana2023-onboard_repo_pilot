from fastapi import FastAPI

from app.api.repositories import router as repositories_router


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
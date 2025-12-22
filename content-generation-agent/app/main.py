from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Content Generation Agent",
    description="Backend API for AI content generation",
    version="0.1.0"
)

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

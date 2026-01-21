from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, documents, tax, wealth

app = FastAPI(
    title="Tax Filing Automation System",
    description="AI-Powered Tax Filing for Pakistan with RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(tax.router, prefix="/api/tax", tags=["Tax Calculation"])
app.include_router(wealth.router, prefix="/api/wealth", tags=["Wealth Statement"])

@app.get("/")
async def root():
    return {
        "message": "Tax Filing Automation System API with RAG",
        "version": "1.0.0",
        "status": "running",
        "features": ["Authentication", "Tax Calculation", "Document OCR", "AI Chatbot with RAG", "Wealth Statement"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected", "rag": "enabled"}

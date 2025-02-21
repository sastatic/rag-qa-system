from fastapi import FastAPI
from api import documents, qa

app = FastAPI(title="RAG Q&A System")

# Include the API routers with prefixes for clarity.
# app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(qa.router, prefix="/qa", tags=["qa"])

# Optionally add a root endpoint for a quick check
@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Q&A System"}

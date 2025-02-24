# app/services/qa_service.py

import numpy as np
import os
from sqlalchemy.orm import Session
from llama_index.core.embeddings import resolve_embed_model
from llama_index.llms.ollama import Ollama
from common.config import OLLAMA_MODEL, EMBED_MODEL
from models import Question, Answer
from repositories.document_repository import DocumentRepository
from common import get_logger
from fastapi import HTTPException

logger = get_logger(__name__)

prompt = """You are an AI answering user questions based on the provided documents.

Context:
{context}

Question: {query_text}

Answer:
"""

class QAService:
    def __init__(self, db: Session):
        self.db = db
        self.document_repo = DocumentRepository(db)
        self.embed_model = resolve_embed_model(embed_model=EMBED_MODEL)
        self.llm = Ollama(
            model=OLLAMA_MODEL,
            request_timeout=60.0,
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        )
    
    async def search_within_documents(self, query_text: str, document_ids: list, top_n: int = 10):
        query_embedding = self.embed_model.get_text_embedding(query_text)
        # Fetch documents using the repository; you can also use self.db directly if preferred.
        documents = self.document_repo.get_all_documents(document_ids)
        logger.info("%s documents found.", len(documents))
        if not documents:
            return []
        doc_scores = []
        for doc in documents:
            if doc.embedding is None:
                logger.info("Doc embedding is none here.")
                continue 
            similarity = np.dot(doc.embedding, query_embedding)
            doc_scores.append((similarity, doc))
        doc_scores.sort(reverse=True, key=lambda x: x[0])
        doc_scores_slice = [doc for _, doc in doc_scores[:top_n]]
        return doc_scores_slice

    async def get_context(self, question: Question):
        relevant_docs = await self.search_within_documents(question.query, question.selected_document)
        if not relevant_docs:
            raise HTTPException(status_code=404, detail={"message": "No relevant information found in the selected documents."})
        return "\n\n".join([f"{doc.title}:\n{doc.content[:1000]}" for doc in relevant_docs])

    async def generate_answer(self, question: Question) -> Answer:
        logger.info("Generating answer for question: %s", question.query)
        context = ""
        if question.selected_document is not None:
            context = await self.get_context(question)
        new_prompt = prompt.format(context=context, query_text=question.query)
        try:
            response_text = self.llm.complete(new_prompt).text  # synchronous call
        except Exception as e:
            logger.error("LLM call failed or timed out: %s", str(e))
            raise HTTPException(status_code=400, detail={"message": "An error occurred while generating an answer. Please try again later."})
        return Answer(answer=response_text)

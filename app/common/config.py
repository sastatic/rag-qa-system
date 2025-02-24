import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
VECTOR_DB = os.getenv("VECTOR_DB", "faiss")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_RAGQA = os.getenv("BUCKET_RAGQA")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
EMBED_MODEL = os.getenv("EMBED_MODEL")
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_URL = os.getenv("REDIS_URL", "6379")
OLLAMA_HOST = os.getenv("OLLAMA_HOST")

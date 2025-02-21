import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
VECTOR_DB = os.environ.get("VECTOR_DB", "faiss")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SECRET_KEY = os.environ.get("SECRET_KEY")
API_KEY = os.environ.get("API_KEY")

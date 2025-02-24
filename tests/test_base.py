import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from main import app  # type: ignore

class TestBaseClass:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)

from test_base import TestBaseClass

class TestQAEndpoints(TestBaseClass):

    def test_get_answer_success(self):
        request_body = {
            "query": "What is this assignment about?",
            "selected_document": ["01JMWC5FQM5NEGAM1T8M1A1N6V"]
        }
        response = self.client.post("/qa", json=request_body)
        assert response.status_code == 200

        data = response.json()
        assert "answer" in data
        assert data["answer"]

    def test_get_answer_no_documents(self):
        request_body = {
            "query": "Valid question",
            "selected_document": []
        }
        response = self.client.post("/qa", json=request_body)
        assert response.status_code == 404

    def test_get_answer_complex_query(self):
        request_body = {
            "query": "Explain in detail how the ingestion workflow is designed, focusing on database persistence and embedding generation.",
        }
        response = self.client.post("/qa", json=request_body)
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data

    def test_get_answer_invalid_document_id(self):
        request_body = {
            "query": "Any question",
            "selected_document": ["fake_doc_id_123"]
        }
        response = self.client.post("/qa", json=request_body)
        assert response.status_code == 404

    def test_get_answer_empty_query(self):
        request_body = { "query": "" }
        response = self.client.post("/qa", json=request_body)
        assert response.status_code == 422

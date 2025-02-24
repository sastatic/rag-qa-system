from test_base import TestBaseClass


class TestDocumentIngestion(TestBaseClass):
    def test_ingest_documents_success(self):
        files = [
            ("files", ("test_doc.txt", b"Hello, world!", "text/plain")),
        ]
        response = self.client.post("/documents", files=files)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "id" in data[0]
        assert "file_name" in data[0]

    def test_ingest_documents_no_files(self):
        response = self.client.post("/documents", files=[])
        # FastAPI returns a 422 error when required file fields are missing.
        assert response.status_code == 422

    def test_ingest_documents_unsupported_file_type(self):
        files = [
            (
                "files",
                ("malicious.exe", b"Pretend binary data", "application/octet-stream"),
            ),
        ]
        response = self.client.post("/documents", files=files)
        assert response.status_code == 500

    def test_ingest_documents_too_large(self):
        big_content = b"A" * (10 * 1024 * 1024)  # 10 MB
        files = [
            ("files", ("big_file.txt", big_content, "text/plain")),
        ]
        response = self.client.post("/documents", files=files)
        assert response.status_code == 200

    def test_ingest_multiple_documents_success(self):
        files = [
            ("files", ("doc1.txt", b"First file content", "text/plain")),
            ("files", ("doc2.txt", b"Second file content", "text/plain")),
        ]
        response = self.client.post("/documents", files=files)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert "id" in data[0] and "file_name" in data[0]
        assert "id" in data[1] and "file_name" in data[1]


class TestDocumentRetrieval(TestBaseClass):
    def test_list_documents(self):
        response = self.client.get("/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

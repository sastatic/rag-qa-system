### Sequence Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant DI as Document Ingestion API
    participant Q as Queue
    participant BP as Background Processor
    participant DB as Document/Embedding Store
    participant DS as Document Selection API
    participant QA as Q&A API
    participant R as RAG Engine

    %% Document Ingestion Flow with Background Processing
    U ->> DI: Upload Document
    DI ->> U: Return Acknowledgment (202 Accepted)
    DI ->> Q: Enqueue Document for Processing
    Q ->> BP: Dispatch Document for Processing
    BP ->> BP: Validate Document & Generate Embedding
    alt Validation Successful
        BP ->> DB: Store Document & Embeddin
        DB -->> BP: Acknowledge Storage
        BP -->> Q: Acknowledge Completion
    else Validation Failed
        BP -x BP: Log Error
        BP -->> Q: Notify Failure
    end

    Status ->> WH: Notify Client of Job Status Change
    %% Client later polls job status or receives notification:
    %%U ->> Status: Poll Job Status (using Job ID)
    %%Status -->> U: Return Job Status (Success/Failure with details)

    %% Document Selection Flow
    U ->> DS: Specify/Select Documents
    DS ->> DB: Retrieve/Update Document Selection
    DB -->> DS: Return Selection Data
    DS -->> U: Confirm Document Selection

    %% Q&A Flow
    U ->> QA: Submit Question
    QA ->> DB: Retrieve Relevant Documents
    DB -->> QA: Return Document Data
    QA ->> R: Send Question + Documents
    R ->> R: Preprocess Data & Generate Answer
    R -->> QA: Return Generated Answer
    QA -->> U: Return Final Answer
```

### HLD
```mermaid
graph LR
    U[User] -->|Authenticated & Rate Limited Requests| API[API Gateway]
    API --> DI[Document Ingestion Service]
    API --> DS[Document Selection Service]
    API --> QA[Q&A Service]
    
    DI -->|Enqueue| Q[Message Queue]
    Q --> BP[Background Processor]
    BP -->|Validate & Generate Embedding| VDB[Vector Database]
    BP --> Status[Job Status Service]
    Status -->|Persist Status| DB[(PostgreSQL)]
    Status -->|Webhook Notifications - Job Completion / Failure|U

    DS --> VDB
    QA --> VDB
    QA --> R[RAG Engine]
    R --> QA
```


### Project Structure
```
app
├── api
│   ├── __init__.py
│   ├── documents.py
│   └── qa.py
├── common
│   ├── __init__.py
│   ├── config.py
│   ├── health_check.py
│   └── logger.py
├── database
│   ├── models
│   │   ├── __init__.py
│   │   └── document.py
│   ├── __init__.py
│   ├── base.py
│   ├── s3.py
│   └── session.py
├── models
│   ├── __init__.py
│   ├── document.py
│   └── qa.py
├── repositories
│   └── document_repository.py
├── services
│   ├── __init__.py
│   ├── document_processor.py
│   ├── document_service.py
│   └── qa_service.py
├── README.md
├── main.py
├── pyproject.toml
├── start.sh
└── worker.py
```

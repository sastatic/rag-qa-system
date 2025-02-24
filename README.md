## Diagrams
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

## Deployment

This section provides step-by-step instructions to deploy the application locally or in a production-like environment using Docker. The deployment process ensures that all services—from the Document Ingestion API to the RAG-based Q&A service—are containerized, making the solution portable and scalable.

Prerequisites
1. Docker: Ensure Docker is installed
2. Docker Compose: Install Docker Compose.
3. Environment Variables: Review and update the configuration in example.env.

#### Step 1: Clone the Repository
#### Step 2: Configure Environment Variables
1. Rename example.env to .env.
2. Update the necessary environment variables (e.g., database connection details, secret keys).

#### Step 3: Build Docker Images
`docker compose build`

#### Step 4: Run the Application
`docker compose up -d`

#### Step 5: Database Migrations

Run the following command to upgrade the database schema:
`docker compose exec api alembic upgrade head`

#### Step 6: Monitoring and Logs

To monitor the application logs, use:
`docker compose logs -f`


#### Step 7: Stopping the Application

`docker compose down`

### CI/CD Integration

To streamline deployments:
- Automated Testing: Integrate your test suite into your CI/CD pipeline to run on each commit.
- Build & Push: Configure your CI/CD system (e.g., GitHub Actions, GitLab CI) to build Docker images and push them to a container registry.
- Automated Deployment: Use deployment scripts to update your production environment automatically upon successful builds.

Troubleshooting
- Container Health: Verify running containers with docker ps.
- Environment Variables: Double-check that the .env file is configured correctly.
- Logs: Use docker-compose logs -f to identify any runtime errors.

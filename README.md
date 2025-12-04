
# Knowledge Graph Backend - Development Guide

> Clean Architecture Backend with FastAPI, GraphDB & SPARQL | TDD + SOLID Principles

## 🏗️ Architecture Overview

This backend follows **Clean Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
│  (FastAPI Routers, Middleware, DTOs)                        │
├─────────────────────────────────────────────────────────────┤
│                    Application Layer                         │
│  (Use Cases/Services, Business Logic)                       │
├─────────────────────────────────────────────────────────────┤
│                      Domain Layer                            │
│  (Entities, Repository Interfaces)                          │
├─────────────────────────────────────────────────────────────┤
│                  Infrastructure Layer                        │
│  (GraphDB Repositories, SPARQL Queries)                     │
└─────────────────────────────────────────────────────────────┘
```

### SOLID Principles Implementation

| Principle | Implementation |
|-----------|---------------|
| **Single Responsibility** | Each service handles one business capability |
| **Open/Closed** | Repository interfaces allow new implementations |
| **Liskov Substitution** | Mock/Real repositories are interchangeable |
| **Interface Segregation** | Focused repository interfaces (IEntityRepository, etc.) |
| **Dependency Inversion** | Services depend on interfaces, not implementations |

## 📁 Project Structure

```
Peladen/
├── app/
│   ├── domain/                      # Enterprise Business Rules
│   │   ├── models/
│   │   │   ├── entities.py         # Domain models (Entity, HealthRecord)
│   │   │   └── __init__.py         # Exports
│   │   └── repositories/
│   │       ├── interfaces.py       # Repository contracts (IEntityRepository)
│   │       └── __init__.py
│   │
│   ├── application/                 # Application Business Rules
│   │   ├── services/
│   │   │   ├── use_cases.py        # Business logic services
│   │   │   └── __init__.py
│   │   ├── dto/
│   │   │   ├── schemas.py          # API request/response models
│   │   │   └── __init__.py
│   │   └── mappers.py              # Domain ↔ DTO conversion
│   │
│   ├── infrastructure/              # Frameworks & Drivers
│   │   ├── repositories/
│   │   │   ├── graphdb_repository.py    # GraphDB implementation
│   │   │   ├── additional_repositories.py
│   │   │   └── __init__.py
│   │   └── config/
│   │       ├── settings.py         # Configuration management
│   │       └── __init__.py
│   │
│   ├── presentation/                # Interface Adapters
│   │   ├── routers/
│   │   │   ├── search_router.py    # /api/search endpoints
│   │   │   ├── entity_router.py    # /api/entities endpoints
│   │   │   ├── map_router.py       # /api/map endpoints
│   │   │   ├── sparql_router.py    # /api/sparql endpoints
│   │   │   └── __init__.py
│   │   ├── middleware/
│   │   │   ├── error_handler.py    # Exception handling
│   │   │   └── __init__.py
│   │   └── dependencies.py         # DI Container
│   │
│   ├── data/
│   │   └── country_coordinates.py  # Static data
│   │
│   └── main.py                      # Application entry point
│
├── tests/
│   ├── unit/
│   │   ├── test_models.py          # Domain model tests
│   │   └── test_services.py        # Service tests
│   └── integration/
│       └── test_api.py             # API endpoint tests
│
├── .env.example                     # Environment template
├── requirements.txt                 # Dependencies
├── pytest.ini                       # Test configuration
├── docker-compose.yml               # Docker orchestration
├── Dockerfile                       # Container definition
└── setup.py                         # Development setup script
```

## 🚀 Quick Start
```sh
# 1. Clone and navigate to backend
cd Peladen

# 2. Run automated setup (creates .env, installs deps)
python setup.py

# 3. Or manual setup:
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your settings
```

### Environment Configuration

Edit `.env` file with your settings:


```env
# GraphDB Configuration
GRAPHDB_URL=http://localhost:7200
SPARQL_ENDPOINT=http://localhost:7200/repositories/knowledge-graph

# API Configuration
API_HOST=0.0.0.0
API_PORT=3000

# CORS (Frontend URL)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

### Start GraphDB & Load Data
```sh
# Start GraphDB with Docker
docker-compose up -d graphdb

# Access GraphDB Workbench
# http://localhost:7200

# Create repository named: knowledge-graph
# Import RDF files:
#   - ../rdf/entity.ttl
#   - ../rdf/property.ttl
#   - ../rdf/health_record.ttl
```

### Run Tests (TDD Approach)
```sh
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py -v

# Run only unit tests
pytest tests/unit/

# Open coverage report
# htmlcov/index.html
```

### Start Development Server
```sh
uvicorn app.main:app --reload --port 3000

# Alternative: with hot-reload and log level
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000 --log-level info
```

### Access API Documentation

- **Swagger UI**: http://localhost:3000/api/docs
- **ReDoc**: http://localhost:3000/api/redoc
- **OpenAPI Schema**: http://localhost:3000/api/openapi.json
- **Health Check**: http://localhost:3000/health

### Docker Deployment
```sh
# Start all services (Backend + GraphDB)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build backend
```

## 🔌 API Endpoints Reference

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search` | Search entities with filters |
| GET | `/api/search/suggestions` | Autocomplete suggestions |

**Example:**
```sh
curl "http://localhost:3000/api/search?query=indonesia&type=country&page=1&pageSize=10"
```

### Entity Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/entities/{id}` | Get entity with health records |
| GET | `/api/entity/{id}` | Get complete entity info (InfoBox) |
| GET | `/api/entity/by-label` | Search entity by label |
| GET | `/api/entity/related` | Get related entities |

**Example:**
```sh
curl "http://localhost:3000/api/entity/http%3A%2F%2Fwww.wikidata.org%2Fentity%2FQ252"
```

### Map Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/map/countries` | Get all country coordinates |
| GET | `/api/map/countries/{iso3}` | Get country by ISO3 code |

### SPARQL Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sparql/query` | Execute SPARQL query |
| POST | `/api/sparql/validate` | Validate query syntax |
| GET | `/api/sparql/samples` | Get sample queries |
| GET | `/api/sparql/history` | Query execution history |

**Example:**
```sh
curl -X POST "http://localhost:3000/api/sparql/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10",
    "format": "json"
  }'
```

## 🧪 Test-Driven Development (TDD) Workflow

### 1. Write Test First (Red Phase)
```python
# tests/unit/test_services.py
@pytest.mark.asyncio
async def test_search_filters_short_queries():
    service = SearchService(mock_repo)
    result = await service.get_suggestions("a")
    assert result == []  # Should return empty for short queries
```

### 2. Implement Minimum Code (Green Phase)
```python
# app/application/services/use_cases.py
async def get_suggestions(self, query: str) -> List[Entity]:
    if len(query) < 2:
        return []
    return await self.entity_repo.get_suggestions(query)
```

### 3. Run Tests
```sh
pytest tests/unit/test_services.py::test_search_filters_short_queries -v
```

### 4. Refactor & Improve (Blue Phase)

After tests pass, refactor code for better quality while keeping tests green.

## 🛠️ Adding New Features

Follow this workflow to add new features:

### Step 1: Define Domain Model
```python
# app/domain/models/entities.py
@dataclass
class NewEntity:
    id: str
    name: str
    # Add fields
```

### Step 2: Create Repository Interface
```python
# app/domain/repositories/interfaces.py
class INewRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[NewEntity]:
        pass
```

### Step 3: Implement Repository with SPARQL
```python
# app/infrastructure/repositories/new_repository.py
class NewRepository(INewRepository):
    def __init__(self, client: GraphDBClient):
        self.client = client
    
    async def get_by_id(self, id: str) -> Optional[NewEntity]:
        sparql_query = f"""
        SELECT ?name WHERE {{
            <{id}> rdfs:label ?name .
        }}
        """
        results = await self.client.query(sparql_query)
        # Parse and return
```

### Step 4: Create Service (Use Case)
```python
# app/application/services/use_cases.py
class NewService:
    def __init__(self, repo: INewRepository):
        self.repo = repo
    
    async def get_entity(self, id: str) -> Optional[NewEntity]:
        return await self.repo.get_by_id(id)
```

### Step 5: Create DTO Schema
```python
# app/application/dto/schemas.py
class NewEntityDTO(BaseModel):
    id: str
    name: str
```

### Step 6: Create Router (Controller)
```python
# app/presentation/routers/new_router.py
router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("/{id}", response_model=NewEntityDTO)
async def get_new_entity(
    id: str,
    service: NewService = Depends(get_new_service)
):
    entity = await service.get_entity(id)
    if not entity:
        raise HTTPException(404, "Not found")
    return NewEntityDTO(id=entity.id, name=entity.name)
```

### Step 7: Register in Dependency Container
```python
# app/presentation/dependencies.py
def get_new_service() -> NewService:
    return NewService(get_new_repository())
```

### Step 8: Include Router in Main App
```python
# app/main.py
from app.presentation.routers import new_router
app.include_router(new_router.router, prefix="/api")
```

## 🔍 Code Quality & Standards

### Code Formatting
```sh
# Format code with Black
black app/ tests/

# Sort imports
isort app/ tests/

# Type checking
mypy app/

# Linting
flake8 app/
```

### Naming Conventions

- **Files**: `snake_case.py` (e.g., `use_cases.py`, `entities.py`)
- **Classes**: `PascalCase` (e.g., `SearchService`, `EntityRepository`)
- **Functions/Methods**: `snake_case` (e.g., `get_entity_info`, `search_entities`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `GRAPHDB_URL`, `MAX_RESULTS`)
- **Interfaces**: Prefix with `I` (e.g., `IEntityRepository`, `ISPARQLRepository`)

## 🐛 Debugging Tips

### Enable Debug Logging
```env
LOG_LEVEL=DEBUG
```

### View SPARQL Queries

All SPARQL queries are logged. Check logs to see exact queries being executed.

### Test Individual Components
```python
# Test repository directly
from app.infrastructure.repositories.graphdb_repository import GraphDBClient, EntityRepository

client = GraphDBClient("http://localhost:7200/repositories/knowledge-graph")
repo = EntityRepository(client)

# Test query
entities, total = await repo.search("indonesia", limit=10)
print(f"Found {total} entities")
```

## 🔗 Integration with Frontend

Update frontend `.env` to connect to backend:
```env
# fe-kg-gaung/.env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_API_TIMEOUT=30000
```

Update frontend services to use real API:
```ts
// fe-kg-gaung/src/services/search.service.ts
const USE_MOCK = false; // Change to false to use real backend
```

## 📊 Performance Tips

### Connection Pooling

GraphDB client uses connection pooling by default via SPARQLWrapper.

### Query Optimization

- Add `LIMIT` clauses to prevent large result sets
- Use specific SPARQL patterns instead of broad queries
- Index commonly queried properties in GraphDB

### Caching (Future Enhancement)

Consider adding Redis for:
- Frequently accessed entities
- Search results
- SPARQL query results

## 🚨 Common Issues & Solutions

### Issue: "Connection refused to GraphDB"

**Solution:**
```sh
# Check if GraphDB is running
docker-compose ps

# Restart GraphDB
docker-compose restart graphdb

# Check GraphDB logs
docker-compose logs graphdb
```

### Issue: "Repository 'knowledge-graph' not found"

**Solution:** Create repository in GraphDB Workbench (http://localhost:7200)

### Issue: "CORS errors from frontend"

**Solution:** Check `CORS_ORIGINS` in `.env` includes frontend URL

### Issue: "Module not found" errors

**Solution:**
```sh
# Ensure all __init__.py files exist
find app -type d -exec touch {}/__init__.py \;

# Reinstall dependencies
pip install -r requirements.txt
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **GraphDB Documentation**: https://graphdb.ontotext.com/documentation/
- **SPARQL Tutorial**: https://www.w3.org/TR/sparql11-query/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **SOLID Principles**: https://en.wikipedia.org/wiki/SOLID

## 📝 License

MIT License

---

**Built with ❤️ following Clean Architecture, SOLID Principles, and TDD**

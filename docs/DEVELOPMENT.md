# MDOP Development Guide

Dieser Guide hilft Entwicklern bei der Arbeit mit der MDOP-Plattform.

## Quick Start

### Voraussetzungen

- Docker 24+ & Docker Compose
- Python 3.11+
- Git

### Lokales Setup

1. **Repository klonen**
```bash
git clone <repository-url>
cd Modularen-Daten-Ontologie-Plattform-MDOP-
```

2. **Plattform starten**
```bash
./scripts/start.sh
```

3. **API testen**
```bash
curl http://localhost:8000/health
```

4. **API-Dokumentation öffnen**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Architektur-Übersicht

### Komponenten

1. **Neo4j** (Port 7474, 7687) - Graph-Datenbank für Entitäten und Beziehungen
2. **PostgreSQL** (Port 5432) - Relationale DB für Metadaten und Konfiguration
3. **Redis** (Port 6379) - Cache für Performance-Optimierung
4. **Elasticsearch** (Port 9200) - Full-Text-Search
5. **Kafka** (Port 9092) - Message Queue für asynchrone Verarbeitung
6. **Backend API** (Port 8000) - FastAPI REST API

### Datenfluss

```
External Data Sources
        ↓
   Data Connectors (ETL)
        ↓
   Schema Mapping
        ↓
Neo4j Graph Database ← → Backend API ← → Frontend
        ↑                     ↑
        └───── Redis Cache ───┘
```

## Entwicklung

### Backend-Entwicklung

#### Neue API-Endpunkte erstellen

1. Schema in `app/schemas/` definieren:
```python
from pydantic import BaseModel

class MySchema(BaseModel):
    name: str
    value: int
```

2. Service-Logik in `app/services/` implementieren
3. API-Router in `app/api/` erstellen
4. Router in `app/api/router.py` registrieren

#### Datenbank-Modelle

**PostgreSQL ORM-Modelle** (`app/models/`):
```python
from app.db.postgres_client import Base
from sqlalchemy import Column, String, Integer

class MyModel(Base):
    __tablename__ = "my_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

**Neo4j Cypher Queries** (über `neo4j_client`):
```python
from app.db.neo4j_client import neo4j_client

query = """
MATCH (n:Person)-[:WORKS_AT]->(c:Company)
WHERE n.name = $name
RETURN n, c
"""
result = neo4j_client.execute_read(query, {"name": "John"})
```

### Neuen Data Connector implementieren

1. Von `BaseConnector` erben:
```python
from app.services.connectors.base_connector import BaseConnector

class MyConnector(BaseConnector):
    async def connect(self) -> bool:
        # Verbindung herstellen
        pass
    
    async def fetch_data(self, full_sync: bool, batch_size: int):
        # Daten abrufen
        pass
```

2. Abstrakte Methoden implementieren:
   - `connect()` - Verbindung herstellen
   - `disconnect()` - Verbindung trennen
   - `test_connection()` - Verbindung testen
   - `detect_schema()` - Schema erkennen
   - `fetch_data()` - Daten abrufen

3. Connector registrieren und verwenden

### Testing

```bash
# Backend Tests
cd backend
pytest tests/ -v

# Mit Coverage
pytest tests/ --cov=app --cov-report=html

# Spezifische Tests
pytest tests/test_ontology.py -v
```

### Logging

Logs werden strukturiert ausgegeben:

```python
from app.core.logging import logger

logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
```

Im Development: Formatiertes Log
In Production: JSON-Format für Log-Aggregation

## API-Nutzung

### Ontologie-Management

#### Entity Type erstellen
```bash
curl -X POST http://localhost:8000/api/v1/ontology/entity-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Person",
    "label": "Person",
    "description": "A human being",
    "properties": {
      "name": {"type": "string"},
      "age": {"type": "integer"},
      "email": {"type": "string"}
    },
    "icon": "user",
    "color": "#3B82F6"
  }'
```

#### Entity erstellen
```bash
curl -X POST http://localhost:8000/api/v1/ontology/entities \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Person",
    "properties": {
      "name": "John Doe",
      "age": 30,
      "email": "john@example.com"
    }
  }'
```

#### Relationship Type erstellen
```bash
curl -X POST http://localhost:8000/api/v1/ontology/relationship-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WORKS_AT",
    "label": "Works At",
    "from_entity_type_id": 1,
    "to_entity_type_id": 2,
    "is_directed": true
  }'
```

### Data Connector Setup

1. **Connector konfigurieren** (PostgreSQL-Beispiel):
```python
connector_config = {
    "host": "source-db.example.com",
    "port": 5432,
    "database": "mydb",
    "user": "readonly_user",
    "password": "secret"
}

mapping = {
    "source_table": "users",
    "entity_type": "Person",
    "field_mappings": {
        "name": "full_name",
        "email": "email_address",
        "age": "user_age"
    }
}
```

2. **Sync ausführen**:
```python
from app.services.connectors.postgresql_connector import PostgreSQLConnector

connector = PostgreSQLConnector("my-pg-connector", connector_config, mapping)
result = await connector.sync(full_sync=True)

print(f"Processed: {result.records_processed}")
print(f"Failed: {result.records_failed}")
```

## Troubleshooting

### Backend startet nicht

1. **Ports belegt?**
```bash
lsof -i :8000  # Check if port 8000 is in use
```

2. **Datenbank-Verbindung fehlgeschlagen?**
```bash
docker-compose logs neo4j
docker-compose logs postgres
```

3. **Logs prüfen**:
```bash
docker-compose logs -f backend
```

### Neo4j Connection Error

```bash
# Neo4j Health Check
curl http://localhost:7474

# Neo4j Browser
open http://localhost:7474
# Default credentials: neo4j / mdop_neo4j_password
```

### Datenbank zurücksetzen

```bash
# WARNUNG: Löscht alle Daten!
docker-compose down -v
docker-compose up -d
```

## Performance-Optimierung

### Query-Performance

1. **Indexes nutzen**:
```python
# Automatisch bei Startup erstellt
neo4j_client.create_indexes()
```

2. **Batch-Processing**:
```python
# Große Datenmengen in Batches verarbeiten
async for batch in connector.fetch_data(batch_size=1000):
    process_batch(batch)
```

3. **Caching**:
```python
from app.db.redis_client import redis_client

# Cache read
cached = redis_client.get("key")
if not cached:
    result = expensive_operation()
    redis_client.set("key", result, expire=300)
```

### Graph Query Optimization

- **Limit Graph Depth**: Tiefe Traversierungen vermeiden
- **Index Properties**: Häufig gesuchte Properties indizieren
- **Projection**: Nur benötigte Felder zurückgeben
- **Parameters**: Immer Cypher Parameters nutzen (SQL-Injection-Schutz)

```cypher
// Good
MATCH (n:Person {id: $id})
RETURN n.name, n.email

// Bad (langsam, unsicher)
MATCH (n:Person)
WHERE n.id = '123'
RETURN n
```

## Best Practices

### Code-Style

- **PEP 8** für Python-Code
- **Type Hints** für alle Funktionen
- **Docstrings** für alle Public APIs
- **Tests** für neue Features

### Security

- **Niemals** Secrets im Code
- **Immer** `.env` für Konfiguration
- **Password-Hashing** für User-Credentials
- **Input-Validierung** mit Pydantic
- **Rate-Limiting** für APIs

### Git Workflow

```bash
# Feature Branch
git checkout -b feature/my-feature

# Commit Messages (conventional commits)
git commit -m "feat: add new connector for MongoDB"
git commit -m "fix: resolve connection timeout issue"
git commit -m "docs: update API documentation"

# Push
git push origin feature/my-feature
```

## Nächste Schritte (Phase 2)

- [ ] React Frontend mit D3.js Visualisierung
- [ ] WebSocket für Real-Time Updates
- [ ] Erweiterte Query Builder UI
- [ ] ABAC Security Implementation
- [ ] Data Lineage Visualization

## Ressourcen

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)

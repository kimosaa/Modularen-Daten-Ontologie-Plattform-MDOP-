# Modulare Daten-Ontologie-Plattform (MDOP)

Eine Palantir-inspirierte, hoch skalierbare Datenplattform zur Integration, Modellierung und Analyse heterogener Datenquellen durch flexible, Graph-basierte Ontologien.

## 🎯 Projektziel

Aufbau einer Enterprise-Grade Datenplattform, die komplexe Beziehungen und Muster in Daten durch eine flexible, Graph-basierte Ontologie aufdeckt und analysierbar macht.

## 🏗️ Architektur-Überblick

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + D3.js)                  │
│              Graph Visualization & Query Builder             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ REST API / WebSocket
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend Services (FastAPI)                 │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ Ontology   │  │ Query Engine │  │ Security &       │   │
│  │ Manager    │  │ (Cypher)     │  │ Governance       │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│              Data Integration Layer (Connectors)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │PostgreSQL│  │   REST   │  │   CSV    │  │  Kafka   │   │
│  │ Adapter  │  │ Adapter  │  │ Adapter  │  │ Adapter  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Neo4j   │  │PostgreSQL│  │  Redis   │  │  ElasticS│   │
│  │  (Graph) │  │(Metadata)│  │ (Cache)  │  │  (Search)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Hauptfunktionen

### Phase 1: Foundation (aktuell)
- ✅ Graph-basierte Ontologie-Engine (Neo4j)
- ✅ Plug-in-basiertes Data Connector Framework
- ✅ ETL/ELT Pipelines mit automatischer Fehlerbehandlung
- ✅ Schema-Detection und Mapping
- ✅ REST API mit FastAPI
- ✅ Basis-Sicherheit (JWT, RBAC)

### Phase 2: Analytics & UI (geplant)
- 🔄 React-basiertes Frontend
- 🔄 Graph-Visualisierung (D3.js/Cytoscape.js)
- 🔄 Drag & Drop Query Builder
- 🔄 Dashboard-System
- 🔄 Erweiterte Sicherheit (ABAC)

### Phase 3: Advanced Features (geplant)
- 📋 Data Lineage Tracking & Visualisierung
- 📋 ML-basierte Pattern Detection
- 📋 Natural Language Query Interface
- 📋 AI-assisted Ontology Creation
- 📋 Performance-Optimierung für 1M+ Entitäten

## 📦 Technologie-Stack

| Komponente | Technologie |
|-----------|-------------|
| Backend | Python 3.11+, FastAPI |
| Graph-DB | Neo4j 5.x |
| Metadata-DB | PostgreSQL 15+ |
| Cache | Redis 7.x |
| Search | Elasticsearch 8.x |
| Message Queue | Apache Kafka |
| Frontend | React 18+, TypeScript |
| Visualization | D3.js, Cytoscape.js |
| Orchestration | Apache Airflow |
| Container | Docker, Kubernetes |

## 🛠️ Installation & Setup

### Voraussetzungen
- Docker 24+ & Docker Compose
- Python 3.11+
- Node.js 18+ (für Frontend-Entwicklung)
- kubectl (für Kubernetes-Deployment)

### Lokale Entwicklung

1. **Repository klonen**
```bash
git clone <repository-url>
cd Modularen-Daten-Ontologie-Plattform-MDOP-
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Environment-Variablen konfigurieren**
```bash
cp .env.example .env
# .env mit spezifischen Werten anpassen
```

4. **Services starten (Docker Compose)**
```bash
docker-compose up -d
```

5. **Backend-Server starten**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **API-Dokumentation aufrufen**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 Projektstruktur

```
MDOP/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Endpoints
│   │   ├── core/              # Core-Konfiguration
│   │   ├── models/            # Datenmodelle
│   │   ├── services/          # Business-Logik
│   │   │   ├── ontology/      # Ontologie-Management
│   │   │   ├── connectors/    # Data Connector Framework
│   │   │   ├── query/         # Query Engine
│   │   │   └── security/      # Security Services
│   │   └── main.py            # Application Entry
│   ├── tests/                 # Backend-Tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # React Frontend (Phase 2)
├── infrastructure/
│   ├── docker/                # Docker Configs
│   ├── kubernetes/            # K8s Manifests
│   └── terraform/             # Infrastructure as Code
├── docs/                      # Dokumentation
├── scripts/                   # Utility Scripts
└── docker-compose.yml
```

## 🔐 Sicherheit

### Implementierte Features
- JWT-basierte Authentifizierung
- Role-Based Access Control (RBAC)
- API-Rate-Limiting
- Request-Validierung (Pydantic)
- Verschlüsselte Verbindungen (TLS)

### Geplante Features (Phase 2+)
- Attribute-Based Access Control (ABAC)
- End-to-End-Verschlüsselung
- Audit Logging aller Datenzugriffe
- Data Masking basierend auf Nutzerrollen
- Compliance Reporting (GDPR, CCPA)

## 📊 Performance-Ziele

| Metrik | Zielwert |
|--------|----------|
| Query Response Time | ≤ 2s (bei 1M+ Entitäten) |
| Concurrent Users | 100+ |
| Data Throughput | 10,000 records/sec |
| Graph Traversal Depth | 10+ Hops in < 1s |
| Uptime | 99.9% |

## 🧪 Testing

```bash
# Backend Unit Tests
cd backend
pytest tests/ -v --cov=app

# Integration Tests
pytest tests/integration/ -v

# Load Tests
locust -f tests/load/locustfile.py
```

## 📖 API-Dokumentation

### Core Endpoints

#### Ontology Management
```
POST   /api/v1/ontology/entities         # Create Entity Type
GET    /api/v1/ontology/entities         # List Entity Types
PUT    /api/v1/ontology/entities/{id}    # Update Entity Type
DELETE /api/v1/ontology/entities/{id}    # Delete Entity Type

POST   /api/v1/ontology/relationships    # Define Relationship
GET    /api/v1/ontology/relationships    # List Relationships
```

#### Data Connectors
```
POST   /api/v1/connectors                # Register Connector
GET    /api/v1/connectors                # List Connectors
POST   /api/v1/connectors/{id}/sync      # Trigger Data Sync
GET    /api/v1/connectors/{id}/status    # Check Sync Status
```

#### Query & Analysis
```
POST   /api/v1/query/cypher              # Execute Cypher Query
POST   /api/v1/query/gremlin             # Execute Gremlin Query
POST   /api/v1/search                    # Full-Text Search
GET    /api/v1/graph/traverse            # Graph Traversal
```

## 🐳 Docker Deployment

```bash
# Build Images
docker-compose build

# Start All Services
docker-compose up -d

# View Logs
docker-compose logs -f backend

# Stop Services
docker-compose down
```

## ☸️ Kubernetes Deployment

```bash
# Apply Kubernetes Manifests
kubectl apply -f infrastructure/kubernetes/

# Check Pod Status
kubectl get pods -n mdop

# Port Forward for Local Access
kubectl port-forward svc/mdop-backend 8000:8000 -n mdop
```

## 🗺️ Roadmap

### Q1 2024 - Phase 1: Foundation ✅
- [x] Ontologie Core-Engine
- [x] Data Connector Framework
- [x] Base Connectors (PostgreSQL, REST, CSV)
- [x] REST API
- [x] Basis-Sicherheit

### Q2 2024 - Phase 2: Analytics & UI
- [ ] React Frontend
- [ ] Graph Visualisierung
- [ ] Query Builder
- [ ] Dashboard System
- [ ] ABAC Implementation

### Q3-Q4 2024 - Phase 3: Advanced Features
- [ ] Data Lineage Tracking
- [ ] ML Pattern Detection
- [ ] Natural Language Queries
- [ ] AI-assisted Ontology
- [ ] Performance Optimierung

---

**Status:** 🚧 Phase 1 - Foundation in Entwicklung

**Version:** 0.1.0-alpha

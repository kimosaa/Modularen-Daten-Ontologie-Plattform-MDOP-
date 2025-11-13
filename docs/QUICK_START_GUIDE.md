# MDOP Quick Start Guide
## Get Started in 15 Minutes

### Prerequisites
- Docker 24+ and Docker Compose installed
- 8GB RAM available
- 20GB disk space

### Step 1: Clone and Start (5 minutes)

```bash
# Clone repository
git clone https://github.com/your-org/mdop-platform.git
cd mdop-platform

# Start all services
./scripts/start.sh
```

**Wait for services to start** (this may take 2-3 minutes on first run)

### Step 2: Access the Platform (1 minute)

Open your browser and navigate to:

- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Neo4j Browser:** http://localhost:7474 (user: `neo4j`, pass: `mdop_neo4j_password`)

### Step 3: Load Demo Data (2 minutes)

```bash
# Install Python dependencies for demo script
pip install requests

# Run demo data setup
python scripts/setup_demo_data.py
```

This creates two demo scenarios:
1. **Fraud Detection** - Banking transactions
2. **Supply Chain** - Supplier networks

### Step 4: Explore the Graph (7 minutes)

#### View the Graph Visualization
1. Open http://localhost:3000
2. You should see nodes and connections
3. Click on nodes to see details
4. Drag nodes to reposition them
5. Zoom in/out with mouse wheel

#### Try the API
1. Open http://localhost:8000/docs
2. Navigate to **Ontology** section
3. Try `GET /api/v1/ontology/entity-types` to see all entity types
4. Try `GET /api/v1/ontology/entities` to see entities

#### Query the Graph (Neo4j Browser)
1. Open http://localhost:7474
2. Login with credentials above
3. Try this query:
   ```cypher
   MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 25
   ```

### Common Tasks

#### Create a New Entity Type

```bash
curl -X POST http://localhost:8000/api/v1/ontology/entity-types \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Company",
    "label": "Company",
    "description": "Business organization",
    "properties": {
      "name": {"type": "string", "required": true},
      "industry": {"type": "string"}
    },
    "icon": "business",
    "color": "#10B981"
  }'
```

#### Create an Entity

```bash
curl -X POST http://localhost:8000/api/v1/ontology/entities \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Company",
    "properties": {
      "name": "Acme Corp",
      "industry": "Technology"
    }
  }'
```

#### Create a Relationship

First, get entity IDs from the entities list, then:

```bash
curl -X POST http://localhost:8000/api/v1/ontology/relationships \
  -H "Content-Type: application/json" \
  -d '{
    "type": "WORKS_AT",
    "from_entity_id": "123",
    "to_entity_id": "456",
    "properties": {}
  }'
```

### Troubleshooting

#### Services Won't Start
```bash
# Check Docker
docker --version
docker-compose --version

# Check ports
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :7474  # Neo4j
```

#### Can't See Graph Data
1. Make sure demo data script ran successfully
2. Check backend logs: `docker-compose logs backend`
3. Verify Neo4j has data: Open Neo4j Browser and run `MATCH (n) RETURN count(n)`

#### API Errors
```bash
# Check backend logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend
```

### Next Steps

1. **Read the Documentation**
   - Product Overview: `docs/PRODUCT_OVERVIEW.md`
   - Development Guide: `docs/DEVELOPMENT.md`

2. **Configure Data Connectors**
   - Connect your PostgreSQL database
   - Import CSV files
   - Integrate REST APIs

3. **Customize the Ontology**
   - Define your entity types
   - Create relationship types
   - Map your data model

4. **Explore Advanced Features**
   - WebSocket real-time updates
   - Custom graph queries
   - Data lineage tracking

### Getting Help

- **Documentation:** `docs/` folder
- **API Reference:** http://localhost:8000/docs
- **Support Email:** support@mdop-platform.com
- **Issues:** GitHub Issues

### Stopping the Platform

```bash
# Stop all services
./scripts/stop.sh

# Or manually
docker-compose down

# Stop and remove all data (WARNING: Deletes all data!)
docker-compose down -v
```

---

**Congratulations!** 🎉 You now have MDOP running locally with demo data.

#!/usr/bin/env python3
"""
Demo Data Setup Script
Creates sample data for MDOP demonstrations
"""
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

# Demo Scenarios
SCENARIOS = {
    "fraud_detection": {
        "entity_types": [
            {
                "name": "Customer",
                "label": "Customer",
                "description": "Bank customer",
                "icon": "person",
                "color": "#3B82F6",
                "properties": {
                    "name": {"type": "string", "required": True},
                    "email": {"type": "string"},
                    "account_number": {"type": "string"},
                    "risk_score": {"type": "integer"}
                }
            },
            {
                "name": "Transaction",
                "label": "Transaction",
                "description": "Financial transaction",
                "icon": "payment",
                "color": "#10B981",
                "properties": {
                    "amount": {"type": "float", "required": True},
                    "timestamp": {"type": "datetime"},
                    "status": {"type": "string"},
                    "suspicious": {"type": "boolean"}
                }
            },
            {
                "name": "Account",
                "label": "Account",
                "description": "Bank account",
                "icon": "account_balance",
                "color": "#F59E0B",
                "properties": {
                    "account_number": {"type": "string", "required": True},
                    "balance": {"type": "float"},
                    "type": {"type": "string"}
                }
            }
        ],
        "entities": [
            {"type": "Customer", "properties": {"name": "John Doe", "email": "john@example.com", "account_number": "ACC001", "risk_score": 25}},
            {"type": "Customer", "properties": {"name": "Jane Smith", "email": "jane@example.com", "account_number": "ACC002", "risk_score": 85}},
            {"type": "Customer", "properties": {"name": "Bob Wilson", "email": "bob@example.com", "account_number": "ACC003", "risk_score": 15}},
            
            {"type": "Account", "properties": {"account_number": "ACC001", "balance": 50000.00, "type": "checking"}},
            {"type": "Account", "properties": {"account_number": "ACC002", "balance": 125000.00, "type": "savings"}},
            {"type": "Account", "properties": {"account_number": "ACC003", "balance": 15000.00, "type": "checking"}},
            
            {"type": "Transaction", "properties": {"amount": 1000.00, "status": "completed", "suspicious": False}},
            {"type": "Transaction", "properties": {"amount": 45000.00, "status": "flagged", "suspicious": True}},
            {"type": "Transaction", "properties": {"amount": 500.00, "status": "completed", "suspicious": False}},
        ]
    },
    
    "supply_chain": {
        "entity_types": [
            {
                "name": "Supplier",
                "label": "Supplier",
                "description": "Supply chain supplier",
                "icon": "factory",
                "color": "#8B5CF6",
                "properties": {
                    "name": {"type": "string", "required": True},
                    "country": {"type": "string"},
                    "rating": {"type": "integer"}
                }
            },
            {
                "name": "Product",
                "label": "Product",
                "description": "Product item",
                "icon": "inventory",
                "color": "#EC4899",
                "properties": {
                    "name": {"type": "string", "required": True},
                    "sku": {"type": "string"},
                    "price": {"type": "float"}
                }
            },
            {
                "name": "Warehouse",
                "label": "Warehouse",
                "description": "Storage facility",
                "icon": "warehouse",
                "color": "#14B8A6",
                "properties": {
                    "name": {"type": "string", "required": True},
                    "location": {"type": "string"},
                    "capacity": {"type": "integer"}
                }
            }
        ],
        "entities": [
            {"type": "Supplier", "properties": {"name": "Asia Manufacturing Co", "country": "China", "rating": 4}},
            {"type": "Supplier", "properties": {"name": "European Parts GmbH", "country": "Germany", "rating": 5}},
            
            {"type": "Product", "properties": {"name": "Widget A", "sku": "WDG-001", "price": 29.99}},
            {"type": "Product", "properties": {"name": "Component B", "sku": "CMP-002", "price": 149.99}},
            
            {"type": "Warehouse", "properties": {"name": "Central Warehouse", "location": "Frankfurt", "capacity": 10000}},
            {"type": "Warehouse", "properties": {"name": "North Warehouse", "location": "Hamburg", "capacity": 5000}},
        ]
    }
}


def setup_demo_scenario(scenario_name):
    """Setup a specific demo scenario"""
    print(f"\n=== Setting up {scenario_name} scenario ===\n")
    
    scenario = SCENARIOS[scenario_name]
    
    # Create entity types
    print("Creating entity types...")
    entity_type_ids = {}
    for et in scenario["entity_types"]:
        try:
            response = requests.post(f"{API_BASE}/ontology/entity-types", json=et)
            if response.status_code == 201:
                data = response.json()
                entity_type_ids[et["name"]] = data["id"]
                print(f"  ✓ Created {et['name']}")
            else:
                print(f"  ✗ Failed to create {et['name']}: {response.text}")
        except Exception as e:
            print(f"  ✗ Error creating {et['name']}: {e}")
    
    # Create entities
    print("\nCreating entities...")
    for entity in scenario["entities"]:
        try:
            response = requests.post(f"{API_BASE}/ontology/entities", json=entity)
            if response.status_code == 201:
                print(f"  ✓ Created {entity['type']}: {list(entity['properties'].values())[0]}")
            else:
                print(f"  ✗ Failed to create entity: {response.text}")
        except Exception as e:
            print(f"  ✗ Error creating entity: {e}")
    
    print(f"\n✅ {scenario_name} scenario setup complete!\n")


def main():
    print("=" * 60)
    print("MDOP Demo Data Setup")
    print("=" * 60)
    
    # Check if API is available
    try:
        response = requests.get(f"{API_BASE.replace('/api/v1', '')}/health")
        if response.status_code != 200:
            print("❌ API is not available. Please start the backend first.")
            return
        print("✅ API is available\n")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Please make sure the backend is running: docker-compose up -d")
        return
    
    # Setup scenarios
    for scenario_name in SCENARIOS.keys():
        setup_demo_scenario(scenario_name)
    
    print("=" * 60)
    print("✅ All demo scenarios created successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Open http://localhost:3000 to view the graph")
    print("  2. Use the API at http://localhost:8000/docs")
    print("  3. Access Neo4j Browser at http://localhost:7474")


if __name__ == "__main__":
    main()

# MDOP Demo Video Scripts
## Anleitungen für Aufnahme von Demo-Videos

---

## Video 1: Platform Overview (3 Minuten)

### Ziel
Schneller Überblick über MDOP für Entscheidungsträger.

### Script

---

**[0:00 - 0:15] Intro**

*Zeige: Logo Animation*

> "Willkommen bei MDOP - der Modularen Daten-Ontologie-Plattform. In den nächsten 3 Minuten zeige ich Ihnen, wie Sie komplexe Datenbeziehungen visualisieren und analysieren können - zu einem Bruchteil der Kosten von Enterprise-Lösungen."

---

**[0:15 - 0:45] Problem & Solution**

*Zeige: Illustrationen von Datensilos*

> "Unternehmen kämpfen täglich mit einem Problem: Daten sind über dutzende Systeme verteilt. Beziehungen zwischen Kunden, Transaktionen, Lieferanten - alles versteckt in verschiedenen Datenbanken."

*Zeige: MDOP Graph-Ansicht*

> "MDOP löst dieses Problem, indem es alle Ihre Daten in einem interaktiven Graphen vereint. Sie sehen sofort, wie alles zusammenhängt."

---

**[0:45 - 1:30] Live Demo**

*Zeige: Browser öffnen, localhost:3000*

> "Hier sehen Sie die MDOP Oberfläche. Links unsere Graph-Visualisierung, rechts Details zum ausgewählten Element."

*Klicke auf verschiedene Nodes*

> "Jeder Punkt repräsentiert eine Entität - hier ein Kunde, dort eine Transaktion. Die Linien zeigen die Beziehungen."

*Zoome und verschiebe Nodes*

> "Sie können zoomen, verschieben und per Drag-and-Drop reorganisieren. Alles ist interaktiv."

*Zeige: Swagger UI mit API Docs*

> "Im Hintergrund läuft eine REST API. Entwickler können alles automatisieren."

---

**[1:30 - 2:00] Key Features**

*Zeige: Feature-Liste oder Icons*

> "MDOP bietet:
> - Echtzeit-Updates per WebSocket
> - Universal Data Connectors für PostgreSQL, MongoDB, REST APIs
> - Enterprise Security mit GDPR-Compliance
> - Und das Beste: Sie können es selbst hosten - keine Cloud-Abhängigkeit."

---

**[2:00 - 2:30] Pricing & Comparison**

*Zeige: Preistabelle*

> "Der Starter-Plan beginnt bei 4.999 Euro pro Jahr - für 10 Benutzer und 100.000 Entitäten. Das ist 90% günstiger als Palantir."

*Zeige: Comparison Chart*

> "Im Vergleich: Palantir kostet über 500.000 Euro. Neo4j Enterprise über 150.000 Euro. Mit MDOP bekommen Sie vergleichbare Features zu einem Bruchteil des Preises."

---

**[2:30 - 3:00] Call to Action**

*Zeige: Website mit Demo-Anfrage Formular*

> "Möchten Sie MDOP in Aktion sehen? Fordern Sie eine kostenlose Demo an unter demo@mdop-platform.com. Wir zeigen Ihnen MDOP mit Ihren eigenen Daten."

> "Vielen Dank fürs Zusehen!"

*Zeige: Logo + Kontaktdaten*

---

## Video 2: Fraud Detection Demo (5 Minuten)

### Ziel
Zeigen, wie MDOP für Fraud Detection in der Finanzbranche genutzt wird.

### Script

---

**[0:00 - 0:30] Intro & Context**

*Zeige: Banking/Finance Imagery*

> "In diesem Video zeige ich Ihnen, wie Banken MDOP nutzen, um betrügerische Transaktionsmuster in Echtzeit zu erkennen."

> "Betrugserkennung ist wie die Suche nach der Nadel im Heuhaufen - außer dass der Heuhaufen täglich größer wird. MDOP macht diese Nadel sichtbar."

---

**[0:30 - 1:30] Data Import**

*Zeige: Swagger UI - POST /entity-types*

> "Zuerst definieren wir unsere Entitätstypen. Wir brauchen Kunden, Konten und Transaktionen."

*Führe API-Call aus*

```json
{
  "name": "Customer",
  "label": "Kunde",
  "properties": {
    "name": {"type": "string"},
    "risk_score": {"type": "integer"}
  },
  "color": "#3B82F6"
}
```

> "Jeder Entitätstyp hat ein Schema mit Eigenschaften. Der Kunde hat einen Namen und einen Risk Score."

*Zeige: Entity Creation*

> "Jetzt importieren wir unsere Daten. In der Realität würden Sie den PostgreSQL-Connector nutzen, um direkt aus Ihrem Core Banking System zu importieren."

---

**[1:30 - 3:00] Graph Exploration**

*Zeige: Frontend mit geladenem Fraud-Graph*

> "Hier sehen wir unseren Transaction-Graphen. Die blauen Nodes sind Kunden, grün sind Konten, orange sind Transaktionen."

*Klicke auf verdächtige Transaktion (rot markiert)*

> "Diese Transaktion ist rot markiert - unser System hat sie als verdächtig eingestuft. Schauen wir uns an, warum."

*Zeige Details Panel*

> "Eine Transaktion über 45.000 Euro - deutlich über dem Durchschnitt dieses Kunden. Der Risk Score ist hoch."

*Zeige Beziehungen*

> "Was MDOP besonders macht: Wir sehen sofort die Beziehungen. Diese Transaktion geht an ein Konto, das in den letzten 7 Tagen 15 weitere verdächtige Transaktionen empfangen hat - von 12 verschiedenen Sendern."

> "Das ist ein klassisches Muster für Money Mule Accounts."

---

**[3:00 - 4:00] Pattern Detection**

*Zeige: Neo4j Browser mit Cypher Query*

> "Für fortgeschrittene Analysen können wir Cypher Queries direkt ausführen."

```cypher
MATCH (c:Customer)-[:OWNS]->(a:Account)-[:RECEIVED]->(t:Transaction)
WHERE t.suspicious = true
WITH a, count(t) as suspiciousCount
WHERE suspiciousCount > 10
RETURN a
```

> "Diese Query findet alle Konten mit mehr als 10 verdächtigen eingehenden Transaktionen. Das sind unsere Money Mule Kandidaten."

*Zeige Ergebnis in Graph*

> "Die Ergebnisse werden sofort im Graph visualisiert. Wir haben 3 verdächtige Konten identifiziert."

---

**[4:00 - 4:30] Real-Time Monitoring**

*Zeige: WebSocket Connection*

> "MDOP aktualisiert sich in Echtzeit. Wenn eine neue verdächtige Transaktion eingeht, erscheint sie sofort im Graph - ohne Seite neu laden."

> "Ihr Fraud-Team kann den ganzen Tag den Graph beobachten und sofort reagieren."

---

**[4:30 - 5:00] Conclusion**

*Zeige: ROI Calculation*

> "Unsere Kunden berichten von einer 70% schnelleren Fraud-Erkennung und 50% weniger False Positives."

> "Möchten Sie sehen, wie MDOP Ihre Fraud-Detection verbessern kann? Schreiben Sie uns an demo@mdop-platform.com für eine personalisierte Demo."

*Zeige: Logo + Kontakt*

---

## Video 3: Quick Start Tutorial (5 Minuten)

### Ziel
Technisches Tutorial für Developer - von Null bis zum laufenden System.

### Script

---

**[0:00 - 0:20] Intro**

> "In diesem Tutorial zeige ich Ihnen, wie Sie MDOP in unter 15 Minuten lokal installieren und die ersten Daten visualisieren."

---

**[0:20 - 1:00] Prerequisites**

*Zeige: Terminal*

> "Sie brauchen Docker und Docker Compose. Prüfen wir das:"

```bash
docker --version
docker-compose --version
```

> "Docker 24, Docker Compose 2.23 - perfekt."

---

**[1:00 - 2:00] Clone & Start**

*Zeige: Terminal*

```bash
git clone https://github.com/your-org/mdop-platform.git
cd mdop-platform
./scripts/start.sh
```

> "Wir klonen das Repository und starten alle Services. Das Script startet Neo4j, PostgreSQL, Redis, Elasticsearch und das Backend."

*Warte bis Services starten*

> "Das dauert beim ersten Mal 2-3 Minuten, weil Docker die Images herunterladen muss."

---

**[2:00 - 2:45] Load Demo Data**

*Zeige: Terminal*

```bash
python scripts/setup_demo_data.py
```

> "Wir laden unsere Demo-Daten. Das Script erstellt zwei Szenarien: Fraud Detection und Supply Chain."

*Zeige Output mit Checkmarks*

> "Alle Entity Types und Entities wurden erstellt. Sie sehen die grünen Checkmarks."

---

**[2:45 - 3:30] Explore Frontend**

*Zeige: Browser - localhost:3000*

> "Öffnen wir das Frontend. Hier ist unser Graph mit den Demo-Daten."

*Klicke auf Nodes, zeige Details*

> "Klicken Sie auf einen Node um Details zu sehen. Die Farben zeigen den Entity Type an."

*Zoome und verschiebe*

> "Mit dem Mausrad zoomen Sie, per Drag-and-Drop verschieben Sie Nodes."

---

**[3:30 - 4:15] Explore API**

*Zeige: Browser - localhost:8000/docs*

> "Hier ist unsere API-Dokumentation. Swagger UI generiert automatisch interaktive Docs."

*Führe GET /entity-types aus*

> "Probieren wir es aus: GET auf /ontology/entity-types. Hier sind alle unsere definierten Typen."

*Zeige Response*

> "Customer, Transaction, Account, Supplier... alle mit ihren Eigenschaften."

---

**[4:15 - 4:45] Create Custom Entity**

*Zeige: POST /entities*

```json
{
  "type": "Customer",
  "properties": {
    "name": "Max Mustermann",
    "email": "max@example.com",
    "risk_score": 50
  }
}
```

> "Erstellen wir einen eigenen Kunden. Execute... und wir bekommen die ID zurück."

*Zeige Frontend - neuer Node erscheint*

> "Dank WebSocket erscheint der neue Kunde sofort im Graph - ohne Neuladen."

---

**[4:45 - 5:00] Next Steps**

*Zeige: Docs/DEVELOPMENT.md*

> "In der DEVELOPMENT.md finden Sie alles Weitere: Wie Sie eigene Connectors bauen, Custom Queries schreiben, und das System für Production deployen."

> "Fragen? Schreiben Sie uns an support@mdop-platform.com. Happy Coding!"

*Zeige: Logo*

---

## Aufnahme-Tipps

### Equipment
- **Screen Recording:** OBS Studio, Loom, oder Camtasia
- **Mikrofon:** USB Kondensator-Mikrofon (Blue Yeti, etc.)
- **Auflösung:** 1920x1080 (Full HD)
- **Frame Rate:** 30 FPS

### Vorbereitung
1. Alle Services starten und testen
2. Browser Tabs vorbereiten
3. Terminal mit den Commands vorbereiten
4. Demo-Daten frisch laden (für konsistente Screenshots)

### Während der Aufnahme
- **Tempo:** Langsam und deutlich sprechen
- **Pausen:** Nach wichtigen Punkten kurz pausieren
- **Cursor:** Cursor groß und sichtbar machen
- **Clean Desktop:** Nur relevante Fenster zeigen

### Post-Production
- **Schnitt:** Stille und Fehler herausschneiden
- **Zooms:** Auf wichtige UI-Elemente zoomen
- **Callouts:** Text-Overlays für wichtige Punkte
- **Music:** Leise Hintergrundmusik (optional)

### Hosting
- YouTube (unlisted für private Demos)
- Vimeo Pro (für embedded Player auf Website)
- Wistia (für Sales-Analytics)

---

## Thumbnail-Ideen

### Video 1: Platform Overview
- Graph-Visualisierung im Hintergrund
- Text: "MDOP in 3 Minuten"
- Blauer Farbton

### Video 2: Fraud Detection
- Roter Alarm-Icon auf Graph
- Text: "Fraud Detection Demo"
- Rot-Orange Farbton

### Video 3: Quick Start
- Terminal-Fenster
- Text: "Setup in 15 Min"
- Grüner Farbton

---

## Metrics zu tracken

- **Views** - Wie viele schauen
- **Watch Time** - Wie lange schauen sie
- **Engagement** - Likes, Comments, Shares
- **Click-Through** - Klicks auf Demo-Link
- **Conversion** - Demo-Anfragen nach Video-View

---

**Fragen zu den Videos?** Kontaktieren Sie marketing@mdop-platform.com

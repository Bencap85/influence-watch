# Influence Watch

Influence Watch is a research prototype for exploring narrative divergence across international media ecosystems. It ingests global news, clusters articles into real‑world events, and analyzes how different geopolitical blocs describe, frame, and prioritize those events. The system detects anomalies such as narrative drift, coordinated messaging, reporting bursts, sentiment manipulation, and asymmetric coverage.

Influence Watch is built around an AI agent that operates over structured, tool‑call–ready data. A dedicated MCP layer exposes events, detections, articles, and analytical signals through controlled, schema‑validated tools, enabling the agent to generate traceable intelligence briefs where every claim is grounded in underlying evidence.

The goal is to provide an early‑warning capability for information manipulation, allowing analysts to understand not just what is being reported, but how, when, and why narratives differ across geopolitical blocs, and to be able to inspect the agent’s reasoning through explicit attribution.

This project is intentionally scoped as a local proof‑of‑concept. It focuses on the core agent‑centric intelligence workflow (ingestion → clustering → signal extraction → anomaly detection → traceable, agent‑generated brief) rather than production concerns like distributed ingestion, cloud deployment, or large‑scale orchestration.

## Why Narrative Divergence Matters for Intelligence
Modern influence operations rarely announce themselves. They emerge as subtle shifts in how state‑aligned media outlets:

- frame an event
- emphasize or omit key details
- coordinate messaging
- amplify or suppress narratives
- diverge from global consensus

These shifts often precede:

- diplomatic escalations
- military signaling
- information shaping campaigns
- domestic mobilization
- coordinated propaganda pushes

Influence Watch is designed to detect these early signals by comparing how the United States, Russia, China, North Korea, Iran, and the European Union report on the same event.

The system answers questions like:

- “Which countries are framing this event differently from everyone else?”
- “Who is reporting unusually early or unusually often?”
- “Is there evidence of coordinated messaging within a state’s media ecosystem?”
- “Which narratives are being selectively amplified or suppressed?”

This is the core of narrative intelligence—understanding not just what happened, but how different actors want it to be perceived.

## System Details

```
influence-watch/
├── main/                 # Python ingestion, clustering, detection
├── mcp/                  # MCP server exposing agent tools
├── frontend/             # React analyst UI
├── shared/               # Models, schemas, DB utilities
├── docker-compose.yml    # Local orchestration
└── README.md
```

### Python Backend
Python service responsible for ingesting, processing, and clustering raw news articles.
- Queries RSS feeds and ingests raw articles
- Cleans and embeds articles to ready them for processing
- Clusters articles into events using an online, threshold-based algorithm
- Captures signals per article, per event, and per bloc
- Detects anomolies based on signals such as sentiment, semantic similarity, temporal distance, and keyword convergence

### MCP Server
The MCP Server provides structured tools to the AI agent used in gathering data used for automated intelligence briefs. This layer supports safe, controlled access to intelligence data stored in the database.
- Connects to database
- Exposes read-only tools for retrieving data on events, detections, articles, and analytical signals
- Enables the agent to prepare reports and conduct data analysis
- Ensures every agent claim is backed by traceable, evidence-based citations

### React UI
- Analyst-centered dashboard on global events and influence operation detections
- Displays attributions for each AI assertion in the automated intelligence briefs

### PostgreSQL Database
- Uses pgvector to support vector storage, comparison, and retrieval

## Detection Categories

A list of narrative influence techniques currently supported by the system and how they are detected

1. Strong Divergence From Global Baseline

    A country’s reporting is semantically or sentimentally far from the global average.
    
    Signals:
    - country_embeddings vs global_baseline_embedding
    - country_sentiment vs global_baseline_sentiment
    - country_keywords vs global_baseline_keywords
    - country_entities vs global_baseline_entities


2. Rapid Reporting Burst (Temporal Anomaly)

    A country publishes an unusually high number of articles about an event in a short window.

    Signals:
    - processed_article.published_at
    - event.first_seen_at, event.last_seen_at
    - Per‑country article counts
    - event.num_articles


3. Strong Sentiment Divergence

    A country’s sentiment is significantly more positive or negative than the global baseline.

    Signals:
    - country_sentiment
    - global_baseline_sentiment
    - Sentiment distribution across articles

4. High Intra‑Country Semantic Similarity (Possible Coordination)

    Articles from the same country are unusually similar to each other.

    Signals:
    - Intra‑country embedding similarity
    - country_embeddings
    - Distance to event centroid

5. Keyword or Entity Convergence (Narrative Steering)

    A country repeatedly uses the same unusual keywords or entities not seen globally.

    Signals:
    - country_keywords vs global_baseline_keywords
    - country_entities vs global_baseline_entities
    - Keyword/entity frequency spikes

6. Asymmetric Coverage (Selective Amplification)

    A country heavily reports on an event that others barely mention.

    Signals:
    - Per‑country article counts
    - event.countries
    - event.num_articles

7. Narrative Reversal or Contradiction

    A country frames the event in the opposite direction of the global consensus.

    Signals:
    - Sentiment polarity differences
    - Keyword framing differences
    - Entity sentiment differences
    - Embedding directionality

8. Early Origin Indicator (Narrative Seeding)

    A country reports significantly earlier than others.

    Signals:
    - Earliest per‑country published_at
    - event.first_seen_at
    - Time deltas between countries

## Getting Started
Influence Watch runs locally using Docker for backend services and Node for the frontend.
To set up the system, you will need:

- Node.js
- Docker and Docker Compose
- OpenAI API key

1. Clone the repository
    ```
    git clone https://github.com/Bencap85/influence-watch.git
    cd influence-watch
    ```
2. Set your environment variables

    Create a .env file in the project root:

    ```
    OPENAI_API_KEY=<your_api_key_here>

    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=influence_watch

    DB_HOST=influence-watch-db
    DB_PORT=5432
    DB_NAME=influence_watch

    MCP_SERVER_BASE_URL=http://host.docker.internal:9000
    ```
    The only value you will need to add is your OpenAI API key. All other values are already configured for local development.

3. Start backend services

    This launches the backend services, including the MCP service and Postgres database:

    ```
    docker-compose up --build
    ```
4. Set up UI environment variables

    Create a .env file in the frontend directory:

    ```
    VITE_API_BASE_URL=http://localhost:8000/api/v1
    ```
    
5. Start the React UI

    In a separate terminal:

    ```
    cd frontend
    npm install
    npm start
    ```
    The UI will be available at:

    ```
    http://localhost:3000
    ```

6. Interact with the system
    Once running, you can:

    Ingest articles by performing `GET http://localhost:8080/api/v1/job/ingestion`

    Run the processing pipeline by performing `GET http://localhost:8080/api/v1/job/process`. This clusters newly-ingested articles, generates signals, runs detections, etc.

    View detections, articles, and events in the UI

    Inspect evidence and divergence signals

    Review traceable, agent-generated intelligence briefs on influence operation detections

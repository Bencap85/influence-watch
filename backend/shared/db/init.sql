CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE source (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    is_state_affiliated BOOLEAN NOT NULL,
    base_url TEXT,
    description TEXT
);

CREATE TABLE raw_article (
    article_id UUID PRIMARY KEY,
    source_id INT REFERENCES source(id),
    source_url TEXT NOT NULL,
    source_name TEXT NOT NULL,
    title TEXT NOT NULL,
    body_text TEXT,
    description_text TEXT,
    language TEXT,
    country TEXT,
    is_state_affiliated BOOLEAN NOT NULL,
    published_at TIMESTAMP NOT NULL,
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    is_processed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE processed_article (
    article_id UUID PRIMARY KEY REFERENCES raw_article(article_id),
    title TEXT NOT NULL,
    clean_body_text TEXT,
    clean_description_text TEXT,
    source_name TEXT NOT NULL,
    summary TEXT,
    embedding Vector(1536),
    sentiment_score FLOAT,
    keyword_list JSONB,
    entity_list JSONB,
    country TEXT,
    is_state_affiliated BOOLEAN NOT NULL,
    published_at TIMESTAMP NOT NULL,
    processed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE event (
    id UUID PRIMARY KEY,
    title TEXT,
    event_summary TEXT,
    centroid_embedding VECTOR(1536),
    global_keywords JSONB,
    global_entities JSONB,
    global_sentiment FLOAT,
    countries JSONB,
    num_articles INTEGER DEFAULT 0,
    first_seen_at TIMESTAMP,
    last_seen_at TIMESTAMP
);

CREATE TABLE event_article (
    event_id UUID REFERENCES event(id),
    article_id UUID REFERENCES processed_article(article_id),
    PRIMARY KEY (event_id, article_id)
);

CREATE TABLE event_analytics (
    event_id UUID PRIMARY KEY REFERENCES event(id),
    country_embeddings JSONB,
    country_keywords JSONB,
    country_entities JSONB,
    country_sentiment JSONB,
    global_baseline_embedding VECTOR(1536),
    global_baseline_keywords JSONB,
    global_baseline_entities JSONB,
    global_baseline_sentiment FLOAT
);

CREATE TABLE detection (
    id UUID PRIMARY KEY,
    event_id UUID REFERENCES event(id),
    country_code TEXT NOT NULL,
    detection_type TEXT NOT NULL,
    timestamp_detected TIMESTAMP DEFAULT NOW(),
    evidence JSONB
);

CREATE TABLE flag (
    name TEXT UNIQUE NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);

ALTER TABLE detection
ADD CONSTRAINT unique_detection
UNIQUE (event_id, detection_type, country_code);

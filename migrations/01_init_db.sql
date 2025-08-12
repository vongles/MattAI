CREATE EXTENSION IF NOT EXISTS "vector";

-- Simplified schema optimized for llama.cpp integration
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    identifier TEXT NOT NULL UNIQUE,
    is_me BOOLEAN DEFAULT FALSE,
    metadata JSONB
);

CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    context_hash BYTEA  -- For storing llama.cpp context snapshots
);

CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(conversation_id),
    sender_id INTEGER REFERENCES users(user_id),
    content TEXT NOT NULL,
    is_outgoing BOOLEAN,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    embedding vector(384),
    tokens INTEGER[]  -- Store tokenized representation
);

-- Indexes optimized for llama.cpp operations
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_embedding ON messages USING ivfflat (embedding vector_l2_ops);

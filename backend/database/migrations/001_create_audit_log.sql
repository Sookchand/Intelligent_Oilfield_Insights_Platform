-- Query Audit Log Table for Halliburton Compliance
-- Tracks all queries for auditability and governance

CREATE TABLE IF NOT EXISTS query_audit_log (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    query_type VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW(),
    user_id VARCHAR(100),  -- For future authentication
    user_name VARCHAR(200),
    confidence_score DECIMAL(3,2),
    processing_time_ms INTEGER,
    status VARCHAR(20) CHECK (status IN ('success', 'failed', 'partial')),
    data_sources_used JSONB,  -- ['PostgreSQL', 'Neo4j', 'Qdrant', 'MinIO']
    reasoning_trace JSONB,
    result_summary TEXT,
    is_archived BOOLEAN DEFAULT FALSE,
    archived_at TIMESTAMP,
    archived_by VARCHAR(100),
    session_id VARCHAR(100),
    ip_address VARCHAR(45),
    metadata JSONB,  -- Additional context
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_query_timestamp ON query_audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_query_user ON query_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_query_archived ON query_audit_log(is_archived);
CREATE INDEX IF NOT EXISTS idx_query_type ON query_audit_log(query_type);
CREATE INDEX IF NOT EXISTS idx_query_status ON query_audit_log(status);
CREATE INDEX IF NOT EXISTS idx_query_session ON query_audit_log(session_id);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Drop trigger if exists before creating (prevents duplicate error)
DROP TRIGGER IF EXISTS update_query_audit_log_updated_at ON query_audit_log;

CREATE TRIGGER update_query_audit_log_updated_at BEFORE UPDATE
    ON query_audit_log FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE query_audit_log IS 'Audit trail for all AI queries - compliance and governance';
COMMENT ON COLUMN query_audit_log.query_text IS 'Original natural language query from user';
COMMENT ON COLUMN query_audit_log.query_type IS 'Classified intent: production_query, safety_analysis, etc.';
COMMENT ON COLUMN query_audit_log.confidence_score IS 'AI confidence level (0.00 to 1.00)';
COMMENT ON COLUMN query_audit_log.data_sources_used IS 'JSON array of databases queried';
COMMENT ON COLUMN query_audit_log.reasoning_trace IS 'Full reasoning trace for explainability';
COMMENT ON COLUMN query_audit_log.is_archived IS 'Soft delete flag for data retention';


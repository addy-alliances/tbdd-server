CREATE TABLE IF NOT EXISTS http_api_executions (
    id VARCHAR(36) PRIMARY KEY,
    http_api_id VARCHAR(36) NOT NULL REFERENCES http_api(id) ON DELETE CASCADE,
    request_headers JSON,
    request_params JSON,
    request_body JSON,
    response_status_code INTEGER,
    response_headers JSON,
    response_body JSON,
    error TEXT,
    duration_ms DOUBLE PRECISION,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_http_api_executions_http_api_id
    ON http_api_executions (http_api_id);
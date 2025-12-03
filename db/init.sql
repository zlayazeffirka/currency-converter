CREATE TABLE IF NOT EXISTS requests (
    id SERIAL PRIMARY KEY,
    base_currency VARCHAR(3) NOT NULL CHECK (length(base_currency) = 3),
    target_currency VARCHAR(3) NOT NULL CHECK (length(target_currency) = 3),
    amount NUMERIC(18, 6) NOT NULL,
    result NUMERIC(18, 6) NOT NULL,
    rate NUMERIC(18, 10) NOT NULL,
    requested_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_requests_time ON requests (requested_at);
CREATE INDEX IF NOT EXISTS idx_requests_pair ON requests (base_currency, target_currency);
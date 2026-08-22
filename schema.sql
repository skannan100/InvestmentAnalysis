-- Portfolio Evaluation Database Schema
-- SQLite schema for investment analysis and holdings tracking

-- Portfolio holdings table (for displaying current holdings)
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    ticker TEXT NOT NULL,
    sector TEXT,
    qty INTEGER,
    avg_cost REAL,
    invested REAL,
    value REAL,
    pe REAL,
    market_cap TEXT,
    w52h REAL,
    w52l REAL,
    last_updated TEXT,
    assessment TEXT
);

-- Indices for common queries
CREATE INDEX IF NOT EXISTS idx_holdings_ticker ON portfolio_holdings(ticker);

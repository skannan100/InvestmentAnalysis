-- Portfolio Evaluation Database Schema
-- DuckDB schema for investment analysis and holdings tracking

-- Main evaluations table
CREATE TABLE IF NOT EXISTS evaluations (
    evaluation_id VARCHAR PRIMARY KEY,
    company_name VARCHAR NOT NULL,
    ticker VARCHAR NOT NULL,
    exchange VARCHAR,
    sector VARCHAR,
    industry VARCHAR,
    analysis_date DATE,
    analysis_time VARCHAR,
    timezone VARCHAR,
    analysis_type VARCHAR,
    ownership_status VARCHAR,
    previous_evaluation_id VARCHAR,
    investment_thesis_summary VARCHAR,
    industry_structure VARCHAR,
    industry_trend VARCHAR,
    competitive_position VARCHAR,
    moat_status VARCHAR,
    customer_economics VARCHAR,
    pricing_power VARCHAR,
    customer_stickiness VARCHAR,
    optionality VARCHAR,
    management_quality VARCHAR,
    capital_allocation VARCHAR,
    incentive_alignment VARCHAR,
    corporate_governance VARCHAR,
    economic_conversion_quality VARCHAR,
    bear_case_severity VARCHAR,
    external_vulnerability VARCHAR,
    downside_asymmetry VARCHAR,
    upside_asymmetry VARCHAR,
    thesis_break_probability VARCHAR,
    market_expectations VARCHAR,
    valuation VARCHAR,
    portfolio_fit VARCHAR,
    opportunity_cost VARCHAR,
    business_quality VARCHAR,
    investment_attractiveness VARCHAR,
    thesis_status VARCHAR,
    overall_confidence VARCHAR,
    primary_bull_case VARCHAR,
    primary_bear_case VARCHAR,
    biggest_unknown VARCHAR,
    buy_trigger VARCHAR,
    add_trigger VARCHAR,
    hold_condition VARCHAR,
    reduce_trigger VARCHAR,
    exit_trigger VARCHAR,
    what_improved_since_last VARCHAR,
    what_deteriorated_since_last VARCHAR,
    decision VARCHAR,
    decision_rationale VARCHAR,
    full_factor_detail JSON
);

-- Portfolio holdings table (for displaying current holdings)
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    ticker VARCHAR NOT NULL,
    sector VARCHAR,
    qty INTEGER,
    avg_cost DECIMAL(10, 2),
    invested DECIMAL(15, 2),
    value DECIMAL(15, 2),
    pe DECIMAL(10, 2),
    market_cap VARCHAR,
    w52h DECIMAL(10, 2),
    w52l DECIMAL(10, 2),
    last_updated DATE,
    assessment JSON
);

-- Indices for common queries
CREATE INDEX IF NOT EXISTS idx_evaluations_ticker ON evaluations(ticker);
CREATE INDEX IF NOT EXISTS idx_evaluations_company ON evaluations(company_name);
CREATE INDEX IF NOT EXISTS idx_evaluations_date ON evaluations(analysis_date);
CREATE INDEX IF NOT EXISTS idx_holdings_ticker ON portfolio_holdings(ticker);

#!/usr/bin/env python3
"""
Simple Flask API server for Portfolio Ledger Dashboard
Serves holdings data from local DuckDB database
"""

import json
import duckdb
from flask import Flask, jsonify
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Path to DuckDB database
DB_PATH = Path(__file__).parent / "portfolio.duckdb"

def get_db():
    """Get or create DuckDB connection"""
    conn = duckdb.connect(str(DB_PATH), read_only=False)
    return conn

def init_db():
    """Initialize database with schema and seed data"""
    conn = get_db()
    
    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            conn.execute(schema_sql)
    
    # Read and execute seed data
    seed_path = Path(__file__).parent / "seed_data.sql"
    if seed_path.exists():
        with open(seed_path, 'r') as f:
            seed_sql = f.read()
            try:
                conn.execute(seed_sql)
            except Exception as e:
                # Data may already exist, continue
                print(f"Note: Seed data load returned: {e}")
    
    conn.close()

def format_holdings(row):
    """Convert DuckDB row to portfolio holdings format"""
    return {
        "id": row[0],
        "name": row[1],
        "ticker": row[2],
        "sector": row[3],
        "qty": int(row[4]) if row[4] else 0,
        "avgCost": float(row[5]) if row[5] else 0,
        "invested": float(row[6]) if row[6] else 0,
        "value": float(row[7]) if row[7] else 0,
        "pe": float(row[8]) if row[8] else None,
        "marketCap": row[9],
        "w52h": float(row[10]) if row[10] else None,
        "w52l": float(row[11]) if row[11] else None,
        "lastUpdated": str(row[12]) if row[12] else None,
        "assessment": json.loads(row[13]) if row[13] else None
    }

@app.route('/api/holdings', methods=['GET'])
def get_holdings():
    """
    GET /api/holdings
    Returns all portfolio holdings as JSON array
    """
    try:
        conn = get_db()
        query = """
            SELECT 
                id, name, ticker, sector, qty, avg_cost, invested, value,
                pe, market_cap, w52h, w52l, last_updated, assessment
            FROM portfolio_holdings
            ORDER BY ticker
        """
        result = conn.execute(query).fetchall()
        conn.close()
        
        holdings = [format_holdings(row) for row in result]
        return jsonify(holdings), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluations', methods=['GET'])
def get_evaluations():
    """
    GET /api/evaluations
    Returns all evaluations as JSON array
    """
    try:
        conn = get_db()
        query = """
            SELECT 
                evaluation_id, company_name, ticker, sector, decision,
                investment_attractiveness, thesis_status, overall_confidence,
                decision_rationale, analysis_date
            FROM evaluations
            ORDER BY analysis_date DESC
        """
        result = conn.execute(query).fetchall()
        conn.close()
        
        evaluations = [
            {
                "evaluation_id": row[0],
                "company_name": row[1],
                "ticker": row[2],
                "sector": row[3],
                "decision": row[4],
                "investment_attractiveness": row[5],
                "thesis_status": row[6],
                "overall_confidence": row[7],
                "decision_rationale": row[8],
                "analysis_date": str(row[9])
            }
            for row in result
        ]
        return jsonify(evaluations), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/evaluation/<ticker>', methods=['GET'])
def get_evaluation(ticker):
    """
    GET /api/evaluation/<ticker>
    Returns full evaluation details for a specific stock
    """
    try:
        conn = get_db()
        query = """
            SELECT * FROM evaluations
            WHERE ticker = ?
            ORDER BY analysis_date DESC
            LIMIT 1
        """
        result = conn.execute(query, [ticker]).fetchall()
        conn.close()
        
        if not result:
            return jsonify({"error": f"No evaluation found for ticker {ticker}"}), 404
        
        # For simplicity, return as JSON string representation
        # In production, map all columns to a dict
        row = result[0]
        evaluation = {
            "evaluation_id": row[0],
            "company_name": row[1],
            "ticker": row[2],
            "exchange": row[3],
            "sector": row[4],
            "industry": row[5],
            "analysis_date": str(row[6]),
            "decision": row[46],
            "decision_rationale": row[47],
            "primary_bull_case": row[34],
            "primary_bear_case": row[35],
            "biggest_unknown": row[36],
            "investment_thesis_summary": row[10],
            "full_factor_detail": json.loads(row[48]) if row[48] else None
        }
        return jsonify(evaluation), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200

if __name__ == '__main__':
    # Initialize database on startup
    print("Initializing database...")
    init_db()
    print(f"Database ready at {DB_PATH}")
    
    # Run Flask app
    print("Starting API server on http://localhost:5000")
    app.run(debug=True, port=5000)

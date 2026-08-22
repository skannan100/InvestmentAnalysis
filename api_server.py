#!/usr/bin/env python3
"""
Simple Flask API server for Portfolio Ledger Dashboard
Serves holdings data from local SQLite database
"""

import json
import sqlite3
from flask import Flask, jsonify
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Path to SQLite database
DB_PATH = Path(__file__).parent / "portfolio.db"

def get_db():
    """Get SQLite connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    return conn

def init_db():
    """Initialize database with schema and seed data"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Read and execute schema
    schema_path = Path(__file__).parent / "schema.sql"
    if schema_path.exists():
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
    
    # Read and execute seed data
    seed_path = Path(__file__).parent / "seed_data.sql"
    if seed_path.exists():
        with open(seed_path, 'r') as f:
            seed_sql = f.read()
            try:
                cursor.executescript(seed_sql)
                conn.commit()
            except Exception as e:
                # Data may already exist
                print(f"Note: Seed data load returned: {e}")
    
    conn.close()

def format_holdings(row):
    """Convert SQLite row to portfolio holdings format"""
    return {
        "id": row['id'],
        "name": row['name'],
        "ticker": row['ticker'],
        "sector": row['sector'],
        "qty": row['qty'] or 0,
        "avgCost": float(row['avg_cost']) if row['avg_cost'] else 0,
        "invested": float(row['invested']) if row['invested'] else 0,
        "value": float(row['value']) if row['value'] else 0,
        "pe": float(row['pe']) if row['pe'] else None,
        "marketCap": row['market_cap'],
        "w52h": float(row['w52h']) if row['w52h'] else None,
        "w52l": float(row['w52l']) if row['w52l'] else None,
        "lastUpdated": row['last_updated'],
        "assessment": json.loads(row['assessment']) if row['assessment'] else None
    }

@app.route('/api/holdings', methods=['GET'])
def get_holdings():
    """
    GET /api/holdings
    Returns all portfolio holdings as JSON array
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        query = """
            SELECT 
                id, name, ticker, sector, qty, avg_cost, invested, value,
                pe, market_cap, w52h, w52l, last_updated, assessment
            FROM portfolio_holdings
            ORDER BY ticker
        """
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        
        holdings = [format_holdings(row) for row in result]
        return jsonify(holdings), 200
    
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

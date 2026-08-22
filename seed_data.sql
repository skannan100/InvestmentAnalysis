-- Seed portfolio holdings data (SQLite compatible)
INSERT INTO portfolio_holdings (
    id, name, ticker, sector, qty, avg_cost, invested, value, pe, market_cap,
    w52h, w52l, last_updated, assessment
) VALUES
(
    'EICHERMOT-001',
    'Eicher Motors Limited',
    'EICHERMOT',
    'Automobile · Two-Wheelers',
    17,
    3828.49,
    65084.25,
    137283.50,
    39.82,
    '₹2,19,598 Cr',
    8230.00,
    5825.50,
    '2026-08-19',
    '{"thesis":{"moatType":"Brand loyalty","summary":"Eicher''s case rests almost entirely on Royal Enfield''s brand moat in the 250-750cc middleweight motorcycle segment, where it holds roughly 85-90% domestic market share and is the global category leader."}}'
),
(
    'CMSINFO-001',
    'CMS Info Systems Limited',
    'CMSINFO',
    'Financial Services · Cash Logistics',
    179,
    241.74,
    43271.10,
    45152.75,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
),
(
    'BLUESTARCO-001',
    'Blue Star Limited',
    'BLUESTARCO',
    'Consumer Durables · Cooling',
    70,
    533.37,
    37335.88,
    106085.00,
    58.36,
    '₹30,796 Cr',
    2040.00,
    1450.00,
    '2026-08-12',
    NULL
),
(
    'ETERNAL-001',
    'Eternal Limited',
    'ETERNAL',
    'Internet · Food Delivery',
    195,
    76.08,
    14835.41,
    63765.00,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
);

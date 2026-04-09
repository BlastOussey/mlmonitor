# MLMonitor — Model Performance Monitoring Dashboard

## What It Does
MLMonitor is a real-time operations dashboard that tracks the health of deployed ML models. It integrates with New Relic's API to pull live system metrics, monitors model accuracy and data drift over time, and fires automated alerts when performance degrades.

## The Problem It Solves
Deployed ML models degrade silently. Accuracy drops, data distributions shift, and latency spikes often go undetected for days. MLMonitor closes this gap with continuous monitoring, drift detection, and instant alerting.

## Tech Stack
- Backend: Python, Flask
- Monitoring: New Relic API
- Database: PostgreSQL
- DevOps: Docker, AWS, GitHub Actions CI/CD

## Key Features
- Real-time accuracy, latency, and data drift tracking
- New Relic API integration for infrastructure metrics
- Automated alerting when thresholds are breached
- Historical performance charts with configurable time windows
- PostgreSQL-backed metrics store for trend analysis

## Results
- Reduced mean time to detect model degradation from days to under 2 hours
- Caught 5 data drift events before they impacted production accuracy
- Dashboard loads all metrics in under 1.5 seconds

## Getting Started
git clone https://github.com/BlastOussey/mlmonitor.git
cd mlmonitor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask run

## Project Structure
mlmonitor/
├── app/
│   ├── main.py
│   ├── monitors/
│   └── integrations/
└── db/
    └── schema.sql

## Author
Ousseynou Diop
LinkedIn: https://www.linkedin.com/in/ousseynou-diop-946a1a245/
Portfolio: https://my-resume-umber-rho.vercel.app/

from flask import Flask, jsonify, request
from monitors.drift import detect_drift
from monitors.accuracy import track_accuracy
from integrations.newrelic import fetch_metrics
from db.models import save_metric, get_metrics_history, save_alert
import os

app = Flask(__name__)


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/metrics/live')
def live_metrics():
    """Fetch live metrics from New Relic API."""
    try:
        metrics = fetch_metrics(
            api_key=os.getenv('NEW_RELIC_API_KEY'),
            account_id=os.getenv('NEW_RELIC_ACCOUNT_ID')
        )
        return jsonify(metrics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/history')
def metrics_history():
    """Get historical metrics from PostgreSQL."""
    model_id = request.args.get('model_id', 'default')
    days = int(request.args.get('days', 7))
    history = get_metrics_history(model_id, days)
    return jsonify(history)


@app.route('/api/metrics/ingest', methods=['POST'])
def ingest_metrics():
    """Receive and store model performance metrics."""
    data = request.json
    required = ['model_id', 'accuracy', 'latency_ms', 'predictions_count']
    if not all(k in data for k in required):
        return jsonify({'error': f'Required fields: {required}'}), 400

    save_metric(data)

    # Check for drift
    drift_result = detect_drift(data['model_id'], data.get('feature_distribution'))
    if drift_result['drift_detected']:
        alert = {
            'model_id': data['model_id'],
            'alert_type': 'data_drift',
            'message': f"Data drift detected: {drift_result['drift_score']:.4f}",
            'severity': 'high' if drift_result['drift_score'] > 0.3 else 'medium'
        }
        save_alert(alert)
        return jsonify({'ingested': True, 'alert': alert})

    return jsonify({'ingested': True, 'drift': drift_result})


@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts."""
    from db.models import get_recent_alerts
    model_id = request.args.get('model_id')
    alerts = get_recent_alerts(model_id)
    return jsonify(alerts)


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development', port=5000)

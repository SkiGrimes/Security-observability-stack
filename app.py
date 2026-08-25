from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['endpoint']
)

LOGIN_ATTEMPTS = Counter(
    'login_attempts_total',
    'Total login attempts',
    ['result']
)

# Fake user database
USERS = {
    'alice': 'password123',
    'bob': 'qwerty',
    'carol': 'letmein'
}

@app.route('/')
def index():
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start)
    return jsonify({
        'service': 'Hotline Capital Lending API',
        'status': 'operational',
        'version': '1.0.0'
    })

@app.route('/quote')
def quote():
    start = time.time()
    # Simulate some processing time
    time.sleep(random.uniform(0.01, 0.05))
    REQUEST_COUNT.labels(method='GET', endpoint='/quote', status='200').inc()
    REQUEST_LATENCY.labels(endpoint='/quote').observe(time.time() - start)
    return jsonify({
        'loan_amount': random.randint(5000, 50000),
        'apr': round(random.uniform(5.0, 18.0), 2),
        'term_months': 36
    })

@app.route('/login', methods=['POST', 'GET'])
def login():
    start = time.time()
    username = request.args.get('username') or (request.json or {}).get('username', '')
    password = request.args.get('password') or (request.json or {}).get('password', '')

    if username in USERS and USERS[username] == password:
        LOGIN_ATTEMPTS.labels(result='success').inc()
        REQUEST_COUNT.labels(method='POST', endpoint='/login', status='200').inc()
        REQUEST_LATENCY.labels(endpoint='/login').observe(time.time() - start)
        return jsonify({'status': 'authenticated', 'user': username})
    else:
        LOGIN_ATTEMPTS.labels(result='failure').inc()
        REQUEST_COUNT.labels(method='POST', endpoint='/login', status='401').inc()
        REQUEST_LATENCY.labels(endpoint='/login').observe(time.time() - start)
        return jsonify({'status': 'unauthorized'}), 401

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
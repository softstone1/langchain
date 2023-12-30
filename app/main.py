from flask import Flask, jsonify
from app.kube_client import list_pods_with_errors
from cachetools import TTLCache, cached
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set up cache with TTL (e.g., 10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

@cached(cache)
def get_cached_pods(namespace):
    return list_pods_with_errors(namespace)

@app.route('/pods/errors/<namespace>')
def get_pods_with_errors(namespace):
    try:
        pods = get_cached_pods(namespace)
        return jsonify(pods)
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

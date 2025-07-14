from flask import Flask, jsonify, request
import redis
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Redis client
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

# Mongo client
mongo_client = MongoClient('mongodb://mongo:27017/')
mongo_db = mongo_client['testdb']
user_agents_collection = mongo_db['user_agents']

@app.route('/')
def hello():
    return "Hello from Flask behind NGINX!"

@app.route('/redis-set')
def redis_set():
    redis_client.set('mykey', 'Hello Redis!')
    return "Set key in Redis."

@app.route('/redis-get')
def redis_get():
    value = redis_client.get('mykey')
    return f"Got from Redis: {value}"

@app.route('/track')
def track():
    user_agent = request.headers.get('User-Agent', 'Unknown')
    today = datetime.utcnow().strftime("%Y-%m-%d")

    hll_key = f'unique_user_agents_hll:{today}'
    redis_client.pfadd(hll_key, user_agent)

    set_key = f'unique_user_agents_set:{today}'
    redis_client.sadd(set_key, user_agent)

    existing = user_agents_collection.find_one({
        'user_agent': user_agent,
        'date': today
    })

    if not existing:
        user_agents_collection.insert_one({
            'user_agent': user_agent,
            'date': today
        })

    return f"Tracked User-Agent: {user_agent} for {today}"

@app.route('/unique-count')
def unique_count():
    count = redis_client.pfcount('unique_user_agents')
    return f"Approximate unique User-Agents: {count}"

@app.route('/unique-user')
def unique_user():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    agents_cursor = user_agents_collection.find(
        {'date': today},
        {'_id': 0, 'user_agent': 1})
    user_agents = [doc['user_agent'] for doc in agents_cursor]
    tota_users = len(user_agents)

    return jsonify({
        "date": today,
        "total": tota_users,
        "user_agents": user_agents
    })

@app.route('/reset')
def reset():
    redis_client.delete('unique_user_agents_hll')
    redis_client.delete('unique_user_agents_set')
    user_agents_collection.delete_many({})
    return "All unique User-Agent data reset!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import time

from flask import Flask, request, jsonify
from urllib.request import Request
from redis import Redis



class RateLimit:
    def __init__(self, redis_client, max_request=10, window=60):
        self.redis = redis_client
        self.max_request = max_request
        self.window = window

    def allow_request(self, user_id):
        now = time.time()
        key = f"rate_limit:{user_id}"

        pipe = self.redis.pipeline()
        pipe.zadd(key, {now: now})
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zcard(key)
        pipe.expire(key, self.window * 2)

        _, _, request_count, _ = pipe.execute()

        print(request_count)

        return request_count <= self.max_request

app = Flask(__name__)

redis_client = Redis(host='redis', port=6379, db=0)
rate_limit = RateLimit(redis_client)


@app.route('/')
def hello_world():
    return {"Hello": "World"}

@app.before_request
async def rate_limit_middleware():
    user_id = request.headers.get('X-User-ID', 'anonymous')

    if not rate_limit.allow_request(user_id):
        return jsonify(
            status_code=429,
            content={"Message": "Limite de requests excedido"}
        )
    
    return jsonify(
            status_code=202,
            content={"Message": "Accepted"}
        )
    

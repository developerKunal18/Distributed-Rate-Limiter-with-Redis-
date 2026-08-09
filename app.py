from flask import Flask, request, jsonify
import redis

from rate_limiter import RateLimiter

app = Flask(__name__)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

limiter = RateLimiter(redis_client)


@app.route("/")
def home():

    client_id = request.headers.get(
        "X-Client-ID",
        request.remote_addr
    )

    result = limiter.allow(client_id)

    if not result["allowed"]:

        response = jsonify({
            "message": "Rate limit exceeded",
            "retry_after": result["retry_after"]
        })

        response.status_code = 429

        response.headers["Retry-After"] = str(
            result["retry_after"]
        )

        response.headers["X-RateLimit-Limit"] = str(
            result["limit"]
        )

        response.headers["X-RateLimit-Remaining"] = str(
            result["remaining"]
        )

        return response

    response = jsonify({
        "message": "Request accepted"
    })

    response.headers["X-RateLimit-Limit"] = str(
        result["limit"]
    )

    response.headers["X-RateLimit-Remaining"] = str(
        result["remaining"]
    )

    return response


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

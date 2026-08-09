import redis


RATE_LIMIT = 100
WINDOW_SECONDS = 60


RATE_LIMIT_SCRIPT = """
local current = redis.call('INCR', KEYS[1])

if current == 1 then
    redis.call('EXPIRE', KEYS[1], ARGV[1])
end

local ttl = redis.call('TTL', KEYS[1])

return {current, ttl}
"""


class RateLimiter:

    def __init__(self, redis_client):

        self.redis = redis_client

    def allow(self, client_id):

        key = f"rate_limit:{client_id}"

        result = self.redis.eval(
            RATE_LIMIT_SCRIPT,
            1,
            key,
            WINDOW_SECONDS
        )

        current_count = int(result[0])
        remaining = max(
            RATE_LIMIT - current_count,
            0
        )

        allowed = current_count <= RATE_LIMIT

        return {
            "allowed": allowed,
            "limit": RATE_LIMIT,
            "remaining": remaining,
            "retry_after": int(result[1])
        }

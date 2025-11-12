import redis
from app.core.config import settings
from typing import Optional
import json


class RedisService:
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            print("✓ Redis connected successfully")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            print("⚠ Application will continue without Redis caching")
            self.redis_client = None

    def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        if not self.redis_client:
            return None
        try:
            return self.redis_client.get(key)
        except Exception:
            return None

    def set(self, key: str, value: str, expire: int = 300) -> bool:
        """Set value in Redis with expiration (default 5 minutes)"""
        if not self.redis_client:
            return False
        try:
            self.redis_client.setex(key, expire, value)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.redis_client:
            return False
        try:
            self.redis_client.delete(key)
            return True
        except Exception:
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        if not self.redis_client:
            return False
        try:
            return bool(self.redis_client.exists(key))
        except Exception:
            return False

    def set_json(self, key: str, value: dict, expire: int = 300) -> bool:
        """Set JSON value in Redis"""
        return self.set(key, json.dumps(value), expire)

    def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from Redis"""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except Exception:
                return None
        return None


# Global instance
redis_service = RedisService()
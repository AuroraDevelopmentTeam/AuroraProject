from typing import Optional, Any, Union, List
import aioredis
import yaml
from pathlib import Path

class RedisManager:
    def __init__(self):
        # Load configuration
        config_path = Path(__file__).parent.parent.parent.parent / "config" / "settings.yaml"
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        # Initialize Redis connection
        self.redis: Optional[aioredis.Redis] = None
        self.redis_config = self.config.get("redis", {})

    async def connect(self) -> None:
        """Connect to Redis server."""
        if self.redis is None:
            self.redis = await aioredis.from_url(
                f"redis://{self.redis_config.get('host', 'localhost')}:{self.redis_config.get('port', 6379)}",
                db=self.redis_config.get("db", 0),
                password=self.redis_config.get("password"),
                encoding="utf-8",
                decode_responses=True,
                max_connections=self.redis_config.get("max_connections", 10),
                socket_timeout=self.redis_config.get("socket_timeout", 5),
                socket_connect_timeout=self.redis_config.get("socket_connect_timeout", 5)
            )

    async def disconnect(self) -> None:
        """Disconnect from Redis server."""
        if self.redis is not None:
            await self.redis.close()
            self.redis = None

    async def get(self, key: str) -> Any:
        """Get value from Redis."""
        if self.redis is None:
            await self.connect()
        return await self.redis.get(key)

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> None:
        """Set value in Redis with optional expiration."""
        if self.redis is None:
            await self.connect()
        await self.redis.set(key, value, ex=ex)

    async def delete(self, key: str) -> None:
        """Delete key from Redis."""
        if self.redis is None:
            await self.connect()
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if self.redis is None:
            await self.connect()
        return bool(await self.redis.exists(key))

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for key."""
        if self.redis is None:
            await self.connect()
        return bool(await self.redis.expire(key, seconds))

    async def incr(self, key: str, amount: int = 1) -> int:
        """Increment the value of a key by the specified amount."""
        if self.redis is None:
            await self.connect()
        return await self.redis.incrby(key, amount)

    async def decr(self, key: str, amount: int = 1) -> int:
        """Decrement the value of a key by the specified amount."""
        if self.redis is None:
            await self.connect()
        return await self.redis.decrby(key, amount)

    async def hset(self, name: str, key: str, value: Any) -> None:
        """Set hash field to value."""
        if self.redis is None:
            await self.connect()
        await self.redis.hset(name, key, value)

    async def hget(self, name: str, key: str) -> Any:
        """Get the value of a hash field."""
        if self.redis is None:
            await self.connect()
        return await self.redis.hget(name, key)

    async def hgetall(self, name: str) -> dict:
        """Get all fields and values in a hash."""
        if self.redis is None:
            await self.connect()
        return await self.redis.hgetall(name)

    async def sadd(self, name: str, *values: Any) -> int:
        """Add one or more members to a set."""
        if self.redis is None:
            await self.connect()
        return await self.redis.sadd(name, *values)

    async def smembers(self, name: str) -> set:
        """Get all members of a set."""
        if self.redis is None:
            await self.connect()
        return await self.redis.smembers(name)

    async def pipeline(self) -> aioredis.Redis:
        """Get a Redis pipeline for executing multiple commands."""
        if self.redis is None:
            await self.connect()
        return self.redis.pipeline()

# Create a global instance
redis_manager = RedisManager() 
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from typing import Optional, Any
from fastapi import UploadFile
from src.config.config import get_settings
import hashlib

async def init_cache():
    settings = get_settings()
    redis_cli = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    
    try:
        pong = await redis_cli.ping()
        if pong != "PONG" and pong is not True:
            raise RuntimeError("Unexpected PING response: %r" % pong)
        print(f"✅ Connected to Redis at {settings.REDIS_URL}")
    except Exception as e:
        raise RuntimeError(f"Cannot connect to Redis at {settings.REDIS_URL!r}: {e}")
    
    FastAPICache.init(RedisBackend(redis_cli), prefix="food-cache")

def image_cache_key_builder(
    func: Any,
    namespace: Optional[str] = "",
    *,
    request: Optional[Any] = None,
    file: UploadFile = None,
    **kwargs: Any
) -> str:
    """Build cache key from file content hash"""
    if file is None:
        raise ValueError("File is required for cache key generation")
    
    # Read first 1MB for hash (adjust size as needed)
    file.file.seek(0)
    file_content = file.file.read(1024 * 1024)
    file.file.seek(0)
    
    # Generate SHA256 hash of file content
    file_hash = hashlib.sha256(file_content).hexdigest()
    return f"{namespace}::{func.__module__}.{func.__name__}::{file_hash}"
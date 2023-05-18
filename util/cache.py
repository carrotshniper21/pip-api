import redis
import asyncio
import json

redis_client = redis.Redis(host='localhost', port=6379)


async def cache_data(key, fetch_data_func, *args):
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    else:
        if asyncio.iscoroutinefunction(fetch_data_func):
            data = await fetch_data_func(*args)
        else:
            data = fetch_data_func(*args)
        redis_client.set(key, json.dumps(data))
        return data

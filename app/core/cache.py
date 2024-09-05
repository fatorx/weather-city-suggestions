import redis as redis
from app.core.config import settings
import re

redis_host = settings.REDIS_HOST
redis_port = settings.REDIS_PORT
redis_db = settings.REDIS_DATABASE

cache = redis.Redis(host=redis_host, port=redis_port, db=redis_db)


def transform_key(key_name):
    key_name = re.sub(r'[àáâãäå]', 'a', key_name)
    key_name = re.sub(r'[èéêë]', 'e', key_name)
    key_name = re.sub(r'[ìíîï]', 'i', key_name)
    key_name = re.sub(r'[òóôõö]', 'o', key_name)
    key_name = re.sub(r'[ùúûü]', 'u', key_name)
    key_name = re.sub(r'[ç]', 'c', key_name)

    key_name = key_name.lower().replace(' ', '_')

    return key_name


def set_cache(key, value, expire):
    key = transform_key(key)
    cache.set(key, value, ex=expire)


def get_cache(key):
    key = transform_key(key)
    return cache.get(key)

import redis
import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR: {BASE_DIR}")

# Take environment variables from .env file
env_file = os.path.join(BASE_DIR, '.env')
environ.Env.read_env(env_file)

# Overwrite existing environment variables with those from the .env file
with open(env_file) as f:
    for line in f:
        if line.strip() and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Now you can access the environment variables
redis_url = os.environ.get('REDIS_URL')
print(f"REDIS_URL: {redis_url}")


try:
    print(f"Trying to connect to Redis server at {redis_url}")
    # Create a Redis client
    client = redis.StrictRedis.from_url(redis_url)

    # Test the connection
    response = client.ping()
    if response:
        print("Connected to Redis server successfully!")
    else:
        print("Failed to connect to Redis server.")
except Exception as e:
    print(f"Error: {e}")
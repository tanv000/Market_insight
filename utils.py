import pickle
from config import CACHE_PATH

def save_cache(data):
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(data, f)

def load_cache():
    with open(CACHE_PATH, "rb") as f:
        return pickle.load(f)

def cache_exists():
    import os
    return os.path.exists(CACHE_PATH)

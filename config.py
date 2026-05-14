#!/usr/bin/env python3
"""
Configuration, Cache & Logging Module
"""

import os
import pickle
import logging
from datetime import datetime

# Cache configuration
CACHE_FILE = os.path.expanduser("~/.dns_harvest_cache.pkl")
CACHE_DURATION = 3600

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='dns_harvest.log'
)

# ==================== CACHE FUNCTIONS ====================

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'rb') as f:
                return pickle.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)
    except:
        pass

def get_from_cache(key):
    cache = load_cache()
    if key in cache:
        cached_time, result = cache[key]
        if (datetime.now() - cached_time).seconds < CACHE_DURATION:
            return result
    return None

def add_to_cache(key, result):
    cache = load_cache()
    cache[key] = (datetime.now(), result)
    save_cache(cache)

def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        return True
    return False
"""Hashing examples to generate ids"""

import hashlib
import json

def hash_example(ex):
    return hashlib.md5(json.dumps(ex, sort_keys=True).encode("utf-8")).hexdigest()

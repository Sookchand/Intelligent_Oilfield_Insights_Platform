"""Test database connections"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.connections import test_all_connections
import json

print("Testing database connections...")
print("="*60)
results = test_all_connections()
print(json.dumps(results, indent=2))
print("="*60)


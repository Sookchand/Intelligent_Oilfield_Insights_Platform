"""Check current environment variables"""
import os
from dotenv import load_dotenv

load_dotenv()

print("Current Environment Variables:")
print("="*60)
print(f"NEO4J_URI: {os.getenv('NEO4J_URI')}")
print(f"QDRANT_HOST: {os.getenv('QDRANT_HOST')}")
print(f"QDRANT_PORT: {os.getenv('QDRANT_PORT')}")
print(f"MINIO_ENDPOINT: {os.getenv('MINIO_ENDPOINT')}")
print("="*60)


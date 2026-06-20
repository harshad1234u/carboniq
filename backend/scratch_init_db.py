"""
Create tables using the Supabase SQL HTTP endpoint.
Supabase exposes a SQL endpoint at /sql that accepts raw SQL via service role.
"""
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

with open("database/schema.sql", "r") as f:
    schema_sql = f.read()

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}

# Try multiple known endpoints for raw SQL execution
endpoints_to_try = [
    "/sql",
    "/rest/v1/rpc/exec_sql",
    "/pg/query", 
    "/database/query",
]

for ep in endpoints_to_try:
    try:
        url = f"{SUPABASE_URL}{ep}"
        
        if "rpc" in ep:
            payload = {"sql": "SELECT 1 as test"}
        else:
            payload = {"query": "SELECT 1 as test"}
        
        response = httpx.post(url, headers=headers, json=payload, timeout=10)
        print(f"{ep}: status={response.status_code} body={response.text[:200]}")
    except Exception as e:
        print(f"{ep}: error={e}")

# Let's also check if supabase CLI is available
print("\n--- Checking for supabase CLI ---")
import subprocess
try:
    result = subprocess.run(["supabase", "--version"], capture_output=True, text=True, timeout=5)
    print(f"Supabase CLI: {result.stdout.strip()}")
except FileNotFoundError:
    print("Supabase CLI not installed")
except Exception as e:
    print(f"CLI check error: {e}")

# Check for npx supabase
try:
    result = subprocess.run(["npx", "supabase", "--version"], capture_output=True, text=True, timeout=15)
    print(f"npx supabase: {result.stdout.strip()}")
except Exception as e:
    print(f"npx supabase error: {e}")

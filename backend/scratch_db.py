import sys
sys.path.append("d:/code_placed/carbon/backend")
from database.client import get_supabase
try:
    client = get_supabase()
    # Attempt to query profiles
    res = client.table('profiles').select('*').limit(1).execute()
    print("Profiles:", res.data)
except Exception as e:
    print("Error profiles:", e)

try:
    res2 = client.table('carbon_entries').select('*').limit(1).execute()
    print("Carbon entries:", res2.data)
except Exception as e:
    print("Error carbon:", e)

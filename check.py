import httpx
import re

print("Fetching index.html...")
r = httpx.get('https://carboniq-frontend-722791638231.asia-south1.run.app')
match = re.search(r'src="(/assets/index-.*?\.js)"', r.text)

if match:
    print(f"Found JS bundle: {match.group(1)}")
    js_url = f"https://carboniq-frontend-722791638231.asia-south1.run.app{match.group(1)}"
    js_code = httpx.get(js_url).text
    
    api_found = 'https://carboniq-backend-722791638231.asia-south1.run.app/api' in js_code
    supabase_found = 'rvnyugoafrixfgdalymf.supabase.co' in js_code
    
    print(f"API URL present in bundle: {api_found}")
    print(f"SUPABASE URL present in bundle: {supabase_found}")
else:
    print("Could not find index.js in HTML")

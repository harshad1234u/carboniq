import os
import subprocess
from dotenv import load_dotenv

# Load env variables
load_dotenv('backend/.env')

secrets = {
    'carboniq-gemini-api-key': os.getenv('GEMINI_API_KEY'),
    'carboniq-openweather-api-key': os.getenv('OPENWEATHER_API_KEY'),
    'carboniq-supabase-url': os.getenv('SUPABASE_URL'),
    'carboniq-supabase-service-key': os.getenv('SUPABASE_SERVICE_ROLE_KEY')
}

for name, value in secrets.items():
    if not value:
        print(f"Skipping {name}: No value in .env")
        continue

    # Create secret (ignore if exists)
    subprocess.run(['gcloud.cmd', 'secrets', 'create', name, '--replication-policy=automatic'], capture_output=True)
    
    # Add new version
    print(f"Adding version for {name}...")
    proc = subprocess.Popen(['gcloud.cmd', 'secrets', 'versions', 'add', name, '--data-file=-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=value.encode())
    if proc.returncode == 0:
        print(f"Successfully added {name}")
    else:
        print(f"Failed to add {name}: {stderr.decode()}")

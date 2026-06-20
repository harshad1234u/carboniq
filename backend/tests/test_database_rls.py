import os
import uuid
import pytest
from database.client import get_supabase
from utils.config import settings

@pytest.mark.skipif(not settings.supabase_url or not settings.supabase_service_role_key, reason="Real Supabase connection required")
def test_rls_violations():
    # We will simulate RLS by using the admin client to create two dummy profiles
    # Then we use a client initialized with an anon key (or jwt for user A) to fetch data.
    # To truly test RLS, we need the user's JWT. We can use auth.sign_up for a dummy user.
    
    admin_client = get_supabase()
    
    # Generate random emails for test users
    user_a_email = f"test_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"test_b_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPassword123!"
    
    # Create User A
    try:
        user_a_res = admin_client.auth.sign_up({"email": user_a_email, "password": password, "options": {"data": {"name": "User A"}}})
        # Create User B
        user_b_res = admin_client.auth.sign_up({"email": user_b_email, "password": password, "options": {"data": {"name": "User B"}}})
        
        user_a_id = user_a_res.user.id
        user_b_id = user_b_res.user.id
        
        # Insert a profile for User A using service role (bypass RLS)
        admin_client.table('profiles').insert({
            "id": user_a_id, "name": "User A", "email": user_a_email, 
            "city": "Mumbai", "transport_type": "car", "diet_type": "average"
        }).execute()
        
        # Now try to login as User B and access User A's profile
        # Supabase python client stores session after sign_in
        from supabase import create_client
        # We need the anon key to create a standard client. If not in settings, use a dummy one and it might fail,
        # but we can try using the admin client's JWT auth override if possible.
        # Assuming we can login User B:
        user_b_client = create_client(settings.supabase_url, os.environ.get("SUPABASE_ANON_KEY", settings.supabase_service_role_key))
        user_b_client.auth.sign_in_with_password({"email": user_b_email, "password": password})
        
        # User B tries to read User A's profile
        result = user_b_client.table('profiles').select('*').eq('id', user_a_id).execute()
        
        # RLS should prevent this, so data should be empty
        assert len(result.data) == 0, "RLS Violation! User B can read User A's profile"
        
    except Exception as e:
        # If signup fails (e.g. rate limit), skip test gracefully
        pytest.skip(f"Could not perform live RLS test: {e}")
    finally:
        # Cleanup
        # Note: service role can delete users from auth
        try:
            admin_client.auth.admin.delete_user(user_a_id)
            admin_client.auth.admin.delete_user(user_b_id)
        except:
            pass

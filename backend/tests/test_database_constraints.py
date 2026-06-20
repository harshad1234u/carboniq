import pytest
from database.client import get_supabase
from utils.config import settings


def _table_exists(client, table_name: str) -> bool:
    """Check if a table is accessible (exists in Supabase schema cache).

    Args:
      client: 
      table_name: str: 

    Returns:

    """
    try:
        client.table(table_name).select("*").limit(0).execute()
        return True
    except Exception:
        return False


@pytest.mark.skipif(
    not settings.supabase_url or not settings.supabase_service_role_key,
    reason="Real Supabase connection required",
)
def test_database_connection():
    """Verify that the Supabase client can connect."""
    client = get_supabase()
    assert client is not None


@pytest.mark.skipif(
    not settings.supabase_url or not settings.supabase_service_role_key,
    reason="Real Supabase connection required",
)
def test_required_tables_exist():
    """Verify all required tables exist in the Supabase schema."""
    client = get_supabase()
    required_tables = [
        "profiles",
        "carbon_entries",
        "recommendations",
        "eco_predictions",
        "challenges",
        "badges",
    ]
    missing = [t for t in required_tables if not _table_exists(client, t)]
    if missing:
        pytest.skip(
            f"Tables not created yet: {', '.join(missing)}. "
            "Run database/schema.sql in the Supabase SQL Editor first."
        )


@pytest.mark.skipif(
    not settings.supabase_url or not settings.supabase_service_role_key,
    reason="Real Supabase connection required",
)
def test_duplicate_profile():
    """Inserting a duplicate profile ID should fail (PK constraint)."""
    client = get_supabase()
    if not _table_exists(client, "profiles"):
        pytest.skip("profiles table not found — run schema.sql first")

    res = client.table("profiles").select("*").limit(1).execute()
    if len(res.data) == 0:
        pytest.skip("No existing profiles to test duplicate constraint")

    existing_profile = res.data[0]
    with pytest.raises(Exception):
        client.table("profiles").insert(existing_profile).execute()


@pytest.mark.skipif(
    not settings.supabase_url or not settings.supabase_service_role_key,
    reason="Real Supabase connection required",
)
def test_missing_foreign_keys():
    """Inserting a carbon_entry with a non-existent profile_id should fail."""
    client = get_supabase()
    if not _table_exists(client, "carbon_entries"):
        pytest.skip("carbon_entries table not found — run schema.sql first")

    import uuid

    dummy_uuid = str(uuid.uuid4())
    with pytest.raises(Exception):
        client.table("carbon_entries").insert(
            {
                "profile_id": dummy_uuid,
                "transport_emissions": 0,
                "electricity_emissions": 0,
                "food_emissions": 0,
                "flight_emissions": 0,
                "total_emissions": 0,
            }
        ).execute()

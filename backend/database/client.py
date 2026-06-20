import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

_supabase: Client | None = None


def get_supabase() -> Client:
    """Initialize and return the Supabase client."""
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.error("Supabase credentials not found in environment variables.")
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        try:
            _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    return _supabase

from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Get Supabase URL and key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(url, key)

def get_supabase_client() -> Client:
    return supabase

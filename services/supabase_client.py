import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
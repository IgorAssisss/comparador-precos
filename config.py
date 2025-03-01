# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 02:54:55 2025

@author: Assis
"""

from supabase import create_client

SUPABASE_URL = "https://pcfxmbplshjvuerixpnl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBjZnhtYnBsc2hqdnVlcml4cG5sIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MDYyODk4MSwiZXhwIjoyMDU2MjA0OTgxfQ.dXYvPZXILF08Eh7uONM5NwDXVnbf2Yn8AQrbl8mkx7E"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

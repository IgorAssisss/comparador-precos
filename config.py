# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 02:54:55 2025

@author: Assis
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Variáveis de ambiente do Supabase não encontradas!")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

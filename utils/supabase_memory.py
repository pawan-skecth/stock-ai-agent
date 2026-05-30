from supabase import create_client
from datetime import datetime

# 👉 PASTE YOUR VALUES HERE
SUPABASE_URL = "https://cnixwdyjytpgyrmacjoj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNuaXh3ZHlqeXRwZ3lybWFjam9qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk4NzU1MTgsImV4cCI6MjA5NTQ1MTUxOH0.FCQOA9Ji0C8sLX41rfzhiED2WctvzfVzjxpOb17Rw0w"

# create connection
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# SAVE MEMORY
def save_memory(stock_symbol, decision, confidence):

    data = {
        "stock_symbol": stock_symbol,
        "decision": decision,
        "confidence": confidence,
        "timestamp": str(datetime.now())
    }

    supabase.table("stock_memory").insert(data).execute()


# GET LAST 5 RECORDS
def get_memory(stock_symbol):

    response = supabase.table("stock_memory") \
        .select("*") \
        .eq("stock_symbol", stock_symbol) \
        .order("id", desc=True) \
        .limit(5) \
        .execute()

    return response.data
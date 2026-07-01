import os

port = int(os.getenv("PORT", "9090"))
db_url = os.getenv("DB_URL")  # без fallback-значения с localhost!
if not db_url:
    raise RuntimeError("DB_URL environment variable is required")
  table_name = "field_lynx"

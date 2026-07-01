import os

port = int(os.getenv("PORT", "9090"))

db_url = os.getenv("DB_URL")
if not db_url:
    raise RuntimeError("DB_URL environment variable is required")

table_name = "field_lynx"  # <-- здесь была ошибка

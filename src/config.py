import os

port = int(os.getenv("PORT", "9090"))
db_url = os.getenv("DB_URL")  # без fallback-значения с localhost!
table_name = "field_lynx"

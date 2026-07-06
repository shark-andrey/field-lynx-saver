import os

port = os.getenv("PORT", 9090)
db_url = os.getenv("DB_URL", "mysql+asyncmy://root:password@localhost:3306/dev")
table_name = "field_lynx"

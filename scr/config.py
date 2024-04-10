import os

port = os.getenv("PORT", 9955)
db_url = os.getenv("DB_URL", "mysql+asyncmy://root:password@localhost:3306/dev")
# db_url = os.getenv("DB_URL", "mysql+pymysql://root:password@localhost:3306/dev")
table_name = "finish_lynx"

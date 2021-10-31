import os
from dotenv import load_dotenv
load_dotenv()

db_scheme = "mysql+pymysql"
db_address = os.getenv("DB_ADDRESS")
db_port = os.getenv("DB_PORT", 3306)
db_name = os.getenv("DB_NAME")
db_account = os.getenv("DB_ACCOUNT")
db_password = os.getenv("DB_PASSWORD")
srv_port = os.getenv("SRV_PORT")

SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
    db_scheme,
    db_account,
    db_password,
    db_address,
    db_port,
    db_name
)

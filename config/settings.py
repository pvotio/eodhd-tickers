from decouple import config

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
TOKEN = config("TOKEN", default="INFO")
EXCHANGES_OUTPUT_TABLE = config("OUTPUT_TABLE")
TICKERS_OUTPUT_TABLE = config("OUTPUT_TABLE")
INSERTER_MAX_RETRIES = config("INSERTER_MAX_RETRIES", default=3, cast=int)
MSSQL_SERVER = config("MSSQL_SERVER")
MSSQL_AD_LOGIN = config("MSSQL_AD_LOGIN", cast=bool, default=False)
MSSQL_DATABASE = config("MSSQL_DATABASE")

if not MSSQL_AD_LOGIN:
    MSSQL_USERNAME = config("MSSQL_USERNAME")
    MSSQL_PASSWORD = config("MSSQL_PASSWORD")

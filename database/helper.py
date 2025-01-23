from config import settings
from database import MSSQLDatabase


def init_db_instance():
    return MSSQLDatabase()


def load_exchanges():
    query = settings.EXCHANGES_DB_QUERY
    conn = init_db_instance()
    df = conn.select_table(query)
    data = list(df.to_dict("list").values())[0]
    return data

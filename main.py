from client.engine import Engine
from config import logger
from database.helper import init_db_instance, load_exchanges
from transformer import Agent


def main():
    logger.info("Loading exchanges...")
    exchanges = load_exchanges()
    logger.info(f"{len(exchanges)} Exchanges loaded from database.")
    logger.info("Initializing Engine...")
    engine = Engine(exchanges)
    logger.info("Engine initialized successfully.")
    logger.info("Running Engine...")
    engine.run()
    logger.info("Engine run completed successfully.")

    logger.info("Transforming data...")
    transformer = Agent(engine.exchanges, engine.tickers)
    tables = transformer.transform()

    logger.info("Saving data to database...")
    conn = init_db_instance()
    for t, dataframe in tables.items():
        if not dataframe.empty:
            logger.info(f"\n{dataframe}")
            conn.insert_table(dataframe, t)

    logger.info("Process completed successfully")


if __name__ == "__main__":
    main()

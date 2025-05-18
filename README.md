# EODHD Exchange Ticker Ingestion Pipeline

This project automates the retrieval and storage of ticker metadata from the **EOD Historical Data API**. It fetches all available instruments listed on each exchange, processes the data, and stores it in a SQL Server database for downstream use in analytics, financial systems, and platform onboarding.

## Overview

### Purpose

This ETL pipeline is designed to:
- Connect to the EODHD API and retrieve all symbols (tickers) listed under each supported exchange.
- Enrich and standardize the data (e.g., generating `eodhd_ticker` codes like `AAPL.US`).
- Insert the resulting dataset into a structured SQL Server table.

It enables users to maintain an up-to-date repository of global financial instruments tied to exchange listings.

## Source of Data

The data originates from the [EOD Historical Data API](https://eodhistoricaldata.com/) and uses the following endpoints:
- `/exchanges-list`: Lists all supported stock exchanges.
- `/exchange-symbol-list/{exchange}`: Lists tickers for a specific exchange.

The API requires a valid token passed as a query parameter.

## Application Flow

Execution starts in `main.py` and proceeds through these stages:

1. **Load Exchange List**:
   - The database is queried using `EXCHANGES_DB_QUERY` to retrieve a list of exchange codes to process.

2. **Initialize Engine**:
   - A custom `Engine` handles per-exchange ticker collection.

3. **Fetch Ticker Data**:
   - Each exchange’s ticker list is requested via the API.
   - For each symbol, metadata is recorded and a canonical `eodhd_ticker` is generated.

4. **Transform & Load**:
   - The `transformer.Agent` prepares the full dataset for loading.
   - Tickers are inserted into the designated SQL Server table using batch insertion.

## Project Structure

```
eodhd-tickers-main/
├── client/               # EODHD API logic and ticker engine
│   ├── engine.py         # Fetches tickers from exchanges
│   └── eodhd.py          # API client for endpoints
├── config/               # Environment and logging
├── database/             # MSSQL connection and helpers
├── transformer/          # Data transformation utilities
├── main.py               # Pipeline entrypoint
├── .env.sample           # Template for configuration variables
├── Dockerfile            # Containerization support
```

## Environment Variables

You must configure a `.env` file based on `.env.sample`. Key variables include:

| Variable | Description |
|----------|-------------|
| `TOKEN` | EODHD API token |
| `EXCHANGES_DB_QUERY` | SQL query to retrieve the list of exchange codes |
| `TICKERS_OUTPUT_TABLE` | SQL Server table to insert ticker data |
| `MSSQL_*` | SQL Server credentials and configuration |
| `REQUEST_MAX_RETRIES`, `REQUEST_BACKOFF_FACTOR` | Retry logic for HTTP requests |
| `INSERTER_MAX_RETRIES` | Retry limit for database inserts |

## Docker Support

You can run the application as a containerized job:

### Build
```bash
docker build -t eodhd-tickers .
```

### Run
```bash
docker run --env-file .env eodhd-tickers
```

## Requirements

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

Key packages used:
- `requests`: For API communication
- `pandas`: For data transformation
- `pyodbc` + `SQLAlchemy`: For SQL Server interaction
- `fast-to-sql`: For efficient batch inserts
- `python-decouple`: For .env config management

## Running the Pipeline

After preparing the `.env` file:

```bash
python main.py
```

Logs will report:
- Number of exchanges processed
- Ticker count fetched and inserted
- Any API or DB issues encountered

## License

This project is released under the MIT License. Use of the EODHD API must comply with their terms of service and rate limitations.

import yaml

from db.init_db import init_db
from etl.extract import extract_all
from etl.load import load_to_sqlite
from etl.logger import setup_logger
from etl.transform import transform
from etl.validate import validate


def _log_table_counts(logger, title: str, dfs: dict) -> None:
    logger.info(title)
    for table_name, df in dfs.items():
        logger.info("  - %s: %s rows", table_name, len(df))


def main():
    logger = setup_logger()

    with open("config/config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    raw_dir = cfg["paths"]["raw_dir"]
    db_path = cfg["paths"]["db_path"]
    tables = cfg["tables"]

    logger.info("Starting ETL pipeline")

    logger.info("Initializing database")
    init_db(db_path=db_path, schema_path="db/schema.sql")

    logger.info("Extracting data")
    dfs = extract_all(raw_dir=raw_dir, tables=tables)
    _log_table_counts(logger, "Extracted tables", dfs)

    logger.info("Transforming data")
    cleaned = transform(dfs)
    _log_table_counts(logger, "Transformed tables", cleaned)

    logger.info("Validating data")
    validate(cleaned)
    logger.info("Validation passed")

    logger.info("Loading data into SQLite")
    load_to_sqlite(db_path=db_path, cleaned=cleaned)

    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    main()
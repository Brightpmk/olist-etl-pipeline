import yaml
from etl.logger import setup_logger
from db.init_db import init_db
from etl.extract import extract_all
from etl.transform import transform
from etl.load import load_to_sqlite
from etl.validate import validate

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

    logger.info("Transforming data")
    cleaned = transform(dfs)

    logger.info("Validating data")
    validate(cleaned)
    
    logger.info("Loading data into SQLite")
    load_to_sqlite(db_path=db_path, cleaned=cleaned)

    logger.info("ETL pipeline completed successfully")
    


if __name__ == "__main__":
    main()

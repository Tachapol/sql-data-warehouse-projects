import psycopg2
from pathlib import Path
from load_bronze import load_bronze

# ==============================
# Database Config
# ==============================
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "dwh",
    "user": "postgres",
    "password": "postgres"
}

# ==============================
# SQL Paths
# ==============================
INIT_DB = Path("scripts/init_database.sql")
DDL_BRONZE = Path("scripts/bronze/ddl_bronze.sql")
DDL_SILVER = Path("scripts/silver/ddl_silver.sql")
LOAD_SILVER = Path("scripts/silver/load_silver.sql")
DDL_GOLD = Path("scripts/gold/ddl_gold.sql")

def run_sql_file(cursor, file_path):
    print(f"\nRunning {file_path}...")
    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    with open(file_path, "r", encoding="utf-8") as f:
        cursor.execute(f.read())

    print("Done.")

def main():
    print("======================================")
    print("Starting Full ETL Pipeline")
    print("======================================")

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 🔁 Drop Gold First (dependency safe)
        print("\nDropping Gold Views...")
        cursor.execute("DROP VIEW IF EXISTS gold.fact_sales CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS gold.dim_products CASCADE;")
        cursor.execute("DROP VIEW IF EXISTS gold.dim_customers CASCADE;")

        # 0️⃣ Init Schemas
        run_sql_file(cursor, INIT_DB)

        # 1️⃣ Bronze DDL
        run_sql_file(cursor, DDL_BRONZE)

        # 2️⃣ Bronze Load
        load_bronze(cursor)

        # 3️⃣ Silver DDL
        run_sql_file(cursor, DDL_SILVER)

        # 4️⃣ Deploy Silver Procedure
        run_sql_file(cursor, LOAD_SILVER)

        # 5️⃣ Execute Silver Load
        print("\nCalling silver.load_silver()...")
        cursor.execute("CALL silver.load_silver();")

        # 6️⃣ Gold DDL
        run_sql_file(cursor, DDL_GOLD)

        conn.commit()
        print("\n🎉 ETL Pipeline Completed Successfully!")

    except Exception as e:
        conn.rollback()
        print("\n❌ Pipeline Failed:")
        print(e)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
from pathlib import Path

BASE_PATH = Path("datasets")

TABLE_FILE_MAPPING = {
    "crm_cust_info": BASE_PATH / "source_crm" / "cust_info.csv",
    "crm_prd_info": BASE_PATH / "source_crm" / "prd_info.csv",
    "crm_sales_details": BASE_PATH / "source_crm" / "sales_details.csv",
    "erp_loc_a101": BASE_PATH / "source_erp" / "loc_a101.csv",
    "erp_cust_az12": BASE_PATH / "source_erp" / "cust_az12.csv",
    "erp_px_cat_g1v2": BASE_PATH / "source_erp" / "px_cat_g1v2.csv",
}

def load_bronze(cursor):
    print("\n🔄 Loading Bronze Layer...")

    for table, path in TABLE_FILE_MAPPING.items():
        print(f"  → {table}")

        if not path.exists():
            raise FileNotFoundError(f"{path} not found")

        cursor.execute(f"TRUNCATE TABLE bronze.{table};")

        with open(path, "r", encoding="utf-8") as f:
            cursor.copy_expert(
                f"COPY bronze.{table} FROM STDIN WITH CSV HEADER",
                f
            )

    print("✅ Bronze Load Complete")
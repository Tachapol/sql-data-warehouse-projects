-- Duplicate or NULL PK
SELECT cst_id
FROM silver.crm_cust_info
GROUP BY cst_id
HAVING COUNT(*) > 1 OR cst_id IS NULL;

-- Unwanted spaces
SELECT cst_key
FROM silver.crm_cust_info
WHERE cst_key <> TRIM(cst_key);

-- Marital status consistency
SELECT DISTINCT cst_marital_status
FROM silver.crm_cust_info;

-- == CRM PRODUCT ==
-- Duplicate or NULL PK
SELECT prd_id
FROM silver.crm_prd_info
GROUP BY prd_id
HAVING COUNT(*) > 1 OR prd_id IS NULL;

-- Unwanted spaces
SELECT prd_nm
FROM silver.crm_prd_info
WHERE prd_nm <> TRIM(prd_nm);

-- Negative or NULL cost
SELECT prd_cost
FROM silver.crm_prd_info
WHERE prd_cost < 0 OR prd_cost IS NULL;

-- Invalid date order
SELECT *
FROM silver.crm_prd_info
WHERE prd_end_dt < prd_start_dt;

-- == CRM SALES ==
-- Invalid date order
SELECT *
FROM silver.crm_sales_details
WHERE sls_order_dt > sls_ship_dt
   OR sls_order_dt > sls_due_dt;

-- Sales consistency
SELECT *
FROM silver.crm_sales_details
WHERE sls_sales <> sls_quantity * sls_price
   OR sls_sales IS NULL
   OR sls_quantity IS NULL
   OR sls_price IS NULL
   OR sls_sales <= 0
   OR sls_quantity <= 0
   OR sls_price <= 0;

-- == ERP CUSTOMER ==
SELECT bdate
FROM silver.erp_cust_az12
WHERE bdate < DATE '1924-01-01'
   OR bdate > CURRENT_DATE;

SELECT DISTINCT gen
FROM silver.erp_cust_az12;

-- == ERP LOCATION ==
SELECT DISTINCT cntry
FROM silver.erp_loc_a101
ORDER BY cntry;

-- == ERP CATEGORY ==
SELECT *
FROM silver.erp_px_cat_g1v2
WHERE cat <> TRIM(cat)
   OR subcat <> TRIM(subcat)
   OR maintenance <> TRIM(maintenance);

SELECT DISTINCT maintenance
FROM silver.erp_px_cat_g1v2;
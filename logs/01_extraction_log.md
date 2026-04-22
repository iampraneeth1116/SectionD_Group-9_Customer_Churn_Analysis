# Notebook Log — `01_extraction.ipynb`

**Project:** Olist Customer Churn Analysis  
**Capstone:** NST DVA Capstone 2 — Section D, Group 9  
**Role:** ETL Stage 1 — Raw data inspection and quality audit  
**Status:** Complete  
**Output:** No files written. All raw data untouched.

---

## What This Notebook Does

Loads all 7 raw Olist CSV files and performs a full structural and quality audit. No data is modified or saved. The sole purpose is to document every issue found in the raw data so that `02_cleaning.ipynb` has a clear, referenced action plan.

---

## Section-by-Section Log

### Section 1 — Imports & Project Path Setup
- Imported `pandas`, `numpy`, `pathlib.Path`
- `PROJECT_ROOT` resolved relative to notebook location using the template pattern — works from both `/notebooks/` and repo root
- `RAW_DIR` set to `data/raw/`

### Section 2 — Raw File Path Definitions
- All 7 file paths defined as named constants (`PATH_ORDERS`, `PATH_CUSTOMERS`, etc.)
- Existence check run on all 7 — all confirmed present

### Section 3 — Load All Raw Datasets
- All 7 CSVs loaded into named DataFrames: `df_orders`, `df_customers`, `df_items`, `df_payments`, `df_reviews`, `df_products`, `df_category`
- No transformation applied at load
- Shapes confirmed:

| DataFrame | Rows | Cols |
|---|---|---|
| df_orders | 99,441 | 8 |
| df_customers | 99,441 | 5 |
| df_items | 112,650 | 7 |
| df_payments | 103,886 | 5 |
| df_reviews | 99,224 | 7 |
| df_products | 32,951 | 9 |
| df_category | 71 | 2 |

### Section 4 — Schema Inspection (dtypes)
- All 5 timestamp columns in `df_orders` stored as `object` → require `pd.to_datetime()` in NB02
- `shipping_limit_date` in `df_items` stored as `object` → same fix needed
- `review_creation_date` and `review_answer_timestamp` in `df_reviews` stored as `object` → same fix needed
- All numeric columns (`price`, `freight_value`, `review_score`, etc.) correctly typed as `float64`

### Section 5 — Head Preview
- First 3 rows of each table displayed for visual sanity check
- Values confirmed sensible across all 7 tables

### Section 6 — Null Audit
Nulls found:

| Table | Column | Null Count | % | Action in NB02 |
|---|---|---|---|---|
| df_orders | order_approved_at | 160 | 0.2% | Fill with order_purchase_timestamp |
| df_orders | order_delivered_carrier_date | 1,783 | 1.8% | Drop after filter to delivered |
| df_orders | order_delivered_customer_date | 2,965 | 3.0% | Drop after filter to delivered |
| df_reviews | review_comment_title | 87,656 | 88.3% | Fill with 'no_comment' (optional field) |
| df_reviews | review_comment_message | 58,247 | 58.7% | Fill with 'no_comment' (optional field) |
| df_products | product_category_name | 610 | 1.9% | Fill with 'unknown' |
| df_products | dimension cols | 2 | ~0% | Drop those 2 rows |

No nulls in `df_customers`, `df_items`, `df_payments`, or `df_category`.

### Section 7 — Duplicate Audit
- Zero exact row duplicates found across all 7 tables
- `order_id` confirmed unique in `df_orders`
- `customer_id` confirmed unique in `df_customers` (one row per order-customer pair)
- `customer_unique_id` is NOT unique in `df_customers` — same real customer appears multiple times with different `customer_id` values (one per order). This is by design in the Olist schema.
- `order_id + order_item_id` confirmed as composite primary key in `df_items`

### Section 8 — Order Status Distribution
- `delivered`: 96,478 rows (97.0%) — the only status retained for analysis
- `shipped`: 1,107 rows
- `canceled`: 625 rows
- `unavailable`, `invoiced`, `processing`, `created`, `approved`: remainder
- **Decision documented:** filter to `delivered` only in NB02. Non-delivered orders cannot contribute to churn behaviour analysis.

### Section 9 — Customer Identity Audit
- `customer_id` unique count: 99,441 (one per row — per-order identifier)
- `customer_unique_id` unique count: 96,096 (real customers)
- Difference of ~3,345 means those real customers placed more than one order
- **Critical finding:** churn label must be built on `customer_unique_id`, not `customer_id`. Using `customer_id` would incorrectly label every customer as a one-time buyer.

### Section 10 — Column Name Quality Check
- Two typos found in `df_products`:
  - `product_name_lenght` → will be renamed to `product_name_length` in NB02
  - `product_description_lenght` → will be renamed to `product_description_length` in NB02
- All other column names across all 7 tables are clean

### Section 11 — Join Key Audit
- `items.order_id` vs `orders.order_id`: all matched, 0 orphaned
- `payments.order_id` vs `orders.order_id`: all matched, 0 orphaned
- `reviews.order_id` vs `orders.order_id`: small number of orphaned review records (orders not in the orders table) — will be lost on left join from orders spine, which is correct
- `items.product_id` vs `products.product_id`: all matched
- `products.product_category_name` vs `category.product_category_name`: small number of untranslated categories — these become nulls in `product_category_name_english` after join, handled in NB02

### Section 12 — Schema Summary Table
- Consolidated reference table of all 7 raw files printed (primary keys, join columns, key nulls)
- This table is reproduced in `docs/data_dictionary.md`

### Section 13 — Extraction Audit Summary
Full handoff table to NB02 listing 14 documented issues with their exact cleaning actions. Covers: datetime casting (8 columns), null handling (5 columns across 3 tables), column rename typos (2), order status filter (1), and churn label design decision (1).

---

## Key Decisions Documented

1. **Filter to `delivered` only** — non-delivered orders excluded from all downstream analysis
2. **Use `customer_unique_id` for churn** — not `customer_id`, which is per-order not per-customer
3. **`review_comment_*` nulls are expected** — optional fields, not data quality failures
4. **All joins will be LEFT from `df_orders`** — orders table is the spine

---

## Handoff to NB02

All 14 issues catalogued in Section 13 have explicit cleaning actions in `02_cleaning.ipynb`. No data was modified in this notebook. All 7 files in `data/raw/` remain untouched.

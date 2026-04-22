# Notebook Log — `02_cleaning.ipynb`

**Project:** Olist Customer Churn Analysis  
**Capstone:** NST DVA Capstone 2 — Section D, Group 9  
**Role:** ETL Stage 2 — Full cleaning pipeline, table merging, feature engineering, and export  
**Status:** Complete  
**Output:** `data/processed/olist_churn_master.csv` — 105,000 rows, 19 columns

---

## What This Notebook Does

Takes all 7 raw Olist CSVs, applies cleaning transformations, merges them into a single flat master table, engineers the churn label and key analytical columns, reduces to a stratified representative sample, and saves the final processed file. Also writes `docs/data_dictionary.md` and updates `scripts/etl_pipeline.py`.

---

## Section-by-Section Log

### Section 1 — Imports & Project Path Setup
- Imported `pandas`, `numpy`, `pathlib`, `sys`
- `basic_clean` imported from `scripts/etl_pipeline.py`
- `PROJECT_ROOT` resolved using template pattern — works from both `/notebooks/` and repo root
- `PROCESSED_DIR` created if not already present
- Output path set to `data/processed/olist_churn_master.csv`

### Section 2 — Load All 7 Raw Datasets
- All 7 CSVs loaded and immediately passed through `basic_clean()`, which:
  - Strips whitespace from all string columns
  - Drops exact duplicate rows
  - Normalises column names to snake_case
- Shapes confirmed post-load — no rows unexpectedly dropped by `basic_clean`

### Section 3 — Fix Column Name Typos
- Two typos in `df_products` corrected via explicit `rename()`:
  - `product_name_lenght` → `product_name_length`
  - `product_description_lenght` → `product_description_length`
- Flagged in NB01 Step 10; fixed here before any downstream reference

### Section 4 — Datetime Casting
- 8 timestamp columns cast from `object` to `datetime64` using `pd.to_datetime(..., errors='coerce')`:
  - `df_orders`: `order_purchase_timestamp`, `order_approved_at`, `order_delivered_carrier_date`, `order_delivered_customer_date`, `order_estimated_delivery_date`
  - `df_items`: `shipping_limit_date`
  - `df_reviews`: `review_creation_date`, `review_answer_timestamp`
- `errors='coerce'` used throughout — unparseable values become `NaT` rather than raising exceptions

### Section 5 — Filter to Delivered Orders
- `df_orders` filtered to `order_status == 'delivered'` only
- Rows before: 99,441 | Rows after: 96,478 | Dropped: ~2,963
- Decision rationale: non-delivered orders (cancelled, processing, shipped, etc.) cannot contribute to churn behaviour analysis as they represent incomplete transactions

### Section 6 — Null Handling in df_orders
- `order_approved_at` (160 nulls): filled with `order_purchase_timestamp` — approval timestamp not recorded for these orders; purchase timestamp is the closest valid proxy
- `order_delivered_carrier_date` (residual nulls): rows dropped — a confirmed delivered order must have a carrier pickup record
- `order_delivered_customer_date` (residual nulls): rows dropped — a confirmed delivered order must have a delivery confirmation date

### Section 7 — Null Handling in df_products
- `product_category_name` (610 nulls): filled with `'unknown'` — dropping these would remove valid product entries from the join
- Dimension columns (`product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`) — 2 rows with nulls dropped — same 2 rows as missing category; no usable data

### Section 8 — Null Handling in df_reviews
- `review_comment_title` (87,656 nulls): filled with `'no_comment'`
- `review_comment_message` (58,247 nulls): filled with `'no_comment'`
- Both are optional fields by design on the Olist platform. Dropping these rows would destroy the review join entirely. `'no_comment'` makes the absence explicit.

### Section 9 — Six-Table Merge
All joins are LEFT from `df_orders` (the spine). Merge sequence:

| Merge | Join Key | Type | Shape After |
|---|---|---|---|
| orders + customers | customer_id | LEFT | ~93,357 × 12 |
| + items | order_id | LEFT | ~115,000+ × 18 |
| + payments | order_id | LEFT | ~130,000+ × 22 |
| + products | product_id | LEFT | ~130,000+ × 30 |
| + category translation | product_category_name | LEFT | ~130,000+ × 31 |
| + reviews | order_id | LEFT | ~130,000+ × 37 |

Row count increase from orders spine is expected — `df_items` and `df_payments` are one-to-many per order.

### Section 10 — Merge Verification
- `df_master.shape` confirmed — no unexpected row explosion
- `customer_unique_id` null count confirmed as 0
- `review_score` nulls noted (~8% of rows have no review — valid data gap)
- `product_category_name_english` nulls noted

### Section 10a — Post-Merge Null Fix
- `product_category_name_english` nulls filled with `'unknown'` after merge
- These are products whose Portuguese category name had no entry in the translation table
- Filled rather than dropped to avoid losing valid order rows; `'unknown'` makes them visible in Tableau filters

### Section 11 — Churn Label Engineering
- `churn` label defined at `customer_unique_id` level (not `customer_id`)
- Logic: count distinct `order_id` per `customer_unique_id` → `churn = 1` if count == 1, `churn = 0` if count >= 2
- Merged back to `df_master`
- **Result:** ~92–93% churn rate — this is a genuine Olist business characteristic (most customers are one-time buyers), not a data error

### Section 12 — delivery_delay_days Engineering
- Formula: `(order_delivered_customer_date − order_estimated_delivery_date).dt.days`
- Positive = arrived late, Negative = arrived early, Zero = on time
- Key analytical feature for churn correlation analysis in NB03

### Section 13 — order_revenue Engineering
- Formula: `price + freight_value`
- Represents total value of one item line including shipping cost
- Will be aggregated per order / per customer in NB03 for revenue KPIs

### Section 14 — Final Column Selection
- 19 columns selected from the full merged dataframe; all internal ID and redundant columns dropped
- Columns kept:

| Column | Reason Kept |
|---|---|
| order_id | Row identifier |
| customer_unique_id | Real customer identifier for churn |
| customer_state, customer_city | Geographic grouping |
| order_purchase_timestamp | Time-series analysis |
| order_delivered_customer_date | Delivery performance |
| order_estimated_delivery_date | Delivery delay calculation |
| order_status | Always 'delivered'; kept for documentation |
| price, freight_value | Raw revenue components |
| order_revenue | Engineered total item value |
| payment_type, payment_installments, payment_value | Payment behaviour features |
| review_score | Customer satisfaction |
| review_comment_message | Optional NLP use in NB04 |
| product_category_name_english | Category-level analysis |
| delivery_delay_days | Delivery performance feature |
| churn | Target variable |

### Section 15 — Pre-Sample Quality Check
- `df_master.isnull().sum()` confirmed: only `review_score` and `review_comment_message` have residual nulls (expected)
- Churn distribution printed and confirmed
- Churn rate explicitly noted as a real business finding, not an error

### Section 16 — Stratified Sampling
- Target: 105,000 rows
- Method: `groupby('churn').sample(frac=frac, random_state=42)` — pandas 3.x safe syntax
- Stratifying on `churn` preserves the original 0/1 class distribution in the sample
- `random_state=42` ensures reproducibility
- Churn rate confirmed unchanged after sampling

### Section 17 — Save Output
- `df_master.to_csv(PROCESSED_PATH, index=False)`
- Saved to: `data/processed/olist_churn_master.csv`
- Final shape: 105,000 rows × 19 columns

### Section 18 — data_dictionary.md Written
- `docs/data_dictionary.md` written from Python
- Documents all 19 columns with data type, description, example value, usage, and cleaning notes
- Derived columns (`churn`, `delivery_delay_days`, `order_revenue`) documented with their exact formulas
- Sampling note included

### Section 19 — etl_pipeline.py Updated
- `scripts/etl_pipeline.py` rewritten with 6 project-specific functions added alongside the original `basic_clean`:
  - `cast_order_datetimes()` — datetime casting for all 5 order timestamp columns
  - `engineer_delivery_delay()` — `delivery_delay_days` column
  - `engineer_order_revenue()` — `order_revenue` column
  - `engineer_churn_label()` — churn label at `customer_unique_id` level
  - `stratified_sample()` — pandas 3.x-safe stratified sampling on churn
  - `save_processed()` — write output CSV

### Section 20 — Final Summary & Verification
- Summary transformation table printed covering all pipeline steps with row counts
- `olist_churn_master.csv` re-read and verified: shape, columns, churn rate, total null count confirmed

---

## Full Transformation Summary

| Step | Action | Rows Before | Rows After |
|---|---|---|---|
| Load + basic_clean | Whitespace strip, dedup, snake_case columns | 99,441 | 99,441 |
| Fix typos | Rename 2 product columns | — | — |
| Cast datetimes | 8 columns to datetime64 | — | — |
| Filter to delivered | Drop non-delivered statuses | 99,441 | 96,478 |
| Null handling — orders | Fill approved_at; drop 2 delivery null groups | 96,478 | ~93,357 |
| Null handling — products | Fill category nulls; drop 2 dimension rows | 32,951 | 32,949 |
| Null handling — reviews | Fill comment nulls with 'no_comment' | 99,224 | 99,224 |
| Six-table merge | Left joins from orders spine | ~93,357 | ~130,000+ |
| Post-merge null fix | Fill product_category_name_english nulls | — | — |
| Churn label | Count orders per customer_unique_id | — | — |
| Feature engineering | delivery_delay_days, order_revenue | — | — |
| Column selection | Keep 19 of ~37 columns | — | 19 cols |
| Stratified sample | Sample to 105,000 rows on churn | ~130,000+ | 105,000 |
| Save | Write olist_churn_master.csv | — | — |

---

## Output File

| Property | Value |
|---|---|
| Path | `data/processed/olist_churn_master.csv` |
| Rows | 105,000 |
| Columns | 19 |
| Churn rate | ~92–93% |
| Known nulls | review_score (~8%), review_comment_message (~8%) — expected |
| Datetime columns | Stored as strings in CSV — re-cast with `pd.to_datetime()` in NB03 on load |

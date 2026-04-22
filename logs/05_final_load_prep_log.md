# Notebook Log — `05_final_load_prep.ipynb`

**Project:** Olist Customer Churn Analysis  
**Capstone:** NST DVA Capstone 2 — Section D, Group 9  
**Role:** ETL Stage 5 — KPI engineering and Tableau export preparation  
**Status:** Complete  
**Input:** `data/processed/olist_churn_master.csv` (105,000 × 19)  
**Outputs:** 4 CSV files in `data/processed/`

---

## What This Notebook Does

Reads the cleaned master dataset, engineers additional analytical columns and KPI aggregations, and exports 4 purpose-built CSV files for the Tableau dashboard. No raw data is touched. This is the final stage of the ETL pipeline.

---

## Output Files Summary

| File | Rows | Cols | Used For |
|---|---|---|---|
| `tableau_ready.csv` | 105,000 | 24 | Primary Tableau data source — all order-level charts |
| `customers_kpi.csv` | ~85,994 | 11 | Customer segmentation views |
| `monthly_kpi.csv` | 23 | 9 | Time-series trend charts |
| `state_kpi.csv` | 27 | 10 | Geographic map view |

---

## Section-by-Section Log

### Section 1 — Imports & Path Setup
- Libraries: `pandas`, `numpy`, `pathlib` only
- `PROJECT_ROOT` resolved using standard template pattern
- All 4 output paths defined as named constants
- `PROCESSED_DIR` created if not present

### Section 2 — Load Master Dataset & Re-Parse Timestamps
- `olist_churn_master.csv` loaded (105,000 × 19)
- Three timestamp columns re-cast to `datetime64` using `pd.to_datetime(errors='coerce')`:
  - `order_purchase_timestamp`
  - `order_delivered_customer_date`
  - `order_estimated_delivery_date`
- Re-parsing explicitly documented — CSV format stores datetimes as strings, not a pipeline bug
- Shape (105,000 × 19) and churn distribution confirmed after load

### Section 3 — Engineer New Columns

Three new columns added to `df`:

**`days_to_deliver`**
- Formula: `(order_delivered_customer_date − order_purchase_timestamp).dt.days`
- Measures raw logistics duration — how many days the customer actually waited from order to delivery
- Different from `delivery_delay_days` (which measures lateness vs estimate); this is the absolute wait time
- Descriptive stats printed; nulls checked

**`review_bucket`**
- Categorical grouping of `review_score`:
  - `'Low (1-2)'` — dissatisfied
  - `'Medium (3)'` — neutral
  - `'High (4-5)'` — satisfied
  - `'No Review'` — null score
- Applied via function with `pd.isna()` guard
- Distribution printed after engineering

**`delivery_bucket`**
- Categorical grouping of `delivery_delay_days`:
  - `'Early'` — delay < 0
  - `'On-time'` — delay == 0
  - `'Late'` — delay 1–7 days
  - `'Severely Late'` — delay > 7 days
- Distribution printed after engineering

### Section 4 — Scalar KPIs (Headline Numbers)
10 single-value KPIs computed for dashboard Page 1 tiles:

| KPI | Formula |
|---|---|
| total_orders | `df['order_id'].nunique()` |
| total_customers | `df['customer_unique_id'].nunique()` |
| total_revenue | `df['order_revenue'].sum()` |
| avg_order_value | `df['order_revenue'].mean()` |
| overall_churn_rate | `df['churn'].mean() * 100` |
| repeat_customer_rate | `100 - overall_churn_rate` |
| on_time_delivery_rate | `(delivery_delay_days <= 0).sum() / len(df) * 100` |
| avg_review_score | `df['review_score'].mean()` |
| avg_delivery_delay | `df['delivery_delay_days'].mean()` |
| avg_days_to_deliver | `df['days_to_deliver'].mean()` |

All values printed and stored in a dict (for reference; not saved as a separate file).

### Section 5 — Customer-Level KPI Table (`customers_kpi.csv`)
Grouped by `customer_unique_id`. One row per real customer.

Columns computed:
- `order_count` — distinct orders placed
- `total_spend` — sum of order_revenue
- `avg_order_value` — mean order_revenue
- `avg_delivery_delay` — mean delivery_delay_days
- `avg_days_to_deliver` — mean days_to_deliver
- `avg_review_score` — mean review_score
- `top_payment_type` — mode of payment_type across orders
- `top_category` — mode of product_category_name_english across orders
- `customer_state` — state (first value, consistent per customer)
- `churn` — label carried through from master

Shape: ~85,994 rows × 11 columns (one row per unique customer)

### Section 6 — Monthly KPI Table (`monthly_kpi.csv`)
`order_month` extracted as year-month string (e.g. `'2017-09'`) from `order_purchase_timestamp`. Stored as string for clean CSV round-tripping and Tableau date parsing.

Grouped by `order_month`. One row per calendar month.

Columns:
- `total_orders` — distinct order_id count
- `total_revenue` — sum of order_revenue
- `avg_order_value` — mean order_revenue
- `churn_rate_pct` — mean churn × 100
- `avg_delivery_delay` — mean delivery_delay_days
- `avg_days_to_deliver` — mean days_to_deliver
- `avg_review_score` — mean review_score
- `on_time_rate_pct` — % of orders with delay ≤ 0

Shape: 23 rows × 9 columns (23 months of data)

### Section 7 — State-Level KPI Table (`state_kpi.csv`)
Two-step aggregation to avoid row duplication bias in churn rate:
1. Customer-level churn computed first per state (count churned / count total customers)
2. Operational metrics (revenue, delay, etc.) aggregated at row level per state
3. Two results merged on `customer_state`

Columns:
- `customer_state` — two-letter Brazilian state code
- `total_orders` — distinct order count
- `total_customers` — distinct customer_unique_id count
- `total_revenue` — sum of order_revenue
- `avg_order_value` — mean order_revenue
- `avg_delivery_delay` — mean delivery_delay_days
- `avg_days_to_deliver` — mean days_to_deliver
- `avg_review_score` — mean review_score
- `on_time_rate_pct` — % on-time deliveries
- `churn_rate_pct` — customer-level churn rate for the state

Shape: 27 rows × 10 columns (one per Brazilian state)

### Section 8 — Category & Payment KPIs (Inline, Not Saved)
Category and payment type KPIs computed and printed for documentation purposes only. Not saved as separate files — Tableau computes these live from `tableau_ready.csv`.

Category KPI: grouped by `product_category_name_english` → total_orders, total_revenue, avg_order_value, churn_rate_pct, avg_review_score. Top 15 by revenue printed.

Payment KPI: grouped by `payment_type` → same metrics. Printed inline.

### Section 9 — Build Tableau-Ready Export (`tableau_ready.csv`)
`order_year` added as integer year extracted from `order_purchase_timestamp`.

Final column order defined (24 columns):
- Identifiers: `order_id`, `customer_unique_id`
- Geography: `customer_state`, `customer_city`
- Timestamps: `order_purchase_timestamp`, `order_delivered_customer_date`, `order_estimated_delivery_date`
- Date dimensions: `order_year`, `order_month`
- Order facts: `order_status`, `price`, `freight_value`, `order_revenue`
- Payment: `payment_type`, `payment_installments`, `payment_value`
- Review: `review_score`, `review_comment_message`, `review_bucket`
- Product: `product_category_name_english`
- Delivery: `delivery_delay_days`, `days_to_deliver`, `delivery_bucket`
- Target: `churn`

### Section 10 — Final Null Audit & Fix Before Export
Pre-export null check on `df_tableau`:
- `review_score` — residual nulls filled with column **median** (not mean, to avoid outlier influence)
- `payment_type` — residual nulls filled with `'unknown'`
- `days_to_deliver` — any NaT-derived nulls filled with column **median**
- Zero nulls confirmed across all 24 columns after fixes

### Section 11 — Save All 4 Output Files
All files saved with `index=False`:
1. `tableau_ready.csv` → 105,000 × 24
2. `customers_kpi.csv` → ~85,994 × 11
3. `monthly_kpi.csv` → 23 × 9
4. `state_kpi.csv` → 27 × 10

### Section 12 — Final Verification
All 4 files re-read from disk and verified:
- Shape confirmed (explicit check for `tableau_ready.csv` against (105,000, 24))
- Total null count confirmed as 0 across all files
- Column list printed for each file

### Section 13 — Pipeline Summary
Full transformation table printed covering all 13 steps from load to save.

---

## Full Transformation Summary

| Step | Action | Output |
|---|---|---|
| Load + re-parse | Read master CSV, cast 3 timestamp cols | 105,000 × 19 |
| Engineer days_to_deliver | Date arithmetic: delivered − purchased | New column |
| Engineer review_bucket | Score → Low / Medium / High / No Review | New column |
| Engineer delivery_bucket | Delay → Early / On-time / Late / Severely Late | New column |
| Scalar KPIs | 10 headline metrics computed | Inline reference |
| Customer KPIs | Grouped by customer_unique_id | customers_kpi.csv (85,994 × 11) |
| Monthly KPIs | Grouped by order_month | monthly_kpi.csv (23 × 9) |
| State KPIs | Two-step aggregation by state | state_kpi.csv (27 × 10) |
| Category + Payment KPIs | Inline only | Not saved |
| Add order_year | Integer year from timestamp | New column |
| Null fix | Fill review_score, payment_type, days_to_deliver | 0 nulls remaining |
| Save 4 files | to_csv(index=False) | All outputs confirmed |
| Verify | Re-read all files, check shape + nulls | All passed |

---

## Notes for Downstream Use
- `tableau_ready.csv` is the primary source for all Tableau sheets — use this for order-level charts, filters, and drill-downs
- `state_kpi.csv`, `monthly_kpi.csv`, `customers_kpi.csv` are pre-aggregated — connect as separate data sources in Tableau for KPI summary sheets; do not join them to `tableau_ready.csv` inside Tableau (avoids row multiplication)
- `review_score` in `tableau_ready.csv` has been median-filled — no nulls remain
- Datetime columns in `tableau_ready.csv` written as ISO strings — Tableau parses these automatically as date dimensions

# Data Dictionary — olist_churn_master.csv

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | olist_churn_master |
| Source | Brazilian E-Commerce Public Dataset by Olist (Kaggle) |
| Raw files | olist_orders_dataset.csv, olist_customers_dataset.csv, olist_order_items_dataset.csv, olist_order_payments_dataset.csv, olist_order_reviews_dataset.csv, olist_products_dataset.csv, product_category_name_translation.csv |
| Processed by | notebooks/02_cleaning.ipynb |
| Granularity | One row per delivered order item (order_id × product) |
| Rows (processed) | ~50,000 (stratified sample on churn label — see NB02 Step 16) |
| Columns | 19 |

## Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| order_id | string | Unique identifier for each order | abc123 | Join key | No transformation; whitespace stripped |
| customer_unique_id | string | Canonical real-customer identifier. One real customer can have multiple customer_id values (one per order). Use this column — not customer_id — for all customer-level analysis | cust_xyz | Churn label, EDA, KPI | Sourced from df_customers; critical for churn definition |
| customer_state | string | Brazilian state code of the customer's address | SP | EDA, Tableau | Whitespace stripped |
| customer_city | string | Brazilian city of the customer's address | São Paulo | EDA, Tableau | Whitespace stripped |
| order_purchase_timestamp | datetime | Date and time the customer placed the order | 2018-01-15 12:30:00 | Time-series, EDA | Cast from string via pd.to_datetime(errors='coerce') |
| order_delivered_customer_date | datetime | Date the order was actually delivered to the customer | 2018-01-22 18:00:00 | delivery_delay_days, EDA | Cast from string; rows with null dropped (could not confirm delivery) |
| order_estimated_delivery_date | datetime | Estimated delivery date shown to customer at purchase | 2018-01-25 00:00:00 | delivery_delay_days | Cast from string |
| order_status | string | Always 'delivered' in this dataset (filtered in NB02 Step 5) | delivered | Documentation only | Filtered to delivered rows only |
| price | float | Price of the individual item in BRL | 49.90 | order_revenue, EDA | No transformation |
| freight_value | float | Freight (shipping) cost charged for the item in BRL | 8.72 | order_revenue, EDA | No transformation |
| order_revenue | float | Engineered: price + freight_value. Total value of this item including shipping | 58.62 | KPI, EDA, Tableau | Derived column: order_revenue = price + freight_value |
| payment_type | string | Payment method used (credit_card, boleto, voucher, debit_card) | credit_card | EDA, Tableau | Whitespace stripped |
| payment_installments | int | Number of payment installments chosen by customer | 3 | EDA, Statistical Analysis | No transformation |
| payment_value | float | Total payment amount for this payment record in BRL | 58.62 | EDA | No transformation |
| review_score | float | Customer review score (1–5). Some orders have no review; these appear as NaN | 5 | EDA, Statistical Analysis, Tableau | Left-joined from df_reviews; ~8% orders have no review |
| review_comment_message | string | Optional free-text review from customer. 'no_comment' where customer left no message | Great product! | Optional NLP (NB04) | Nulls filled with 'no_comment' — optional field by design |
| product_category_name_english | string | English translation of the product category | health_beauty | EDA, Tableau | Joined from translation table; replaces Portuguese product_category_name |
| delivery_delay_days | int | Engineered: (order_delivered_customer_date − order_estimated_delivery_date).dt.days. Positive = late, Negative = early, Zero = on time | 3 | EDA, Churn analysis, Tableau | Derived column. Key analytical feature for churn correlation |
| churn | int | Target variable. 1 = customer placed only one order in the full dataset (churned). 0 = customer placed 2 or more orders (retained) | 1 | All analysis, Tableau, Statistical modelling | Derived at customer_unique_id level. High churn rate (~97%) is a genuine Olist business characteristic, not a data error |

## Derived Columns

| Derived Column | Logic | Business Meaning |
|---|---|---|
| churn | 1 if customer_unique_id appears in exactly 1 order across entire dataset, else 0 | Whether a customer made only one purchase (churned) vs returned to buy again (retained) |
| delivery_delay_days | (order_delivered_customer_date − order_estimated_delivery_date).dt.days | How many days late (positive) or early (negative) the actual delivery was vs the estimated date |
| order_revenue | price + freight_value | Total monetary value of one item line including shipping; used to compute per-order and per-customer revenue KPIs |

## Data Quality Notes

- Dataset was filtered to `order_status == 'delivered'` only (~96,478 rows before sampling). Non-delivered orders were excluded as they cannot contribute to churn behaviour analysis.
- Rows where `order_delivered_customer_date` or `order_delivered_carrier_date` were null were dropped after the delivered filter — these represent incomplete delivery records.
- `order_approved_at` nulls (~160) were filled with `order_purchase_timestamp` as the approval timestamp was not recorded for those orders.
- The dataset was reduced to ~50,000 rows using stratified sampling on `churn` to preserve the original churn/retained distribution (see NB02 Step 16). The full pipeline can be re-run without sampling by changing `TARGET_N` in NB02.
- `review_score` is null for orders with no associated review (~8%). These are valid data gaps, not cleaning failures.
- `product_category_name_english` replaces the original Portuguese `product_category_name`. The Portuguese column is not included in the processed file.

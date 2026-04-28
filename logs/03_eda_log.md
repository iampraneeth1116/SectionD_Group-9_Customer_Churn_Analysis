# Notebook Log — `03_eda.ipynb`

**Project:** Olist Customer Churn Analysis  
**Capstone:** NST DVA Capstone 2 — Section D, Group 9  
**Role:** Exploratory Data Analysis — patterns, distributions, and churn drivers  
**Status:** Complete  
**Output:** No files written. All charts rendered inline.

---

## What This Notebook Does

Loads `olist_churn_master.csv` and performs a full exploratory analysis across 10 sections covering univariate distributions, time trends, geographic patterns, revenue composition, delivery performance, customer satisfaction, and multi-variable relationships. Produces business insights at each section.

---

## Section-by-Section Log

### Section 1 — Setup & Data Loading
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `pathlib`
- Style: `seaborn-v0_8-whitegrid`, `Set2` palette, `%matplotlib inline`
- Dataset loaded from `../data/processed/olist_churn_master.csv`
- Shape confirmed on load

### Section 2 — Dataset Overview
- Shape, memory usage, and dtypes printed via `df.info()`
- Missing value summary computed — only `review_score` and `review_comment_message` have residual nulls (~8%), both expected and acceptable
- `df.describe().T` printed for full numeric summary
- **Insight noted:** High variance in revenue and delay metrics signals need for customer segmentation

### Section 3 — Univariate Analysis
Four distributions examined:

**Order Revenue**
- Histogram with mean and median reference lines
- Right-skewed distribution — majority of orders are low value, a small segment drives high revenue
- Mean > Median confirming positive skew

**Delivery Delay**
- Histogram with on-time (0) and mean reference lines
- Most orders arrive early or on time; a long right tail of severely delayed orders
- Mean delay logged

**Review Scores**
- Bar chart across scores 1–5
- Score 5 dominates; scores 1–2 form a secondary cluster indicating a dissatisfied segment

**Payment Types**
- Bar chart — credit card overwhelmingly dominant
- Boleto (bank slip) second; debit card and voucher minimal

**Order Status**
- All rows confirmed as `delivered` — pipeline filter verified visually

**Churn Distribution**
- Bar chart showing retained (0) vs churned (1)
- Churn rate: ~92.9% — confirmed as genuine Olist characteristic, not a data error
- **Insight:** Severe revenue leakage from one-time buyers; requires lifecycle management pivot

### Section 4 — Time-Based Trends
- `order_purchase_timestamp` re-cast to datetime (CSV stores as string)
- `order_month` derived as Period column

**Monthly Order Volume**
- Line chart with area fill
- Clear growth trend from 2017 through mid-2018; peaks indicate seasonal demand spikes

**Monthly Revenue**
- Line chart with area fill — mirrors order volume trend
- Revenue surges correlate with order volume peaks
- **Insight:** Cyclical demand peaks stress logistics capacity; predictive planning required

### Section 5 — Customer & Geographic Analysis
- Top 15 states by order volume computed and plotted (horizontal bar)
- Top 15 states by total revenue computed and plotted (horizontal bar)
- SP (São Paulo) dominant in both volume and revenue by large margin
- RJ, MG follow as secondary markets
- **Insight:** Revenue concentrated in metropolitan states; identifies locations for potential distribution hubs

### Section 6 — Revenue Analysis
- Category-level aggregation: total revenue, average order value, order count
- Top 15 categories by total revenue plotted
- Top 15 categories by average order value plotted separately
- High-volume categories don't always have the highest AOV
- **Insight:** Revenue concentrated in small set of categories; high-AOV categories identified for targeted growth

### Section 7 — Delivery Performance Analysis
**Delivery Performance Breakdown**
- Three-bucket bar chart: On-time/Early, Delayed (>0 days), Severely Delayed (>7 days)
- Majority on time; meaningful tail of severely delayed orders

**Delivery Delay vs Churn (Boxplot)**
- Churned customers have a higher median delivery delay than retained customers
- Confirms delivery performance as a churn driver

**Delay Distribution (Histogram)**
- Majority of orders early or on time; right tail extends to extreme delays
- **Insight:** Higher delivery delay → higher churn. Logistics directly impacts retention.

### Section 8 — Customer Satisfaction & Reviews
**Churn Rate by Review Score**
- Bar chart: churn rate computed per review score bucket
- Score 1 and 2 customers have the highest churn rates
- Score 5 customers still churn at high rates (Olist baseline) but lower than low-scorers

**Delivery Delay vs Review Score (Boxplot)**
- Lower review scores associated with higher delivery delays
- Clear inverse relationship — worse logistics → worse reviews → higher churn

**Review Score Distribution**
- Bar chart — score 5 dominant; bi-modal pattern with secondary peak at 1
- **Insight:** 1–2 star ratings are leading churn indicators; warrants automatic intervention workflows

### Section 9 — Relationship Analysis

**A. Correlation Heatmap**
- Numeric columns: `price`, `freight_value`, `order_revenue`, `payment_value`, `payment_installments`, `review_score`, `delivery_delay_days`, `churn`
- Key correlations found:
  - `delivery_delay_days` ↑ → `churn` ↑ (positive)
  - `review_score` ↑ → `churn` ↓ (negative)
  - `price` and `freight_value` highly correlated with `order_revenue` (expected — derived column)
- **Insight:** Delay is the leading quantifiable churn driver; review score is the sentiment proxy

**B. Revenue vs Delivery Delay Scatter (5,000 row sample)**
- Points coloured by churn status (0 = green, 1 = red)
- High-revenue orders exposed equally to delivery delays
- Churned orders spread across all revenue levels — churn is not confined to low-value customers
- **Insight:** Premium transactions at risk from delays; VIP delivery tiers warranted

**C. State-wise Revenue Analysis**
- Top 10 states aggregated: total revenue, order count, average delay, churn rate

**Revenue vs Churn Rate (Dual Axis Bar)**
- Revenue bars (left axis) vs churn rate bars (right axis) per state
- High-revenue states still have high churn rates — revenue scale does not protect against churn

**Average Delivery Delay by State**
- Horizontal bar chart for top 10 states
- SP and other high-revenue states show meaningful average delays
- **Insight:** Logistics investment in top-revenue states would have the highest retention ROI

### Section 10 — Key Findings & Business Implications
Three executive directives documented:

1. **Address Logistics as Core Retention Driver** — delayed orders collapse customer lifetime value; localized logistics investment required in high-volume clusters
2. **Standardize Predictive Recovery** — 1-star ratings are leading churn indicators; automatic risk-intervention workflows recommended
3. **Safeguard High-Value Portfolios** — late premium transactions amplify revenue loss; VIP fulfillment tiers required

---

## Key Findings Summary

| Finding | Evidence |
|---|---|
| 92.9% churn rate | Churn distribution chart — genuine Olist characteristic |
| Delivery delay is the #1 churn driver | Boxplot + correlation heatmap |
| Low review scores precede churn | Churn rate by review score chart |
| Revenue concentrated in SP and top 5 states | Geographic bar charts |
| Revenue concentrated in ~5 product categories | Category revenue chart |
| High-revenue customers churn too | Scatter plot coloured by churn |
| Credit card dominant payment method | Payment type distribution |

---

## Libraries Used
`pandas`, `numpy`, `matplotlib.pyplot`, `seaborn` — no scipy, no statsmodels (those are in NB04)

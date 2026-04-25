# Tableau Dashboards - Customer Churn Analysis

This folder contains the final Tableau dashboards developed for the Olist Customer Churn Analysis project.

The dashboards present key insights on customer retention, behavior patterns, and churn drivers using an interactive and structured visual approach.

---

## Live Dashboard (Tableau Public)

Access the interactive dashboards here:
https://public.tableau.com/app/profile/atharva.sharma1638/viz/CustomerChurn_17769513030030/Retention

---

## Dashboard Overview

### 1. Retention Dashboard

![Retention Dashboard](screenshots/Dashboard-1%20(Retension).png)

Focus:
- Customer retention and repeat behavior
- Distribution of one-time vs repeat customers
- Impact of reviews and payment methods on repeat purchases

Key Insights:
- ~97% of customers are one-time buyers
- Repeat rate is extremely low (~2.8%)
- Customer experience (reviews) influences repeat behavior

### 2. Behavior Dashboard

![Behavior Dashboard](screenshots/Dashboard-2%20(Behavior).png)

Focus:
- Customer spending patterns
- Order frequency vs spend relationship
- Distribution of customer value

Key Insights:
- Spending distribution is highly skewed
- Majority of customers fall into a low-spend segment
- Higher spend correlates with better retention

### 3. Churn Drivers Dashboard

![Churn Drivers Dashboard](screenshots/Dashboard-3%20(Churn%20Drivers).png)

Focus:
- Factors contributing to churn
- Customer segmentation by risk
- Payment and review-based churn behavior

Key Insights:
- Overall churn rate is very high (~97%)
- Low-value customers contribute most to churn
- Review score and delivery experience are key churn drivers

---

## Features

- Interactive navigation between dashboards
- Context-based filtering for each dashboard
- KPI-driven layout for quick insights
- Consistent design across all dashboards

---

## Data Source

Dashboards are built using:

- tableau_ready.csv (105,000 rows x 24 columns)
- Derived from the full ETL pipeline and statistical analysis

---

## Notes on Visualization Design

- Bar charts are primarily used due to highly skewed data distribution
- Log scale is applied where necessary for better visibility
- Pie charts and histograms were avoided due to poor interpretability in this dataset

---

## Folder Structure

```text
tableau/
├── screenshots/
│   ├── Dashboard-1 (Retension).png
│   ├── Dashboard-2 (Behavior).png
│   └── Dashboard-3 (Churn Drivers).png
└── README.md
```

---

## Summary

These dashboards translate complex churn analysis into a clear, interactive format, enabling:

- Quick identification of retention issues
- Understanding of customer behavior
- Data-driven decision-making for reducing churn

---

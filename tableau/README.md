# Tableau Dashboards - Customer Churn Analysis

This folder contains the final Tableau dashboards developed for the Olist Customer Churn Analysis project.

The dashboards present key insights on customer retention, behavior patterns, and churn drivers using an interactive and structured visual approach.

---

## Live Dashboard (Tableau Public)

Access the interactive dashboards here:
https://public.tableau.com/views/CustomerChurn_17769513030030/Retention (Navigation-enabled multi-dashboard view: Retention → Behavior → Churn Drivers)

---

## Dashboard Overview

### Storytelling Flow

The dashboards are designed to follow a clear analytical narrative:

1. **Retention (What is happening?)**
   - Establishes the core problem: extremely low repeat rate and high churn

2. **Behavior (Why is it happening?)**
   - Explores spending patterns and customer segments driving retention differences

3. **Churn Drivers (What is causing it?)**
   - Identifies operational and experience-based factors such as delivery delay, reviews, and payment type

This structured flow ensures that users move from high-level metrics to root-cause analysis in a logical progression.

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

- Interactive navigation (Retention → Behavior → Churn Drivers)
- Context-aware filters specific to each dashboard
- KPI-driven layout for rapid insight consumption
- Consistent color, typography, and layout across dashboards
- Logical storytelling structure guiding users from problem to root cause

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
- Logarithmic scale is selectively used for highly skewed distributions (e.g., Customer Lifecycle)
- Scatter/point plots are used where category comparison benefits from spatial separation (e.g., Payment vs Repeat)
- Visual hierarchy emphasizes KPIs first, followed by trend and breakdown analysis

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

These dashboards translate complex churn analysis into a structured, insight-driven narrative, enabling:

- Immediate identification of critical retention issues
- Clear understanding of customer behavior patterns
- Root-cause analysis of churn drivers
- Data-driven decision-making for improving customer retention

---

# Notebook Log — `04_statistical_analysis.ipynb`

**Project:** Olist Customer Churn Analysis  
**Capstone:** NST DVA Capstone 2 — Section D, Group 9  
**Role:** Statistical validation of EDA hypotheses — significance testing, effect sizes, multicollinearity, and logistic regression  
**Status:** Complete  
**Output:** No files written. All results printed inline and charts rendered inline.

---

## What This Notebook Does

Takes the EDA findings from NB03 and subjects them to rigorous statistical testing. Quantifies which features have a statistically significant AND practically meaningful relationship with churn. Concludes with a logistic regression model that produces odds ratios for each feature — the clearest quantification of churn drivers.

---

## Section-by-Section Log

### Section 1 — Setup & Data Loading
- Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats`, `statsmodels`, `pathlib`
- `scipy` and `statsmodels` installed inline via pip (first code cell)
- Dataset loaded from `../data/processed/olist_churn_master.csv`
- Churn distribution confirmed: ~92.9% churned, ~7.1% retained
- Two subsets created for all subsequent tests: `churned` (churn == 1) and `retained` (churn == 0)

### Section 2 — Helper Functions
Two reusable effect size functions defined:

- **`cohens_d(group1, group2)`** — pooled standard deviation approach; standardised mean difference between two groups. Interpretation: 0.2 = small, 0.5 = medium, 0.8 = large.
- **`cramers_v(contingency_table)`** — chi-square based; measures association strength between categorical variable and churn. Ranges 0–1.

> Key note documented in notebook: with 100K+ records, almost any difference will reach p < 0.05. Effect size is the real measure of practical importance throughout this notebook.

---

## Section 3 — Continuous Variables: T-tests, Mann-Whitney U & Effect Sizes

For each continuous variable: Welch's T-test (unequal variance), Mann-Whitney U (non-parametric), Cohen's d (effect size).

### 3.1 Delivery Delay vs Churn
- **H₀:** No significant difference in delivery delay between churned and retained  
- **H₁:** Churned customers experience higher average delivery delays  
- Result: p < 0.05 on both T-test and Mann-Whitney → **H₀ rejected**
- Cohen's d: small-to-medium effect
- Visualisation: side-by-side boxplot + KDE density curves by churn group
- **Finding:** Delivery delay is statistically and practically significant — churned customers experienced measurably higher delays

### 3.2 Review Score vs Churn
- **H₀:** No significant difference in review score between churned and retained  
- **H₁:** Retained customers give higher review scores  
- Result: p < 0.05 → **H₀ rejected**
- Cohen's d: small effect (scores differ but distributions overlap heavily)
- Visualisation: grouped % bar chart + KDE by churn group
- **Finding:** Retained customers gave marginally higher scores; low scores (1–2) are over-represented in churned group

### 3.3 Price vs Churn
- **H₀:** No significant difference in order price between churned and retained  
- Result: p < 0.05 → **H₀ rejected** (large sample drives significance)
- Cohen's d: very small — practically negligible difference
- **Finding:** Price is statistically significant but effect size is near zero; price alone does not predict churn

### 3.4 Freight Value vs Churn
- **H₀:** No significant difference in freight cost between churned and retained  
- Result: p < 0.05 → **H₀ rejected**
- Cohen's d: very small
- **Finding:** Freight cost shows minimal practical difference between groups

### 3.5 Payment Installments vs Churn
- **H₀:** No significant difference in installment count between churned and retained  
- Result: p < 0.05 → **H₀ rejected**
- Cohen's d: very small
- **Finding:** Marginal difference; retained customers used slightly more installments on average (multi-order behaviour)

### 3.6 Continuous Variables Summary Table
All 5 variables printed in a single summary table with columns: Feature, Mean (Churned), Mean (Retained), T-test p-value, Mann-Whitney p-value, Cohen's d, Effect magnitude, Significant?

| Feature | Effect Size | Practically Meaningful |
|---|---|---|
| Delivery Delay | Small-Medium | Yes |
| Review Score | Small | Marginal |
| Price | Negligible | No |
| Freight Value | Negligible | No |
| Payment Installments | Negligible | No |

---

## Section 4 — Categorical Variables: Chi-square & Cramér's V

### 4.1 Customer State vs Churn
- **H₀:** Churn is independent of customer state  
- Chi-square result: p < 0.05 → **H₀ rejected**
- Cramér's V: weak association (V < 0.1)
- Bar chart: churn rate per state, coloured above/below median
- **Finding:** Statistically significant variation across states but weak practical association; geography alone is not a strong churn predictor

### 4.2 Payment Type vs Churn
- **H₀:** Churn is independent of payment type  
- Chi-square result: p < 0.05 → **H₀ rejected**
- Cramér's V: weak association
- Visualisation: churn rate bar + stacked proportion bar by payment type
- **Finding:** Boleto (bank slip) customers show slightly higher churn than credit card; effect is weak

### 4.3 Product Category vs Churn
- Analysis restricted to top 15 categories by volume for interpretability
- Chi-square result: p < 0.05 → **H₀ rejected**
- Cramér's V: weak association
- Horizontal bar chart: churn rate per category, coloured above/below mean
- **Finding:** Some category-level variation in churn rates; no single category dominates

### 4.4 Categorical Summary Table
All 3 variables printed with Chi-square statistic, degrees of freedom, p-value, Cramér's V, and association strength label.

---

## Section 5 — Multicollinearity Check (VIF)

Features tested: `price`, `freight_value`, `payment_installments`, `review_score`, `delivery_delay_days`, `payment_value`

VIF results:
- `price` and `freight_value` — moderate VIF (expected — both feed into `order_revenue`)
- `payment_value` — higher VIF due to correlation with price and freight
- All others — VIF ≤ 5, acceptable
- **Decision:** `payment_value` and `order_revenue` excluded from logistic regression to avoid multicollinearity. Remaining features retained.

Visualisation: horizontal bar chart with VIF = 5 threshold line marked in red.

---

## Section 6 — Correlation Analysis

Numeric columns: `price`, `freight_value`, `order_revenue`, `payment_installments`, `payment_value`, `review_score`, `delivery_delay_days`, `churn`

Two charts:
1. **Full lower-triangle correlation heatmap** (coolwarm palette, annotated)
2. **Churn-only correlation bar chart** — isolates each feature's correlation with `churn`

Key correlations with `churn`:
- `delivery_delay_days`: highest positive correlation with churn
- `review_score`: negative correlation with churn (higher score → lower churn)
- `price`, `freight_value`, `payment_installments`: near-zero correlation

---

## Section 7 — Logistic Regression: Feature Importance & Odds Ratios

**Features used** (post-VIF check): `price`, `freight_value`, `payment_installments`, `review_score`, `delivery_delay_days`  
`payment_value` and `order_revenue` excluded due to multicollinearity.

- `statsmodels.Logit` used with `sm.add_constant(X)`
- Full model summary printed (coefficients, standard errors, z-scores, p-values, pseudo R²)

**Odds Ratios table** (exp(coefficient)):

| Feature | Direction | Significant |
|---|---|---|
| delivery_delay_days | ↑ Increases churn (OR > 1) | Yes |
| review_score | ↓ Decreases churn (OR < 1) | Yes |
| freight_value | ↑ Slight increase | Yes |
| price | Marginal | Yes (large N) |
| payment_installments | ↓ Slight decrease | Yes |

Visualisation: horizontal bar chart of odds ratios with 95% CI error bars, OR = 1 reference line, red = increases churn / green = decreases churn.

---

## Section 8 — Summary of Findings

Full printed summary covering:
- All continuous variable results with effect sizes
- All categorical variable results with Cramér's V
- Logistic regression odds ratios ranked by magnitude

**Key conclusions:**
1. **Delivery delay** is the strongest quantifiable churn driver — statistically significant with the largest effect size and highest positive odds ratio
2. **Review score** is the strongest protective factor — negative correlation and OR < 1 confirm that satisfied customers are less likely to churn
3. **Price, freight, and installments** are statistically significant at this sample size but have negligible practical effect sizes — not meaningful churn predictors on their own
4. **Geographic and category effects** are real but weak — Cramér's V confirms limited practical value for targeting
5. **High baseline churn (~92.9%)** is a structural Olist characteristic — the analytical focus should be on the margin between churned and retained, not the absolute rate

---

## Libraries Used
`pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy.stats` (ttest_ind, mannwhitneyu, chi2_contingency), `statsmodels` (Logit, VIF)

# Notebook Log — 06_tableau_dashboard_design.ipynb

Project: Olist Customer Churn Analysis  
Capstone: NST DVA Capstone 2 — Section D, Group 9  
Role: Visualization & Insight Delivery — Tableau Dashboard Design  
Status: Complete  
Primary Input: tableau_ready.csv (105,000 × 24)  
Output: 3 Interactive Dashboards (Tableau Public)

---

## What This Stage Does

Transforms the fully processed and feature-engineered dataset into interactive analytical dashboards that communicate:

- Customer retention patterns  
- Customer spending behavior  
- Key churn drivers  

This stage operationalizes insights derived from ETL and statistical validation into a decision-support interface.

---

## Upstream Dependency & Data Lineage

This stage directly builds on:

-  — Raw audit → data integrity, schema correctness  
-  — Cleaning + churn label + feature engineering  
-  — Tableau-ready dataset + KPI structures  
-  — Statistical validation of churn drivers  

### Key Dependency Alignment

| Stage | Output Used in Tableau |
|------|----------------------|
| NB02 | churn, delivery_delay_days, order_revenue |
| NB05 | review_bucket, delivery_bucket, KPIs |
| NB04 | Identified strongest drivers → guided visual focus |

---

## Tableau Deployment

Dashboard published at:  
https://public.tableau.com/views/CustomerChurn_17769513030030/Retention

---

## Data Model Used in Tableau

Single primary data source:

- tableau_ready.csv (denormalized, analysis-ready)

### Key Fields Used

Target Variable
- churn (customer-level derived)

Behavior Metrics
- order_revenue
- order_count
- avg_spend
- payment_type

Experience Metrics
- review_score
- review_bucket
- delivery_delay_days
- delivery_bucket

Segmentation
- order_count_bucket
- spend_segment

---

## Dashboard Architecture

Three dashboards designed as a modular analytical flow:

1. Retention → What is happening
2. Behavior → Why customers behave this way
3. Churn Drivers → What is causing churn

### Design Principle
Each dashboard answers a distinct analytical question while maintaining visual consistency.

### Storytelling Flow (Final Design)

The dashboards are intentionally structured as a left-to-right and top-to-bottom analytical narrative:

1. **Retention (Entry Point)**  
   Establishes the baseline problem — extremely high churn and low repeat rate.  
   Focus: “What is happening?”

2. **Behavior (Diagnostic Layer)**  
   Explains customer value distribution and spending behavior.  
   Focus: “Who are these customers and how do they behave?”

3. **Churn Drivers (Causal Layer)**  
   Identifies operational and experiential factors driving churn.  
   Focus: “Why is churn happening?”

This progression ensures that users move from observation → segmentation → causation without cognitive overload.

---

## Layout Standardization

### Header
- Fixed title across all dashboards
- Dynamic subtitle per context

### KPI Row
- Exactly 3 KPIs per dashboard
- Large font, minimal clutter
- Focus on decision-critical metrics only

### Right Panel
- Navigation (top)
- Filters (bottom)

---

## Navigation System (Dashboard Actions)

### Implementation
- Text-based buttons
- Dashboard → Actions → Go to Sheet

### Behavior
- Click-based navigation
- Active tab highlighted

### Rationale
- Avoids dropdown navigation complexity
- Improves storytelling flow

---

## Filter Design Strategy

Filters are contextual, not global:

| Dashboard | Filters | Purpose |
|----------|--------|--------|
| Retention | Order Count, Review Bucket | Retention segmentation |
| Behavior | Spend Segment, Order Count | Spending patterns |
| Churn Drivers | Payment, Spend, Review | Root cause analysis |

### Key Decision
Avoided global filters to:
- Prevent irrelevant slicing
- Maintain dashboard clarity

---

## Calculated Fields (Tableau Layer)

Derived on top of ETL outputs:

### Core KPIs
- Churn Rate = AVG([Customer Churn Flag])
- Repeat Rate = 1 - [Churn Rate]

### Customer Metrics
- Avg Orders per Customer  
- Avg Spend per Customer  
- Total Revenue  

### Segmentation Logic
- Order Count Bucket  
- Spend Segment  

### Risk Indicators
- High Risk Customer %  
- High Value Customer %  

### Important Constraint
All calculations respect:
- Customer-level churn definition (from NB02)
- Avoid row duplication bias

---

## Dashboard 1 — Retention

### Purpose
Understand baseline customer behavior and retention structure

### KPIs
- Repeat Rate (~2.8%)
- One-time Customers (~97%)
- Total Revenue

### Charts
1. Customer Lifecycle Distribution (log scale applied)  
2. Review vs Repeat Rate (sorted descending)  
3. Payment vs Repeat Rate (dot plot for compact comparison)  

### Key Insights
- Customer base is overwhelmingly one-time buyers (~97%)  
- Retention sharply increases with order frequency, but volume remains negligible  
- Customers with no reviews show the highest repeat rate (possible survivorship bias)  
- Payment method differences exist but are not dominant drivers  

### Link to Statistics
- Review score → statistically significant (NB04)
- Effect size small but direction consistent

---

## Dashboard 2 — Behavior

### Purpose
Analyze how customers spend and interact

### KPIs
- Avg Spend  
- Avg Orders  
- High Value %

### Charts
1. Average Spend vs Order Count (primary trend view)  
2. Spend Distribution (log scale applied)  
3. Spend vs Repeat Rate (segmented comparison)  

### Key Insights
- Customer spending follows a strong long-tail distribution (majority low spenders)  
- Repeat likelihood increases significantly with higher spend segments  
- Average spend peaks around mid-frequency customers (4 orders), then slightly declines  
- High-value customers are extremely rare but disproportionately important  

### Link to Statistics
- Price → statistically significant but negligible effect  
- Confirms behavior segmentation is more meaningful than raw price

---

## Dashboard 3 — Churn Drivers

### Purpose
Identify what drives churn

### KPIs
- Overall Churn Rate  
- High Risk %  
- Avg Delivery Delay  

### Charts
1. Delivery Delay Trend Over Time (monthly granularity fixed)  
2. Churn by Review Score  
3. Churn Contribution by Spend Segment  
4. Churn Rate by Payment Type  

### Key Insights
- Delivery delays show temporal fluctuation and align with churn risk periods  
- Low-value customers contribute ~99% of total churn volume  
- Review scores maintain a consistent directional relationship with churn  
- Payment type impact is visible but comparatively weak  

### Link to Statistics
- Delivery delay → strongest driver (NB04)  
- Review score → strongest negative predictor  
- Payment type → weak association (Cramér’s V low)

---

## Visualization Design Decisions

### Data Constraint
- Extremely skewed distributions (e.g., 97% vs <3%)

### Design Responses

| Decision | Reason |
|--------|--------|
| Bar charts dominant | Best for extreme comparisons |
| Log scale used | Handles magnitude imbalance |
| Line chart used selectively | Only for trend clarity |
| Pie charts avoided | Misleading under skew |
| Histograms avoided | Space + low interpretability |
| Consistent layout across dashboards | Improves usability and reduces cognitive load |

---

## Challenges & Resolutions

### 1. Extreme Skew
- Issue: Small segments invisible
- Fix: Log scale + horizontal bars

### 2. Chart Variety Limitation
- Issue: Many charts default to bars
- Reason: Data structure unsuitable for alternatives
- Resolution: Prioritized clarity over variety

### 3. Space Constraints
- Issue: Filters + navigation overcrowding
- Fix: Right-side panel design

### 4. High Churn Baseline
- Issue: Hard to interpret differences
- Fix: Focus on relative comparisons

### 5. Storytelling Clarity
- Issue: Dashboards initially felt like independent views  
- Fix: Reordered layouts and standardized chart hierarchy  
- Outcome: Clear narrative flow from retention → behavior → drivers  

---

## Traceability: Data → Insight

| Feature | Chart | Insight |
|--------|------|--------|
| delivery_delay_days | KPI + churn view | Strong churn driver |
| review_score | Review vs churn | Experience impacts retention |
| spend_segment | Spend vs repeat | High value = retention |
| payment_type | Payment vs churn | Weak behavioral influence |

---

## Final Output

- 3 dashboards  
- Fully interactive navigation  
- Clean KPI presentation  
- Context-aware filtering  
- Public deployment completed  

---

## Key Learnings

- Statistical validation should guide visualization  
- Data distribution dictates chart selection  
- Simplicity > variety in dashboard design  
- Log scaling is critical for skewed data  
- Strong storytelling requires structured dashboard flow  
- Dashboard sequencing is as important as chart design  
- Narrative flow significantly improves interpretability  
- Minimalism with consistency outperforms complex visuals  

---

## Final Status

| Component | Status |
|----------|--------|
| Data Integration | Complete |
| Dashboard Design | Complete |
| Navigation | Functional |
| Filters | Optimized |
| Visual Accuracy | Validated |
| Deployment | Completed |

---
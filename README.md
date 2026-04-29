<p align="center">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=0:06b6d4,50:0ea5e9,100:7c3aed&height=160&section=header&text=Customer%20Churn%20Analysis&fontSize=40&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Olist%20E-commerce%20|%20Churn%20KPI%20&descAlignY=58" alt="Customer Churn Analysis banner" width="100%">
</p>

Predicting and analysing customer churn from Olist marketplace data — extraction, cleaning, EDA, KPI generation, and Tableau-ready outputs.

<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white">
    <img alt="Pandas" src="https://img.shields.io/badge/Data-Pandas-%230192d6?logo=pandas&logoColor=white">
    <img alt="Tableau" src="https://img.shields.io/badge/Tableau-Dashboard-E97627?logo=tableau&logoColor=white">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-green">
</p>

## ✨ Overview

- Goal: analyse Olist orders/customers to derive churn-related KPIs and build reproducible artifacts for reporting and dashboards.
- Pipeline: extraction → cleaning → EDA → statistical analysis → final load/prep for Tableau.

## 🧰 Tech Stack

- Languages & libs: Python, Pandas, NumPy, Scikit-learn
- Notebooks: Jupyter / JupyterLab
- Reporting: Tableau (prepared `tableau_ready.csv`)
- Orchestration: lightweight ETL in `scripts/etl_pipeline.py`

## 📂 Key files

- `requirements.txt` — Python dependencies
- `scripts/etl_pipeline.py` — ETL that transforms `data/raw/` → `data/processed/`
- `notebooks/` — stepwise notebooks `01_extraction.ipynb` → `05_final_load_prep.ipynb`
- `docs/data_dictionary.md` — field definitions and notes
- `data/processed/` — outputs including `customers_kpi.csv`, `monthly_kpi.csv`, `state_kpi.csv`, `tableau_ready.csv`
- `logs/` — pipeline logs for reproducibility and audit

## 📈 High-level workflow

```mermaid
flowchart TD
    RAW["Raw CSVs (data/raw)"] --> ETL["ETL: scripts/etl_pipeline.py"]
    ETL --> PROCESSED["data/processed — cleaned, KPIs, tableau_ready.csv"]
    PROCESSED --> NOTEBOOKS["notebooks: analysis & visualisation"]
    PROCESSED --> TABLEAU["Tableau Dashboard (Live)"]
    TABLEAU --> REPORTS["reports/ and docs/"]
    NOTEBOOKS --> REPORTS["reports/ and docs/"]
```

**Live Tableau Dashboard:** [View dashboard](https://public.tableau.com/views/CustomerChurn_17769513030030/Retention)

## 🚀 Quick start

1. Create and activate a virtual environment (Python 3.10+):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the ETL to regenerate processed datasets (example with input/output):

```bash
python scripts/etl_pipeline.py --input data/raw/olist_orders_dataset.csv \
    --output data/processed/olist_orders_cleaned.csv
```

4. Explore analysis and visualizations in the notebooks:

```bash
jupyter lab notebooks/
```

## 🔁 Reproducibility & Notes

- Processed artifacts are written to `data/processed/` and are used for reporting and Tableau dashboards.
- The `logs/` folder documents each pipeline stage (extraction, cleaning, EDA, stats, final prep).

---



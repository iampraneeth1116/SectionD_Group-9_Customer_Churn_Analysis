"""ETL pipeline for NST DVA Capstone 2 — Olist Customer Churn Analysis.

This script contains cleaning and feature engineering functions used in
notebooks/02_cleaning.ipynb. Import these functions directly from the notebook
to keep the pipeline reproducible and auditable.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import numpy as np


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply safe default cleaning steps: normalize columns, drop duplicates, strip strings."""
    result = normalize_columns(df)
    result = result.drop_duplicates().reset_index(drop=True)

    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype("string").str.strip()

    return result


def cast_order_datetimes(df_orders: pd.DataFrame) -> pd.DataFrame:
    """Cast all 5 timestamp columns in df_orders to datetime64.

    Uses errors='coerce' to convert unparseable values to NaT.
    """
    ts_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    result = df_orders.copy()
    for col in ts_cols:
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], errors="coerce")
    return result


def engineer_delivery_delay(df: pd.DataFrame) -> pd.DataFrame:
    """Add delivery_delay_days column.

    delivery_delay_days = (order_delivered_customer_date - order_estimated_delivery_date).dt.days
    Positive values = late delivery. Negative values = early delivery.
    """
    result = df.copy()
    result["delivery_delay_days"] = (
        result["order_delivered_customer_date"] - result["order_estimated_delivery_date"]
    ).dt.days
    return result


def engineer_order_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Add order_revenue column.

    order_revenue = price + freight_value
    Represents total value of one item line including shipping.
    """
    result = df.copy()
    result["order_revenue"] = result["price"] + result["freight_value"]
    return result


def engineer_churn_label(df: pd.DataFrame) -> pd.DataFrame:
    """Add churn column based on customer_unique_id order count.

    churn = 1 if customer placed exactly 1 order in the dataset (churned).
    churn = 0 if customer placed 2 or more orders (retained).

    Uses customer_unique_id — not customer_id — because a single real customer
    can have multiple customer_id values (one per order) in the Olist schema.
    """
    result = df.copy()
    order_counts = (
        result.groupby("customer_unique_id")["order_id"]
        .nunique()
        .reset_index()
        .rename(columns={"order_id": "order_count"})
    )
    order_counts["churn"] = (order_counts["order_count"] == 1).astype(int)
    result = result.merge(order_counts[["customer_unique_id", "churn"]], on="customer_unique_id", how="left")
    return result


def stratified_sample(df: pd.DataFrame, target_n: int = 105_000, random_state: int = 42) -> pd.DataFrame:
    """Reduce df to approximately target_n rows using stratified sampling on the churn column.

    Stratifying on churn preserves the original churn/retained distribution in the sample,
    preventing class imbalance introduced by random sampling.

    Returns the full df unchanged if len(df) <= target_n.
    """
    if len(df) <= target_n:
        return df.reset_index(drop=True)
    frac = target_n / len(df)
    return (
        df.groupby("churn", group_keys=False)
        .sample(frac=frac, random_state=random_state)
        .reset_index(drop=True)
    )


def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    """Read a raw CSV file and return a cleaned dataframe (template compatibility shim)."""
    df = pd.read_csv(input_path)
    return basic_clean(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write the cleaned dataframe to disk, creating the parent folder if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Capstone 2 Olist ETL pipeline.")
    parser.add_argument("--input",  required=True, type=Path, help="Path to raw CSV in data/raw/.")
    parser.add_argument("--output", required=True, type=Path, help="Path to output CSV in data/processed/.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f"Processed dataset saved to: {args.output}")
    print(f"Rows: {len(cleaned_df)} | Columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()

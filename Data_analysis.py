"""
Data_analysis.py
Performs descriptive analysis on clean_dataset.csv.

Run data_cleaning.py first, then:
  python Data_analysis.py
"""

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "clean_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("clean_dataset.csv not found. Run data_cleaning.py first.")

    df = pd.read_csv(INPUT_FILE)
    for col in ["Quantity_kg", "Wasted_kg", "Freshness_Percent",
                "Days_To_Expiry", "Temperature_C"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    report = []
    report.append("SMART FOOD SAVER - DATA ANALYSIS")
    report.append("=" * 40)
    report.append(f"Number of records: {len(df)}")
    report.append(f"Number of columns: {len(df.columns)}")
    report.append(f"Total quantity (kg): {df['Quantity_kg'].sum():.2f}")
    report.append(f"Total wasted quantity (kg): {df['Wasted_kg'].sum():.2f}")
    waste_pct = (df["Wasted_kg"].sum() / df["Quantity_kg"].sum() * 100
                 if df["Quantity_kg"].sum() else 0)
    report.append(f"Waste as percentage of quantity: {waste_pct:.2f}%")
    report.append(f"Average freshness (%): {df['Freshness_Percent'].mean():.2f}")
    report.append(f"Average days to expiry: {df['Days_To_Expiry'].mean():.2f}")

    report.append("\nRecords by status:")
    report.append(df["Status"].value_counts(dropna=False).to_string())

    report.append("\nRecords by food category:")
    report.append(df["Category"].value_counts(dropna=False).to_string())

    report.append("\nTotal wasted quantity by category (kg):")
    report.append(
        df.groupby("Category")["Wasted_kg"].sum()
          .sort_values(ascending=False).round(2).to_string()
    )

    report.append("\nAverage freshness by category (%):")
    report.append(
        df.groupby("Category")["Freshness_Percent"].mean()
          .round(2).to_string()
    )

    report.append("\nTop 10 food records by wasted quantity:")
    top_waste = df.nlargest(10, "Wasted_kg")[
        ["Food_ID", "Food_Name", "Category", "Quantity_kg", "Wasted_kg", "Status"]
    ]
    report.append(top_waste.to_string(index=False))

    report_text = "\n".join(report)
    output_file = OUTPUT_DIR / "analysis_report.txt"
    output_file.write_text(report_text, encoding="utf-8")

    # Export useful summary tables for the report and dashboard.
    df.groupby("Category").agg(
        Record_Count=("Food_ID", "count"),
        Total_Quantity_kg=("Quantity_kg", "sum"),
        Total_Wasted_kg=("Wasted_kg", "sum"),
        Average_Freshness_Percent=("Freshness_Percent", "mean")
    ).round(2).to_csv(OUTPUT_DIR / "category_summary.csv")

    df.groupby("Status").agg(
        Record_Count=("Food_ID", "count"),
        Total_Wasted_kg=("Wasted_kg", "sum")
    ).round(2).to_csv(OUTPUT_DIR / "status_summary.csv")

    print(report_text)
    print(f"\nAnalysis report saved to: {output_file}")

if __name__ == "__main__":
    main()

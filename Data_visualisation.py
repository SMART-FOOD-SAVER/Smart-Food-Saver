"""
Data_visualisation.py
Creates charts from clean_dataset.csv using Matplotlib and Seaborn.

Run data_cleaning.py first, then:
  python Data_visualisation.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "clean_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("clean_dataset.csv not found. Run data_cleaning.py first.")

    df = pd.read_csv(INPUT_FILE)
    for col in ["Quantity_kg", "Wasted_kg", "Freshness_Percent", "Days_To_Expiry"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 1. Number of records in each food category.
    df["Category"].value_counts().plot(kind="bar")
    plt.title("Food Records by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=35, ha="right")
    save_chart("food_category_count.png")

    # 2. Total wasted quantity by category.
    df.groupby("Category")["Wasted_kg"].sum().sort_values(
        ascending=False
    ).plot(kind="bar")
    plt.title("Total Food Waste by Category")
    plt.xlabel("Category")
    plt.ylabel("Wasted Quantity (kg)")
    plt.xticks(rotation=35, ha="right")
    save_chart("waste_by_category.png")

    # 3. Food status distribution.
    df["Status"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Food Status Distribution")
    plt.ylabel("")
    save_chart("food_status_distribution.png")

    # 4. Freshness percentage distribution.
    df["Freshness_Percent"].dropna().plot(kind="hist", bins=15, edgecolor="black")
    plt.title("Distribution of Food Freshness")
    plt.xlabel("Freshness (%)")
    plt.ylabel("Number of Records")
    save_chart("freshness_distribution.png")

    # 5. Days to expiry against freshness.
    plt.scatter(df["Days_To_Expiry"], df["Freshness_Percent"], alpha=0.6)
    plt.title("Days to Expiry vs Freshness")
    plt.xlabel("Days to Expiry")
    plt.ylabel("Freshness (%)")
    save_chart("expiry_vs_freshness.png")

    print("Charts created in the outputs folder:")
    for filename in [
        "food_category_count.png", "waste_by_category.png",
        "food_status_distribution.png", "freshness_distribution.png",
        "expiry_vs_freshness.png"
    ]:
        print("-", OUTPUT_DIR / filename)

if __name__ == "__main__":
    main()

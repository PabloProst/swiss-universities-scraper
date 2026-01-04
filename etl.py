import pandas as pd
from pathlib import Path

RAW_PATH = "data/raw/swiss_universities_basic.csv"
PROCESSED_PATH = "data/processed/swiss_universities_clean.csv"

def clean_enrollment(value):
    """Convert enrollment string like '10,686' to int"""
    if pd.isna(value):
        return None
    return int(value.replace(",", "").strip())

def clean_founded(value):
    """Convert founded string to int"""
    if pd.isna(value):
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None

def etl_process():
    # --- READ RAW CSV ---
    df = pd.read_csv(RAW_PATH)

    # Strip whitespace from string columns
    str_cols = ['University', 'Abbreviation', 'Location', 'Language', 'Type']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Clean Enrollment and Founded columns
    if 'Enrollment' in df.columns:
        df['Enrollment'] = df['Enrollment'].apply(clean_enrollment)
    if 'Founded' in df.columns:
        df['Founded'] = df['Founded'].apply(clean_founded)

    # Ensure processed folder exists
    Path("data/processed").mkdir(parents=True, exist_ok=True)

    # Save cleaned CSV
    df.to_csv(PROCESSED_PATH, index=False, encoding="utf-8")
    print("Processed CSV saved successfully!")
    print(df.head())

def main():
    etl_process()

if __name__ == "__main__":
    main()

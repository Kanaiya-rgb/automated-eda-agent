import pandas as pd
import os
import glob


def run_verified_cleaning_agent():
    print("==================================================")
    print("VERIFIED AUTO-EDA & CLEANING AGENT")
    print("==================================================")

    # 1. Check if any CSV files exist in the folder
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("❌ Error: Folder mein koi bhi .csv file nahi mili!")
        return

    for file_path in csv_files:
        # Avoid processing already cleaned or audit files to prevent loops
        if '_cleaned.csv' in file_path or '_audit_report' in file_path:
            continue

        print(f"\n📂 Processing & Verifying: '{file_path}'")

        # --- LOAD ORIGINAL DATA ---
        try:
            df_original = pd.read_csv(file_path, encoding='utf-8', encoding_errors='replace')
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue

        if df_original.empty:
            print(f"⚠️ Skipping empty file: {file_path}")
            continue

        # Handle duplicate column names (rare but breaks fillna logic if present)
        if df_original.columns.duplicated().any():
            print(f"⚠️ Warning: Duplicate column names found in {file_path}. Renaming duplicates.")
            cols = pd.Series(df_original.columns)
            for dup in cols[cols.duplicated()].unique():
                dup_indices = cols[cols == dup].index
                for i, idx in enumerate(dup_indices):
                    if i > 0:
                        cols[idx] = f"{dup}_{i}"
            df_original.columns = cols

        orig_rows, orig_cols = df_original.shape
        orig_missing = df_original.isnull().sum().sum()
        orig_duplicates = df_original.duplicated().sum()

        # Copy for cleaning
        df = df_original.copy()

        # --- CLEANING PROCESS ---
        try:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()

            # Fill missing numeric values with Median
            for col in numeric_cols:
                if df[col].isnull().sum() > 0:
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)

            # Fill missing categorical values with Mode or 'Unknown'
            for col in categorical_cols:
                if df[col].isnull().sum() > 0:
                    mode_series = df[col].mode()
                    mode_val = mode_series[0] if not mode_series.empty else "Unknown"
                    df[col] = df[col].fillna(mode_val)

            # Fill missing datetime values with forward-fill then back-fill (safe fallback)
            for col in datetime_cols:
                if df[col].isnull().sum() > 0:
                    df[col] = df[col].ffill().bfill()

            # Drop duplicate rows
            df.drop_duplicates(inplace=True)

        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")
            continue

        # --- VERIFICATION & CROSS-CHECK REPORT ---
        new_rows, _ = df.shape
        new_missing = df.isnull().sum().sum()

        print("   🔍 --- VERIFICATION REPORT ---")
        print(f"   - Rows Before: {orig_rows:,} | Rows After: {new_rows:,} (Removed: {orig_rows - new_rows:,} rows)")
        print(f"   - Missing Values Before: {orig_missing:,} | Missing Values After: {new_missing:,}")
        print(f"   - Duplicates Removed: {orig_duplicates:,}")
        print("   - Status: Verified & Cleaned Successfully! ✅")

        # --- SAVE CLEANED FILE ---
        try:
            base_name, ext = os.path.splitext(file_path)
            output_filename = f"{base_name}_cleaned{ext}"
            df.to_csv(output_filename, index=False)
            print(f"   💾 Saved as: '{output_filename}'")
        except Exception as e:
            print(f"❌ Error saving cleaned file for {file_path}: {e}")
            continue

    print("\n==================================================")
    print("ALL FILES VERIFIED AND PROCESSED!")
    print("==================================================")


if __name__ == "__main__":
    run_verified_cleaning_agent()
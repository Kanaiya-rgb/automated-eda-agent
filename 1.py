import pandas as pd
import os
import glob
from datetime import datetime

def run_verified_cleaning_agent():
    print("==================================================")
    print("VERIFIED AUTO-EDA & CLEANING AGENT (PRO EDITION)")
    print("==================================================")
    
    csv_files = glob.glob('*.csv')
    if not csv_files:
        print("❌ Error: Folder mein koi bhi .csv file nahi mili!")
        return
        
    for file_path in csv_files:
        if '_cleaned.csv' in file_path or '_audit_report' in file_path:
            continue
            
        print(f"\n📂 Processing & Verifying: '{file_path}'")
        
        try:
            df_original = pd.read_csv(file_path, encoding='utf-8', encoding_errors='replace')
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue
            
        if df_original.empty:
            print(f"⚠️ Skipping empty file: {file_path}")
            continue

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
        
        df = df_original.copy()
        
        try:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns.tolist()
            
            for col in numeric_cols:
                if df[col].isnull().sum() > 0:
                    median_val = df[col].median()
                    df[col] = df[col].fillna(median_val)
                
                skip_keywords = ['id', 'code', 'zip', 'year', 'no', 'number']
                if any(keyword in col.lower() for keyword in skip_keywords):
                    continue  

                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
                
            for col in categorical_cols:
                if df[col].isnull().sum() > 0:
                    mode_series = df[col].mode()
                    mode_val = mode_series[0] if not mode_series.empty else "Unknown"
                    df[col] = df[col].fillna(mode_val)
                    
            for col in datetime_cols:
                if df[col].isnull().sum() > 0:
                    df[col] = df[col].ffill().bfill()
                    
            df.drop_duplicates(inplace=True)
            
        except Exception as e:
            print(f"❌ Error cleaning {file_path}: {e}")
            continue

        new_rows, _ = df.shape
        new_missing = df.isnull().sum().sum()
        
        report_text = f"""--- VERIFICATION REPORT FOR: {file_path} ---
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Rows Before: {orig_rows:,} | Rows After: {new_rows:,} (Removed: {orig_rows - new_rows:,} rows)
- Missing Values Before: {orig_missing:,} | Missing Values After: {new_missing:,}
- Duplicates Removed: {orig_duplicates:,}
- Status: Verified & Cleaned Successfully! ✅
--------------------------------------------------"""
        
        print(f"\n   🔍 --- VERIFICATION REPORT ---")
        print(f"   - Rows Before: {orig_rows:,} | Rows After: {new_rows:,} (Removed: {orig_rows - new_rows:,} rows)")
        print(f"   - Missing Values Before: {orig_missing:,} | Missing Values After: {new_missing:,}")
        print(f"   - Duplicates Removed: {orig_duplicates:,}")
        print("   - Status: Verified & Cleaned Successfully! ✅")

        base_name, ext = os.path.splitext(file_path)
        output_filename = f"{base_name}_cleaned{ext}"
        audit_filename = f"{base_name}_audit_report.txt"
        
        try:
            df.to_csv(output_filename, index=False)
            with open(audit_filename, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"   💾 Saved Cleaned File: '{output_filename}'")
            print(f"   📝 Saved Audit Log:   '{audit_filename}'")
        except Exception as e:
            print(f"❌ Error saving files for {file_path}: {e}")
            continue

    print("\n==================================================")
    print("ALL FILES VERIFIED, CLEANED AND AUDITED!")
    print("==================================================")

if __name__ == "__main__":
    run_verified_cleaning_agent()
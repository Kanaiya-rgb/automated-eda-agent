<div align="center">

# 🧹 Automated EDA & Data Cleaning Agent

**Point it at a folder full of messy CSVs. It hands back clean ones, plus a report proving what it actually changed.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-Data%20Cleaning-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)

<img src="https://www.python.org/static/community_logos/python-logo-generic.svg" width="300" alt="Python logo">

</div>

---

## 📋 Table of Contents

- [Why this exists](#-why-this-exists)
- [Stack](#-stack)
- [What it does](#-what-it-does)
- [Project layout](#-project-layout)
- [Running it](#-running-it)
- [What the output looks like](#-what-the-output-looks-like)
- [How it works, roughly](#-how-it-works-roughly)
- [Ideas for later](#-ideas-for-later)
- [License](#-license)
- [Contributing](#-contributing)

---

## 🤔 Why this exists

Cleaning CSVs by hand gets old fast. Open a file, count the nulls, decide how to fill them, chase down outliers, drop the duplicates, save it, repeat for every file in the folder. Do that ten times in a row and you start skipping steps without noticing.

This script handles the repetitive part. It finds every CSV sitting in the working directory, cleans each one based on what's actually in each column, and writes out a before/after report so you're not just trusting it blindly — you can open the report and check its work.

---

## 🛠️ Stack

| | |
|---|---|
| **Language** | Python 3.x |
| **Core library** | `pandas` — does the actual data work |
| **Standard library** | `os`, `glob`, `datetime` — file discovery, paths, timestamps |

No extra dependencies beyond pandas.

---

## ⚙️ What it does

**Finds your files.** Scans the current folder for `.csv` files — no need to list filenames anywhere in the script.

**Handles duplicate column names.** If a CSV somehow has two columns called the same thing, the second one gets renamed (`col`, `col_1`, `col_2`...) instead of quietly breaking downstream.

**Cleans by column type:**
- Numeric columns: missing values filled with the median (mean gets dragged around by outliers, median doesn't).
- Text/categorical columns: missing values filled with the most common value, or `"Unknown"` if there isn't one.
- Date columns: gaps filled by carrying the nearest known value forward, then backward for anything left at the start.

**Clips outliers on numeric columns**, using the standard IQR method (anything outside Q1 − 1.5×IQR to Q3 + 1.5×IQR gets pulled in to the boundary). Columns that look like IDs, codes, ZIPs, years, or other reference numbers are skipped, since "outlier" doesn't really mean anything for a ZIP code.

**Drops duplicate rows** — the plain, fully-duplicated kind.

**Writes a report for every file**, not just a printout. Rows before/after, missing values before/after, duplicates removed, timestamp — saved as its own `.txt` file so you have a record even after the terminal's scrolled away.

**Doesn't crash on one bad file.** Empty, corrupted, or unreadable CSVs get logged and skipped, and the script moves on to the next one instead of dying halfway through the folder.

**Won't clean its own output.** Anything already ending in `_cleaned.csv` or `_audit_report` gets skipped, so re-running the script doesn't reprocess what it already cleaned.

---

## 📁 Project layout

```
.
├── verified_cleaning_agent.py   # the script
├── your_data_1.csv              # your raw CSVs go here
├── your_data_2.csv
└── README.md
```

After a run:

```
├── your_data_1.csv
├── your_data_1_cleaned.csv
├── your_data_1_audit_report.txt
├── your_data_2.csv
├── your_data_2_cleaned.csv
├── your_data_2_audit_report.txt
```

---

## 🚀 Running it

Clone the repo:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

Install pandas if you don't have it already:

```bash
pip install pandas
```

Drop your CSV files into the same folder as the script, then run:

```bash
python verified_cleaning_agent.py
```

Cleaned files show up as `*_cleaned.csv`, and each one gets a matching `*_audit_report.txt` next to it.

---

## 📊 What the output looks like

```
==================================================
VERIFIED AUTO-EDA & CLEANING AGENT (PRO EDITION)
==================================================

📂 Processing & Verifying: 'sales_data.csv'

   🔍 --- VERIFICATION REPORT ---
   - Rows Before: 5,000 | Rows After: 4,982 (Removed: 18 rows)
   - Missing Values Before: 142 | Missing Values After: 0
   - Duplicates Removed: 18
   - Status: Verified & Cleaned Successfully! ✅
   💾 Saved Cleaned File: 'sales_data_cleaned.csv'
   📝 Saved Audit Log:   'sales_data_audit_report.txt'

==================================================
ALL FILES VERIFIED, CLEANED AND AUDITED!
==================================================
```

And the matching `sales_data_audit_report.txt`:

```
--- VERIFICATION REPORT FOR: sales_data.csv ---
Timestamp: 2026-08-18 11:42:07
- Rows Before: 5,000 | Rows After: 4,982 (Removed: 18 rows)
- Missing Values Before: 142 | Missing Values After: 0
- Duplicates Removed: 18
- Status: Verified & Cleaned Successfully! ✅
--------------------------------------------------
```

---

## 🧠 How it works, roughly

`glob` finds every `.csv` in the folder, skipping anything already cleaned or already an audit report. Each file gets loaded, checked for basic sanity — is it empty, does it have duplicate columns — then cleaned column by column depending on its dtype: numeric columns get median-filled and IQR-clipped, categorical columns get mode-filled, date columns get forward/backward filled. Duplicate rows get dropped. The before/after counts get compared, printed to the terminal, and written to disk as both the cleaned CSV and its audit report.

Basically the checklist you'd run through by hand, just automated and consistent every time.

---

## 🔮 Ideas for later

A few things worth adding if this grows:

- Support for `.xlsx`, `.tsv`, `.json` — CSV isn't the only format people have lying around
- A CLI flag or two, so you can pick the imputation strategy or output folder without editing the script
- Z-score as an alternative to IQR for outlier detection, since IQR isn't always the right call for skewed distributions
- Proper logging instead of print statements, if this ever runs unattended
- A summary CSV that rolls up every file's stats into one table, for folders with a lot of files in them

It works fine as-is — these are just the next things worth reaching for.

---

## 📄 License

MIT. Use it however you want.

---

## 🤝 Contributing

Found a bug or have an idea? Open an issue or send a PR. Turnaround isn't fast, but I do read them.
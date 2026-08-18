# Automated EDA & Data Cleaning Agent

A Python script that takes a folder full of messy CSVs and hands you back clean ones, with a printout showing exactly what changed.

---

## Why this exists

Cleaning CSVs by hand gets old fast. You open a file, count the nulls, decide how to fill them, drop the duplicates, save it, and repeat for every dataset in the folder. Do that ten times and you start making mistakes or skipping steps.

This script does the repetitive part: it finds every CSV in the working directory, cleans each one based on what type of data is in each column, and prints a before/after comparison so you can actually see what it did rather than trusting it blindly.

---

## Stack

- Python 3.x
- `pandas` for the actual data work
- `os` and `glob` from the standard library for file handling

That's it — no extra dependencies to install beyond pandas.

---

## What it does

**Finds your files.** Scans the current folder for `.csv` files. No need to list filenames anywhere in the script.

**Cleans by column type:**
- Numeric columns get missing values filled with the median (mean gets thrown off by outliers, median doesn't).
- Text/categorical columns get filled with the most common value, or `'Unknown'` if there isn't one.
- Date columns get filled by carrying the nearest known value forward, then backward for any gaps left at the start.

**Handles duplicate column names.** If your CSV somehow has two columns named the same thing, the script renames the second one instead of silently breaking.

**Drops duplicate rows** — the plain, fully-duplicated kind.

**Shows its work.** For every file, it prints row counts before and after, how many missing values got filled, and how many duplicate rows got removed. You don't have to take the cleaning on faith.

**Doesn't crash on one bad file.** If a CSV is empty, corrupted, or won't parse, the script logs the error and moves on to the next one instead of stopping the whole run.

**Won't clean its own output.** Files ending in `_cleaned.csv` are skipped, so you can re-run the script without it endlessly reprocessing what it already cleaned.

---

## Project layout

```
.
├── verified_cleaning_agent.py   # the script
├── your_data_1.csv              # your raw CSVs go here
├── your_data_2.csv
└── README.md
```

After a run, you'll see the cleaned versions sitting next to the originals:

```
├── your_data_1.csv
├── your_data_1_cleaned.csv
├── your_data_2.csv
├── your_data_2_cleaned.csv
```

---

## Running it

Clone the repo:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

Install pandas if you don't already have it:

```bash
pip install pandas
```

Drop your CSV files into the same folder as the script, then run:

```bash
python verified_cleaning_agent.py
```

That's it. Cleaned files show up as `*_cleaned.csv`, and you'll get a report for each one printed to your terminal.

---

## What the output looks like

```
==================================================
VERIFIED AUTO-EDA & CLEANING AGENT
==================================================

📂 Processing & Verifying: 'sales_data.csv'
   🔍 --- VERIFICATION REPORT ---
   - Rows Before: 5,000 | Rows After: 4,982 (Removed: 18 rows)
   - Missing Values Before: 142 | Missing Values After: 0
   - Duplicates Removed: 18
   - Status: Verified & Cleaned Successfully! ✅
   💾 Saved as: 'sales_data_cleaned.csv'

==================================================
ALL FILES VERIFIED AND PROCESSED!
==================================================
```

---

## How it works, roughly

`glob` finds every `.csv` in the folder (skipping anything already cleaned). Each file gets loaded, checked for basic sanity — is it actually empty, does it have duplicate column names — then cleaned column by column depending on its data type. Duplicate rows get dropped. Then the row counts and missing-value counts from before and after get compared and printed, and the result is written out with a `_cleaned` suffix.

Nothing fancy — it's basically the checklist you'd run through manually, just automated and consistent.

---

## Ideas for later

A few things I'd add if I kept working on this:

- Write the audit report to a file too, not just the terminal — useful if you're processing a lot of files and want a record
- Outlier detection (IQR or Z-score) instead of just filling gaps
- Support for `.xlsx`, `.tsv`, `.json` — CSV isn't the only thing people have lying around
- A CLI flag or two, so you can pick the imputation strategy or output folder without editing the script
- Proper logging instead of print statements, if this ever runs unattended

It works fine as-is. These are just the next things I'd reach for.

---

## License

MIT. Use it however you want.

---

## Contributing

If you find a bug or have an idea, open an issue or send a PR. I can't promise a fast turnaround but I do read them.

import pdfplumber
import pandas as pd
import os

# ============================
# FILE PATHS
# ============================

PDF_PATH = r"C:\Users\adity\Downloads\faym-agent\sql\dataset\Data Set.pdf"
CSV_PATH = r"C:\Users\adity\Downloads\faym-agent\sql\dataset\transactions.csv"

rows = []

print("Reading PDF...\n")

with pdfplumber.open(PDF_PATH) as pdf:

    print(f"Total Pages : {len(pdf.pages)}\n")

    for page_no, page in enumerate(pdf.pages, start=1):

        print(f"Processing Page {page_no}...")

        table = page.extract_table()

        if not table:
            continue

        # Skip header row
        for row in table[1:]:

            if row is None:
                continue

            # Remove whitespace
            row = [str(x).strip() if x is not None else "" for x in row]

            # Ignore incomplete rows
            if len(row) < 9:
                continue

            # Ignore blank rows
            if row[1] == "":
                continue

            rows.append([
                row[1],   # transaction_time
                row[2],   # user_id
                row[3],   # transaction_amt
                row[4],   # narration
                row[5],   # transaction_type
                row[6],   # txn_id
                row[7],   # month
                row[8],   # month2
            ])

print("\nRows Extracted :", len(rows))

columns = [
    "transaction_time",
    "user_id",
    "transaction_amt",
    "narration",
    "transaction_type",
    "txn_id",
    "month",
    "month2"
]

df = pd.DataFrame(rows, columns=columns)

# Remove duplicate header rows if present
df = df[df["transaction_time"] != "Transaction Time"]

# Remove completely empty rows
df = df.dropna(how="all")

# Save CSV
df.to_csv(CSV_PATH, index=False)

print("\nCSV Created Successfully!")
print("Location :", CSV_PATH)

print("\nFirst 10 Rows\n")
print(df.head(10))

print("\nDataset Shape :", df.shape)
from pathlib import Path
from PyPDF2 import PdfReader
import csv


pdf_path = Path("opay.pdf")
csv_path = Path("opay_transactions.csv")

if not pdf_path.exists():
    raise FileNotFoundError(f"{pdf_path} does not exist")


reader = PdfReader(pdf_path)


rows_to_write = []
total_credit = 0.0
total_debit = 0.0


for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()

    if not text:
        continue

    for row in text.split("\n"):
        parts = row.split()

   
        if len(parts) < 3:
            continue

        date = parts[0]

        amount = None
        amount_token = None

       
        for token in parts:
            if token.startswith(("+", "-")):
                try:
                    amount = float(token.replace(",", ""))
                    amount_token = token
                    break
                except ValueError:
                    continue

      
        if amount is None:
            continue

        
        if amount > 0:
            txn_type = "credit"
            total_credit += amount
        else:
            txn_type = "debit"
            total_debit += abs(amount)

       
        description_tokens = []
        for token in parts:
            if token == date or token == amount_token:
                continue

            cleaned = token.replace(",", "").replace(".", "")
            if cleaned.isdigit():
                continue

            description_tokens.append(token)

        description = " ".join(description_tokens)

        rows_to_write.append([
            date,
            description,
            abs(amount),
            txn_type
        ])


with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "description", "amount", "type"])
    writer.writerows(rows_to_write)


print("CSV file created:", csv_path)
print(f"Total Credit: ₦{total_credit:,.2f}")
print(f"Total Debit: ₦{total_debit:,.2f}")

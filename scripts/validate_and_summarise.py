#!/usr/bin/env python3
"""Rebuild aggregate evidence from the published first-page Auckland Transport sample.
Standard library only. No invented receipts, invoice spend, or supplier reliability scores.
"""
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import date
import csv, json, hashlib

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "auckland_transport_award_sample.csv"
OUT = ROOT / "evidence"
COLUMNS = [
    "source_row", "procurement_number", "category_code",
    "contract_description", "supplier_name", "award_value_nzd",
    "contract_created_date", "source_page", "source_url",
]
SOURCE_URL = "https://at.govt.nz/media/xy2jwzgu/auckland-transport-latest-awarded-contracts-july-2026.pdf"

def write_csv(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

with DATA.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    assert reader.fieldnames == COLUMNS, f"Unexpected schema: {reader.fieldnames}"
    raw = list(reader)
assert raw, "No rows found"

rows, errors = [], []
for ix, row in enumerate(raw, 1):
    if int(row["source_row"]) != ix:
        errors.append(f"Nonsequential source row at {ix}")
    for col in ("procurement_number", "category_code", "contract_description", "supplier_name", "source_url"):
        if not row[col].strip():
            errors.append(f"Missing {col} at {ix}")
    try:
        value = Decimal(row["award_value_nzd"])
    except InvalidOperation:
        errors.append(f"Invalid amount at {ix}")
        continue
    if value < 0:
        errors.append(f"Negative amount at {ix}")
    try:
        created = date.fromisoformat(row["contract_created_date"])
    except ValueError:
        errors.append(f"Invalid date at {ix}")
        continue
    if not (date(2025, 7, 1) <= created <= date(2026, 6, 30)):
        errors.append(f"Outside FY2026 at {ix}")
    if row["source_page"] != "1":
        errors.append(f"Unexpected source page at {ix}")
    if row["source_url"] != SOURCE_URL:
        errors.append(f"Unexpected source URL at {ix}")
    rows.append((row, value, created))
assert not errors, "\n".join(errors)

values = [v for _, v, _ in rows]
total = sum(values, Decimal(0))
supplier = defaultdict(lambda: [0, Decimal(0)])
category = defaultdict(lambda: [0, Decimal(0)])
daily = defaultdict(lambda: [0, Decimal(0)])
for row, value, created in rows:
    supplier[row["supplier_name"]][0] += 1
    supplier[row["supplier_name"]][1] += value
    category[row["category_code"]][0] += 1
    category[row["category_code"]][1] += value
    daily[created.isoformat()][0] += 1
    daily[created.isoformat()][1] += value
proc_ids = Counter(row["procurement_number"] for row, _, _ in rows)
repeats = {k: n for k, n in proc_ids.items() if n > 1}
top_supplier = sorted(supplier.items(), key=lambda kv: kv[1][1], reverse=True)
largest = max(rows, key=lambda row: row[1])
OUT.mkdir(exist_ok=True)

write_csv(
    OUT / "supplier_summary.csv",
    ["supplier_name", "award_entries", "disclosed_award_value_nzd", "share_of_sample_value_pct"],
    [[name, vals[0], str(vals[1]), round(float(vals[1] / total * 100), 4)] for name, vals in top_supplier],
)
write_csv(
    OUT / "category_summary.csv",
    ["category_code", "award_entries", "disclosed_award_value_nzd", "share_of_sample_value_pct"],
    [[name, vals[0], str(vals[1]), round(float(vals[1] / total * 100), 4)]
     for name, vals in sorted(category.items(), key=lambda kv: kv[1][1], reverse=True)],
)
write_csv(
    OUT / "daily_summary.csv",
    ["contract_created_date", "award_entries", "disclosed_award_value_nzd"],
    [[day, vals[0], str(vals[1])] for day, vals in sorted(daily.items())],
)

qa = {
    "source": "Auckland Transport FY2026 awarded contracts PDF, page 1",
    "record_scope": "First 52 disclosed entries; 2025-07-01 to 2025-07-10; NONREPRESENTATIVE PILOT SAMPLE",
    "source_url": SOURCE_URL,
    "sample_entries": len(rows),
    "total_disclosed_award_value_nzd": str(total),
    "unique_supplier_name_strings": len(supplier),
    "unique_procurement_numbers": len(proc_ids),
    "repeated_procurement_numbers": repeats,
    "largest_entry": {
        "source_row": int(largest[0]["source_row"]),
        "supplier": largest[0]["supplier_name"],
        "value_nzd": str(largest[1]),
        "pct_of_sample_value": round(float(largest[1] / total * 100), 4),
    },
    "top_supplier": {
        "supplier": top_supplier[0][0],
        "value_nzd": str(top_supplier[0][1][1]),
        "pct_of_sample_value": round(float(top_supplier[0][1][1] / total * 100), 4),
    },
    "qa_checks": {
        "schema_match": True,
        "source_row_sequence": True,
        "nonempty_required_fields": True,
        "valid_nonnegative_amounts": True,
        "valid_fy2026_dates": True,
        "pdf_source_and_page_consistent": True,
        "supplier_rollup_reconciles": sum((v[1] for v in supplier.values()), Decimal(0)) == total,
        "category_rollup_reconciles": sum((v[1] for v in category.values()), Decimal(0)) == total,
        "daily_rollup_reconciles": sum((v[1] for v in daily.values()), Decimal(0)) == total,
    },
    "file_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
    "important_caveat": "Award value is not actual spend, invoice payments, purchase order commitments or physical goods receipts. GST basis is not stated. Duplicated procurement IDs may represent distinct disclosed entries.",
}
(OUT / "validation_summary.json").write_text(
    json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("PASS:", len(rows), "entries, NZD", total, "supplier strings", len(supplier), "categories", len(category))
print("Duplicate procurement numbers:", repeats)
print("Largest entry share:", round(float(largest[1] / total * 100), 4), "%")

# Data model, grain and quality controls

## Grain and keys

Source: **one published row** of the Auckland Transport FY2026 award-contract PDF, first 52 entries on PDF page 1. The added source_row (1–52) is the pilot's row-level key. Procurement number is **not unique** and must not be used to eliminate entries.

| CSV field | Source label | Meaning and restrictions |
|---|---|---|
| source_row | Added sequence | Row position, not a source identifier |
| procurement_number | AT Procurement Number | Text; recurring values are possible |
| category_code | Contract Category | Code is retained without guessed meaning |
| contract_description | Contract Description | Public description; may be truncated |
| supplier_name | Successful Supplier | Unverified textual name, not legal-entity ID |
| award_value_nzd | Contract Award Value | Published amount, **not cash expenditure** |
| contract_created_date | Contract Created Date | Not a delivery, invoice or award-signature date |
| source_page | PDF page | 1-based page index |
| source_url | Official PDF URL | Traceability back to publisher |

## Model

AWARDS_DATA aggregates by supplier name string, category code and created date. These are logical reporting dimensions and are not a validated corporate supplier master or enforced foreign keys.

## QA rules

The reproducibility script validates the CSV schema, row order, required fields, nonnegative decimal amounts, FY2026 date scope, source URL/page and exact supplier/category/day reconciliation. The Excel DATA_QA view checks ten measures, including repeated procurement-number occurrences.

**Known duplicates:** 250-14-758-IT and 714-24-276-BT occur twice; 751-25-474-TMS occurs three times. That is 52 entries and 48 unique IDs. Duplicates may represent separate awarded entries; retain them until validated.

**Large exception:** source row 19, procurement 705-25-1021-BT, describes an NZTA national-land-transport-fund/frontloading arrangement at NZ$9,250,200 (61.2% of the pilot's value). This may not be economically comparable to external supplier awards; classify separately after manual review.

## Limitations

- Public disclosure does not prove independent financial audit accuracy.
- Some source supplier names are truncated; matching legal entities requires more data.
- The selected 52 rows are nonrandom and cover 1–10 July 2025 only.
- The PDF does not specify GST treatment for values.
- The raw page was manually transcribed, not ingested through a verified full-document parser.
- No source records of actual delivery, PO receipts, payments, savings or verified misconduct.

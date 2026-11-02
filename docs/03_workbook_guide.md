# Excel workbook walkthrough

Open [NZ_Public_Procurement_Awards_Intelligence.xlsx](../workbook/NZ_Public_Procurement_Awards_Intelligence.xlsx) in Microsoft Excel desktop.

1. **DASHBOARD** — 52 published entries and NZ$15.11m disclosed award value, not Auckland Transport's annual procurement spending.
2. **AWARDS_DATA** — One row per disclosed PDF entry. Inspect the exact supplier name, category code, date, source page and URL.
3. **SUPPLIER_SCORECARD** — Award value by raw supplier-name string. REVIEW OUTLIER is an illustrative prompt to investigate high sample concentration; **not** supplier risk or misconduct.
4. **CATEGORY_EXPOSURE** — Breakdown by unexpanded official category codes.
5. **DAILY_TREND** — Values by contract-created date, **not** payment or delivery date.
6. **DATA_QA** — Formula checks for count, amounts, missing keys, distinct procurement IDs and rollups.
7. **KPI_DICTIONARY** and **SOURCE_LOG** — Definition, provenance and interpretive limitations.

## Updating the model

The workbook is a **fixed 52-entry pilot**, not an automatically refreshing procurement application. If replacing the source, extend AWARDS_DATA and dependent formula/table ranges, recheck category and supplier lists, and revise sample-based expectations. Regenerate the aggregate evidence with the standard-library Python script and review discrepancies before reporting.

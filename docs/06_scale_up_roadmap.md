# Roadmap - toward a refreshable real-data procurement product

This is a **limited real-source pilot**, not a completed enterprise procurement platform.

## Stage 1 - Full Auckland Transport PDF extraction

1. Confirm publisher reuse conditions and pin a dated source edition.
2. Extract **all** pages with a tested PDF-table parser, preserving source page, row, checksum and raw text.
3. Manually verify samples from beginning, middle and end; track ambiguous/truncated records in an exception queue.
4. Validate complete row counts against official source totals where available; never infer missing fields.

**Definition of done:** reviewed page coverage, documented exceptions, reproducible source-to-dataset pipeline.

## Stage 2 - MBIE GETS ingestion

1. Obtain official award, supplier, category and region CSVs and schema from the [MBIE open-data page](https://www.mbie.govt.nz/cross-government-functions/new-zealand-government-procurement-and-property/open-data).
2. Preserve source grains and inspect tender-to-supplier/category cardinalities before joins.
3. Use an award–supplier bridge for multi-supplier awards; prevent double-counting when expanding rows.
4. Explicitly handle missing values, non-awards, contract categories, and reported vs unreported award amounts.
5. Match legal suppliers with NZBN only when supported by evidence; log uncertainty.

**Definition of done:** schema mapping, documented transformations, reconciled award counts/values and join QA.

## Stage 3 - Reporting and governance

Decision views: disclosure coverage, category and agency trends, concentration (with outlier controls), unusual entries, quality exceptions. Establish source refresh schedule, data owner, KPI dictionary, approval record and change log. Alert on upstream schema changes.

## Stage 4 - Operational purchasing KPIs

Actual backlog, supplier OTIF, goods-receipt variance, late deliveries and **paid spend** require lawful access to internal purchase orders, receiving events, original/revised due dates and invoices. They cannot be derived from the public award notices alone.

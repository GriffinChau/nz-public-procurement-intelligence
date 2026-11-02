# Business case - New Zealand public procurement award intelligence

## Problem

Public contract-award disclosures are useful for market research, procurement transparency and supplier/category planning, but PDFs are difficult to compare, aggregate and reconcile. Decision-makers can misinterpret **award value** as cash spend or treat one procurement identifier as one unique award entry. Large, exceptional agreements can dominate naïve supplier-concentration comparisons.

## Stakeholders and practical decisions

| Stakeholder | Question | Decision supported |
|---|---|---|
| Procurement/Category Lead | What award categories and entries are material in an inspected publication? | Choose cases for detailed review or additional data collection |
| Supplier Relationship Analyst | Which supplier-name strings appear most in selected records? | Prioritise enrichment and supplier-ID verification, without inferring quality |
| Business Analyst | Are award dates and meanings clearly defined? | Approve KPI definitions and prevent misleading interpretation |
| Data Quality Analyst | Which records look duplicated or anomalous? | Investigate instead of silently deleting legitimate line items |

## Scope

**In:** Official public award entries; value and category aggregation; vendor-name concentration; source links; QA; outlier interpretation.

**Out:** Purchase-order backlogs, goods receipts, supplier delivery performance, invoice spend, claimed savings, supplier misconduct, fiscal-year-wide inference.

## Requirements to acceptance evidence

| ID | Requirement | Evidence |
|---|---|---|
| BR-01 | Trace each record to publisher and PDF page | Source page/URL in AWARDS_DATA and CSV |
| BR-02 | Reconcile published values across entries, suppliers and categories | NZ$15,111,059.25 in DATA_QA and independent script |
| BR-03 | Retain potentially valid multiple entries under same procurement ID | 52 entries vs 48 distinct procurement IDs |
| BR-04 | Never represent award value as paid spend | Dashboard labels and KPI definitions |
| BR-05 | Flag material exceptions | NZTA-associated NZ$9.25m entry marked for review |
| BR-06 | Disclose scope and uncertainty | SOURCE_LOG, KPI_DICTIONARY and source notes |

This prototype demonstrates a traceable decision-support process, **not measured business improvements**.

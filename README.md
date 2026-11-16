# E-commerce Delivery & Logistics Performance Analysis

A comprehensive data analytics project investigating e-commerce order fulfillment, delivery reliability, warehouse dispatch latency, regional transit variances, and customer satisfaction impacts using the Olist Brazilian E-Commerce dataset (~100k orders from 2016 to 2018).

---

## 📌 Project Overview & Business Context

Reliable order fulfillment is critical for online retailers to preserve customer trust, minimize logistics expenditures, and prevent churn. Fulfillment failures—including warehouse processing backlogs, carrier transit delays, regional bottlenecks, and cancellations—frequently translate into low review ratings and operational overhead.

### Key Objectives
1. **Operational Visibility**: Track end-to-end lifecycle metrics: order processing latency, carrier transit duration, on-time delivery rates, cancellations, and customer review scores.
2. **KPI Accuracy**: Establish unambiguous definitions for On-Time Delivery (OTD), Delay Duration, and Cancellation Rates with strictly documented numerators and denominators.
3. **Comparative Analysis**: Identify performance disparities across carriers, destination states/regions, weekdays, product categories, and distance bands.
4. **Customer Experience Correlation**: Statistically evaluate the link between shipment delays and 1-star customer ratings.
5. **Actionable Delivery**: Deliver an executive dashboard and operational recommendations targeting high-impact fulfillment bottlenecks.

---

## 🏗 Repository Structure

Following universal data-engineering and data-science reproducibility standards:

```text
ecommerce_logistics_analysis/
├── data/
│   ├── raw/                # Immutable raw CSV files from source
│   ├── interim/            # Cleaned, standardized, and SQLite-indexed tables
│   └── processed/          # Final analytical datasets optimized for reporting/BI
├── notebooks/
│   └── 01_data_ingestion_and_eda.ipynb   # Week 1 data ingestion, audit, & EDA
├── src/
│   ├── __init__.py
│   ├── ingest_and_clean.py # Modular ETL & cleaning pipeline
│   └── generate_eda_charts.py # Chart generation script
├── reports/
│   ├── data_dictionary.md  # Detailed schema, field definitions, data types
│   ├── data_quality_audit.md # Missing values, anomalies, and exclusion rationale
│   └── figures/            # High-resolution generated EDA visualizations
├── .gitignore
├── README.md               # Project documentation and guide
└── requirements.txt        # Python dependency manifest
```

---

## 🗄 Dataset Summary

This project utilizes the **Olist Brazilian E-Commerce Public Dataset**, covering 99,441 unique orders from September 2016 to October 2018 across Brazil:
* `olist_orders_dataset.csv`: Order status and 5 lifecycle timestamps (purchase, approval, carrier dispatch, customer delivery, estimated delivery).
* `olist_order_items_dataset.csv`: Item-level pricing, freight values, seller IDs, and shipping deadlines.
* `olist_order_reviews_dataset.csv`: Customer review scores (1 to 5) and timestamps.
* `olist_customers_dataset.csv`: Customer location (city, state, zip code).
* `olist_sellers_dataset.csv`: Seller/dispatch location (city, state, zip code).
* `olist_products_dataset.csv` & `product_category_name_translation.csv`: Product dimensions, weight, and English category names.
* `olist_geolocation_dataset.csv`: Lat/long coordinates by zip prefix.

---

## 📅 Four-Week Implementation Plan

* **Week 1: Data Ingestion, Validation & Exploratory Analysis** *(Current)*
  * Establish reproducible folder hierarchy.
  * Ingest raw CSVs into SQLite database (`data/interim/logistics.db`).
  * Audit missing data, duplicates, and timestamp anomalies.
  * Produce data dictionary, data quality audit report, and initial EDA charts.
* **Week 2: KPI Engineering & Delay Pattern Analysis**
  * Define standard KPI formulas (OTD rate, cancellation rate, processing duration, transit delay).
  * Segment performance across states, carriers, and categories.
* **Week 3: Deeper Analysis & Operational Opportunity Assessment**
  * Drill down into route distance bands, warehouse processing bottlenecks, and customer rating degradation curves.
* **Week 4: Power BI Dashboard, Reporting & Presentation**
  * Interactive Power BI / Tableau dashboard with drill-down filters and executive summary report.

---

## 🚀 Quickstart & Setup

1. **Clone & Environment Setup**:
   ```bash
   git clone https://github.com/dog098263-ui/ecommerce-delivery-logistics-analysis.git
   cd ecommerce-delivery-logistics-analysis
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Download Raw Dataset**:
   Raw CSV files (~120MB uncompressed) are excluded from git to prevent repository bloat. Automatically download and extract them into `data/raw/` with:
   ```bash
   python3 src/download_data.py
   ```
   *(Alternatively, download `olist_dataset.zip` manually from [GitHub Releases](https://github.com/dog098263-ui/ecommerce-delivery-logistics-analysis/releases/tag/v1.0.0-data) and unzip into `data/raw/`)*.

3. **Run Pipeline & Analysis**:
   ```bash
   # 1. Ingest, audit, and clean data (creates SQLite DB and interim datasets)
   python3 src/ingest_and_clean.py

   # 2. Generate EDA visualizations
   python3 src/generate_eda_charts.py
   ```

3. **Explore Notebooks**:
   Open `notebooks/01_data_ingestion_and_eda.ipynb` in your preferred Jupyter/IDE environment.

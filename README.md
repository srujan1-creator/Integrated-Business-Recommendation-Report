# Agribusiness Data Science Project

An applied, multi-modal data science and machine learning repository for the agribusiness sector, spanning market intelligence, climate reanalysis, satellite remote sensing, and commodity economics.

---

## Project Milestones & Deliverables

### Week 1: Agribusiness Market Analysis & Planning
* **Focus**: Ecosystem value chain mapping, PESTLE analysis, KPI taxonomy, and conceptual 4-tier data science pipeline architecture.
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Market_Analysis_and_Planning_Report.docx`](file:///c:/Agridatascience%20project/Agribusiness_Market_Analysis_and_Planning_Report.docx) (~4,000 words, executive styling).
* **Technical Report (Markdown)**: [`Agribusiness_Market_Analysis_and_Planning_Report.md`](file:///c:/Agridatascience%20project/Agribusiness_Market_Analysis_and_Planning_Report.md).
* **Automated Generator**: [`generate_report.py`](file:///c:/Agridatascience%20project/generate_report.py).

---

### Week 2: Public Data Collection and Preprocessing (Current Phase)
* **Focus**: Systematic public data sourcing (FAOSTAT, USDA NASS, NASA POWER, Sentinel-2 MSI, World Bank Pink Sheet), multi-modal schema design, automated retrieval pipelines, data harmonization, and preprocessing challenge mitigation (30–35 hours scope).
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx`](file:///c:/Agridatascience%20project/Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx) (Executive styled Word report with custom callouts, standardized tables, and full variable dictionary).
* **Technical Report (Markdown)**: [`Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md`](file:///c:/Agridatascience%20project/Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md).
* **Automated Generator**: [`generate_week2_report.py`](file:///c:/Agridatascience%20project/generate_week2_report.py).
* **Data Pipelines**:
  - Ingestion: [`src/data_collection/collect_public_data.py`](file:///c:/Agridatascience%20project/src/data_collection/collect_public_data.py) (Live NASA POWER API, USDA/FAO benchmarks, World Bank prices).
  - Preprocessing & Validation: [`src/preprocessing/clean_and_harmonize.py`](file:///c:/Agridatascience%20project/src/preprocessing/clean_and_harmonize.py) (GDD, VPD, metric harmonization, cloud-filtering, and automated schema assertions).
* **Datasets Stored**:
  - Bronze Raw Layer: [`data/raw/`](file:///c:/Agridatascience%20project/data/raw/)
  - Silver Processed Layer: [`data/processed/`](file:///c:/Agridatascience%20project/data/processed/)

---

## Directory Architecture

```text
Agridatascience project/
├── data/
│   ├── raw/                               # Bronze Layer (immutable source extracts)
│   │   ├── crop_production_statistics_raw.csv
│   │   ├── nasa_power_agrometeorology_raw.csv
│   │   └── world_bank_commodity_prices_raw.csv
│   └── processed/                         # Silver Layer (harmonized & validated)
│       ├── commodity_market_prices_cleaned.csv
│       ├── crop_production_statistics_harmonized.csv
│       ├── sentinel2_ndvi_phenology_cleaned.csv
│       └── weather_agrometeorology_cleaned.csv
├── src/
│   ├── data_collection/
│   │   └── collect_public_data.py         # Live API & public data ingestion
│   └── preprocessing/
│       └── clean_and_harmonize.py         # Unit conversion, GDD, VPD, SG filtering
├── Agribusiness_Market_Analysis_and_Planning_Report.docx   # Week 1 Word deliverable
├── Agribusiness_Market_Analysis_and_Planning_Report.md     # Week 1 Markdown report
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx # Week 2 Word deliverable
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md   # Week 2 Markdown report
├── generate_report.py                     # Week 1 docx generator
├── generate_week2_report.py               # Week 2 docx generator
└── README.md
```

---

## Execution Instructions

### 1. Ingest Raw Public Data
Fetches live agrometeorology from the NASA POWER API and compiles benchmark agricultural statistics and commodity prices:
```powershell
python src/data_collection/collect_public_data.py
```

### 2. Clean, Harmonize, and Validate Datasets
Calculates agronomic indices (GDD, VPD), converts imperial bushels to metric tons/ha, applies Savitzky-Golay cloud smoothing, and executes automated schema assertions:
```powershell
python src/preprocessing/clean_and_harmonize.py
```

### 3. Re-compile Formal Reports
To regenerate the submission-ready Word deliverables:
```powershell
# Generate Week 1 Report
python generate_report.py

# Generate Week 2 Report
python generate_week2_report.py
```

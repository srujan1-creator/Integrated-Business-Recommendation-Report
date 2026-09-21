# Agribusiness Data Science Project

An applied, multi-modal data science and machine learning repository for the agribusiness sector, spanning market intelligence, climate reanalysis, satellite remote sensing, commodity economics, and predictive yield analytics.

---

## Project Milestones & Deliverables

### Week 1: Agribusiness Market Analysis & Planning
* **Focus**: Ecosystem value chain mapping, PESTLE analysis, KPI taxonomy, and conceptual 4-tier data science pipeline architecture.
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Market_Analysis_and_Planning_Report.docx`](./Agribusiness_Market_Analysis_and_Planning_Report.docx) (~4,000 words, executive styling).
* **Technical Report (Markdown)**: [`Agribusiness_Market_Analysis_and_Planning_Report.md`](./Agribusiness_Market_Analysis_and_Planning_Report.md).
* **Automated Generator**: [`generate_report.py`](./generate_report.py).
* **GitHub Repository**: [`srujan1-creator/Agribusiness-Market-Analysis-Planning`](https://github.com/srujan1-creator/Agribusiness-Market-Analysis-Planning.git)

---

### Week 2: Public Data Collection and Preprocessing
* **Focus**: Systematic public data sourcing (FAOSTAT, USDA NASS, NASA POWER, Sentinel-2 MSI, World Bank Pink Sheet), multi-modal schema design, automated retrieval pipelines, data harmonization, and preprocessing challenge mitigation (30–35 hours scope).
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx`](./Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx) (Executive Word deliverable with variable dictionaries and schema assertions).
* **Technical Report (Markdown)**: [`Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md`](./Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md).
* **Automated Generator**: [`generate_week2_report.py`](./generate_week2_report.py).
* **GitHub Repository**: [`srujan1-creator/Public-Data-Collection-and-Preprocessing`](https://github.com/srujan1-creator/Public-Data-Collection-and-Preprocessing.git)

---

### Week 3: Exploratory Data Analysis and Visualization (Current Phase)
* **Focus**: Rigorous exploratory data analysis (EDA), univariate statistical moments, bivariate/multivariate correlation decomposition, biological phenology extraction, and multi-tiered anomaly detection across the four agribusiness tiers (30–35 hours scope).
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx`](./Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx) (Executive Word document, 3.9 MB, 8 High-Resolution 300 DPI Figures, 8 Standardized Tables, and Callouts).
* **Technical Report (Markdown)**: [`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md`](./Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md).
* **Automated Word Generator**: [`generate_week3_report.py`](./generate_week3_report.py).
* **Analytical EDA Engine**: [`src/eda/exploratory_analysis.py`](./src/eda/exploratory_analysis.py) (Computes moments, kurtosis, skewness, generates 8 publication-grade charts).
* **Figure Catalog**: [`reports/figures/`](./reports/figures/)
  1. `fig1_thermal_regimes_gdd.png`: Diurnal temperature range & GDD accumulation vs corn developmental stages.
  2. `fig2_hydrological_moisture_vpd.png`: Rainfall clusters & Vapor Pressure Deficit atmospheric moisture stress zones.
  3. `fig3_sentinel2_ndvi_phenology.png`: Sentinel-2 MSI NDVI canopy curve & Savitzky-Golay cloud filtering.
  4. `fig4_commodity_prices_volatility.png`: World Bank FOB benchmark prices & 3-month rolling volatility spikes.
  5. `fig5_input_output_parity_ratios.png`: DAP fertilizer-to-grain parity ratios & farm margin compression.
  6. `fig6_crop_yield_benchmarks.png`: Comparative crop yields (MT/ha) & 2020 Derecho land abandonment efficiency.
  7. `fig7_multivariate_correlation_matrix.png`: Dual Pearson (linear) and Spearman (rank) correlation heatmaps.
  8. `fig8_anomaly_detection_dashboard.png`: 4-quadrant multi-modal anomaly detection dashboard.
* **GitHub Repository**: [`srujan1-creator/Exploratory-Data-Analysis-and-Visualization`](https://github.com/srujan1-creator/Exploratory-Data-Analysis-and-Visualization.git)

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
│       ├── eda_summary_statistics.json    # Full statistical moments & anomaly metrics
│       ├── sentinel2_ndvi_phenology_cleaned.csv
│       └── weather_agrometeorology_cleaned.csv
├── reports/
│   └── figures/                           # Publication-grade figures (300 DPI)
│       ├── fig1_thermal_regimes_gdd.png
│       ├── fig2_hydrological_moisture_vpd.png
│       ├── fig3_sentinel2_ndvi_phenology.png
│       ├── fig4_commodity_prices_volatility.png
│       ├── fig5_input_output_parity_ratios.png
│       ├── fig6_crop_yield_benchmarks.png
│       ├── fig7_multivariate_correlation_matrix.png
│       └── fig8_anomaly_detection_dashboard.png
├── src/
│   ├── data_collection/
│   │   └── collect_public_data.py         # Live API & public data ingestion
│   ├── preprocessing/
│   │   └── clean_and_harmonize.py         # Unit conversion, GDD, VPD, SG filtering
│   └── eda/
│       └── exploratory_analysis.py        # Statistical engine & visualization generator
├── Agribusiness_Market_Analysis_and_Planning_Report.docx   # Week 1 Word deliverable
├── Agribusiness_Market_Analysis_and_Planning_Report.md     # Week 1 Markdown report
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx # Week 2 Word deliverable
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md   # Week 2 Markdown report
├── Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx # Week 3 Word deliverable
├── Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md   # Week 3 Markdown report
├── generate_report.py                     # Week 1 docx generator
├── generate_week2_report.py               # Week 2 docx generator
├── generate_week3_report.py               # Week 3 docx generator
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

### 3. Run Exploratory Data Analysis & Generate Visualizations
Computes univariate moments, correlation matrices, anomaly metrics, and outputs 8 publication-grade charts to `reports/figures/`:
```powershell
python src/eda/exploratory_analysis.py
```

### 4. Compile Submission-Ready Reports
To regenerate the formal executive Word deliverables:
```powershell
# Generate Week 1 Report
python generate_report.py

# Generate Week 2 Report
python generate_week2_report.py

# Generate Week 3 Report
python generate_week3_report.py
```

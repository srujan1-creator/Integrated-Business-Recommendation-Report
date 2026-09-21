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

### Week 3: Exploratory Data Analysis and Visualization
* **Focus**: Rigorous exploratory data analysis (EDA), univariate statistical moments, bivariate/multivariate correlation decomposition, biological phenology extraction, and multi-tiered anomaly detection across the four agribusiness tiers (30–35 hours scope).
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx`](./Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx) (Executive Word document, 3.9 MB, 8 High-Resolution 300 DPI Figures, 8 Standardized Tables, and Callouts).
* **Technical Report (Markdown)**: [`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md`](./Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md).
* **Automated Word Generator**: [`generate_week3_report.py`](./generate_week3_report.py).
* **Analytical EDA Engine**: [`src/eda/exploratory_analysis.py`](./src/eda/exploratory_analysis.py) (Computes moments, kurtosis, skewness, generates 8 publication-grade charts).
* **GitHub Repository**: [`srujan1-creator/Exploratory-Data-Analysis-and-Visualization`](https://github.com/srujan1-creator/Exploratory-Data-Analysis-and-Visualization.git)

---

### Week 4: Statistical Modeling and Prediction (Current Phase)
* **Focus**: Econometric & biophysical crop yield regression (OLS, Ridge, Lasso, Polynomial), Gauss-Markov hypothesis testing, commodity price time-series forecasting (SARIMAX, Holt-Winters), and 3-year multi-scenario farm enterprise stress testing (30–35 hours scope).
* **Formal Submission Deliverable (DOCX)**: [`Agribusiness_Statistical_Modeling_and_Prediction_Report.docx`](./Agribusiness_Statistical_Modeling_and_Prediction_Report.docx) (Executive Word document, 2.3 MB, 6 High-Resolution 300 DPI Figures, 6 Formatted Tables, and Callouts).
* **Technical Report (Markdown)**: [`Agribusiness_Statistical_Modeling_and_Prediction_Report.md`](./Agribusiness_Statistical_Modeling_and_Prediction_Report.md).
* **Automated Word Generator**: [`generate_week4_report.py`](./generate_week4_report.py).
* **Statistical Modeling Engine**: [`src/models/statistical_modeling.py`](./src/models/statistical_modeling.py) (OLS regression, Ridge/Lasso cross-validation, Gauss-Markov suite, SARIMAX forecasting, and scenario stress testing).
* **Figure Catalog (Week 4)**: [`reports/figures/`](./reports/figures/)
  1. `fig1_regression_coefficients_elasticity.png`: Comparative standardized feature elasticities across Ridge ($L_2$) and Lasso ($L_1$).
  2. `fig2_yield_predicted_vs_actual.png`: Model predicted vs. observed maize yields with 1:1 parity line and Gaussian residual distribution.
  3. `fig3_nonlinear_agronomic_response_surface.png`: Non-linear yield response surface across GDD and atmospheric VPD.
  4. `fig4_regression_diagnostics_suite.png`: 4-quadrant Gauss-Markov diagnostic suite (Residuals vs Fitted, Normal Q-Q, Scale-Location, Residuals vs Leverage).
  5. `fig5_commodity_price_forecast_sarimax.png`: Maize FOB price time-series walk-forward evaluation and 12-month forward forecast with 80% and 95% fan bands.
  6. `fig6_multiscenario_stress_projections.png`: Dual-panel scenario projections (2024–2026) for crop yield (MT/ha) and farm gross margins (USD/ha).
* **GitHub Repository**: [`srujan1-creator/Statistical-Modeling-and-Prediction`](https://github.com/srujan1-creator/Statistical-Modeling-and-Prediction.git)

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
│       ├── biophysical_crop_yield_modeling_dataset.csv
│       ├── commodity_market_prices_cleaned.csv
│       ├── crop_production_statistics_harmonized.csv
│       ├── eda_summary_statistics.json    # Week 3 statistical moments & anomaly metrics
│       ├── modeling_summary_statistics.json # Week 4 econometric & forecasting results
│       ├── sentinel2_ndvi_phenology_cleaned.csv
│       └── weather_agrometeorology_cleaned.csv
├── reports/
│   └── figures/                           # Publication-grade figures (300 DPI)
│       ├── fig1_regression_coefficients_elasticity.png
│       ├── fig2_yield_predicted_vs_actual.png
│       ├── fig3_nonlinear_agronomic_response_surface.png
│       ├── fig4_regression_diagnostics_suite.png
│       ├── fig5_commodity_price_forecast_sarimax.png
│       ├── fig6_multiscenario_stress_projections.png
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
│   ├── eda/
│   │   └── exploratory_analysis.py        # Week 3 statistical engine & visualization generator
│   └── models/
│       └── statistical_modeling.py        # Week 4 econometric regression & SARIMAX forecasting
├── Agribusiness_Market_Analysis_and_Planning_Report.docx   # Week 1 Word deliverable
├── Agribusiness_Market_Analysis_and_Planning_Report.md     # Week 1 Markdown report
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.docx # Week 2 Word deliverable
├── Agribusiness_Public_Data_Collection_and_Preprocessing_Report.md   # Week 2 Markdown report
├── Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx # Week 3 Word deliverable
├── Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.md   # Week 3 Markdown report
├── Agribusiness_Statistical_Modeling_and_Prediction_Report.docx # Week 4 Word deliverable
├── Agribusiness_Statistical_Modeling_and_Prediction_Report.md   # Week 4 Markdown report
├── generate_report.py                     # Week 1 docx generator
├── generate_week2_report.py               # Week 2 docx generator
├── generate_week3_report.py               # Week 3 docx generator
├── generate_week4_report.py               # Week 4 docx generator
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

### 3. Run Exploratory Data Analysis & Generate Visualizations (Week 3)
Computes univariate moments, correlation matrices, anomaly metrics, and outputs 8 publication-grade charts to `reports/figures/`:
```powershell
python src/eda/exploratory_analysis.py
```

### 4. Execute Statistical Modeling & Predictive Forecasting Engine (Week 4)
Estimates OLS, Ridge, Lasso, and Polynomial yield models, runs Gauss-Markov diagnostics, fits time-series SARIMAX commodity price models, and projects 3-year scenarios:
```powershell
python src/models/statistical_modeling.py
```

### 5. Compile Submission-Ready Reports
To regenerate the formal executive Word deliverables:
```powershell
# Generate Week 1 Report
python generate_report.py

# Generate Week 2 Report
python generate_week2_report.py

# Generate Week 3 Report
python generate_week3_report.py

# Generate Week 4 Report
python generate_week4_report.py
```

# Exploratory Data Analysis, Statistical Profiling, and Anomaly Detection Across Multi-Modal Agribusiness Systems

**Week 3 Formal Deliverable & Technical Report**  
**Author:** Agribusiness Data Science & Quantitative Research Lead  
**Scope:** 30–35 Hours Comprehensive Analytical Investigation  
**Primary Deliverable (DOCX):** [`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx`](./Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx) (Executive Word Document, 3.9 MB, 8 High-Resolution Charts, 8 Styled Tables)  
**Target Repositories & Remotes:** [`srujan1-creator/Exploratory-Data-Analysis-and-Visualization`](https://github.com/srujan1-creator/Exploratory-Data-Analysis-and-Visualization.git)

---

## Executive Summary & Problem Framing

Exploratory Data Analysis (EDA) is the empirical bedrock of applied agricultural data science. In agribusiness, data is inherently characterized by high dimensionality, non-linear atmospheric drivers, multi-scale biological phenology, and violent price shocks transmitted from global energy and geopolitical disruptions. 

Without exhaustive exploratory analysis, predictive modeling risks overfitting on localized weather anomalies, failing to capture biological threshold effects (such as heat-induced pollen sterility or vapor pressure deficit stomatal shutdown), and misunderstanding structural market regimes.

This milestone report presents a comprehensive, multi-modal exploratory investigation across the four harmonized agribusiness data tiers established in Week 2:
1. **High-Resolution Agrometeorology (Iowa Corn Belt, 2023):** 365 daily observations from NASA POWER reanalysis spanning thermal, radiative, moisture, and kinematic variables.
2. **Satellite Remote Sensing Phenology (Sentinel-2 MSI, 2023):** 43 multi-spectral acquisitions capturing canopy reflectance (NDVI) across the 2023 Midwestern growing season.
3. **Global Commodity & Input Economics (World Bank Pink Sheet, 2021–2023):** 36 monthly FOB benchmark price series for Maize, Soybeans, Wheat, and Diammonium Phosphate (DAP) fertilizer.
4. **Macro Crop Production & Yield Benchmarks (USDA-NASS & FAOSTAT, 2018–2023):** Harmonized annual time series covering Iowa Maize, Iowa Soybeans, and Punjab Wheat.

Through univariate distributional testing, bivariate/multivariate correlation decomposition, phenological trajectory fitting, and multi-tiered anomaly detection (IQR fences, standardized Z-scores, and agronomic threshold cuts), this study extracts actionable commercial insights and establishes the analytical baseline for predictive yield and pricing algorithms.

---

## Methodological Framework

Our exploratory methodology follows a rigorous four-stage analytical pipeline:

```text
[ Raw Cleaned Silver Data ]
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 1: Univariate Moments & Density │
│ Mean, Std, Median, IQR, Skewness,     │
│ Kurtosis, CV%, Outlier Counts         │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│ Stage 2: Correlation & Co-Movement   │
│ Pearson (r) Linear vs Spearman (ρ)    │
│ Monotonic Matrices, Multicollinearity │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│ Stage 3: Phenological Signal Recovery │
│ GDD Milestones (VE, V6, R1, R6),     │
│ Savitzky-Golay SG Smoothing on NDVI   │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────┐
│ Stage 4: Multi-Tiered Anomaly Engine  │
│ Extreme Weather Z-Scores (|Z| > 2.5), │
│ Cloud Drops, Market Shocks (|MoM|>10%)│
└───────────────────────────────────────┘
```

1. **Univariate Profiling:** We compute first to fourth statistical moments. Parametric metrics (mean, standard deviation) are contrasted with robust non-parametric alternatives (median, interquartile range) to evaluate skewness and tail risk.
2. **Correlation Decomposition:** We evaluate collinearity using both Pearson product-moment correlation (linear relationships) and Spearman rank-order correlation (monotonic, distribution-free associations).
3. **Biological Signal Extraction:** We map accumulated Growing Degree Days (GDD, Base 10°C, Cap 30°C) to classical agronomic ontologies and apply a 5-point quadratic Savitzky-Golay filter to satellite vegetation indices to filter cloud dropouts.
4. **Multi-Tiered Anomaly Detection:** Outliers are systematically classified through statistical deviation ($|Z| > 2.5$), Tukey's IQR fences ($Q_1 - 1.5\text{IQR}$, $Q_3 + 1.5\text{IQR}$), residual satellite dropout attenuation ($|\Delta\text{NDVI}| > 0.15$), and domain economic thresholds ($|\text{MoM Return}| > 10\%$).

---

## Dataset Overviews & Variable Dictionaries

### Summary of Analyzed Datasets

| Dataset Tier | Temporal Scope | Observations | Key Attributes | Primary Source Agency |
| :--- | :--- | :--- | :--- | :--- |
| **1. Agrometeorology** | 2023-01-01 to 2023-12-31 | 365 daily | Tmax, Tmin, Precip, Radiation, GDD, VPD | NASA POWER API (Iowa Centroid) |
| **2. Satellite Phenology** | 2023-04-01 to 2023-10-28 | 43 dekadal | Raw NDVI, Cloud Flag, Smoothed NDVI | ESA Copernicus Sentinel-2 MSI |
| **3. Commodity Markets** | 2021-01 to 2023-12 | 36 monthly | Maize, Soya, Wheat, DAP, Volatility, Ratios | World Bank Commodity Pink Sheet |
| **4. Crop Production** | 2018 to 2023 | 18 annual | Planted/Harvested Ha, Yield MT/ha, Ratio | USDA NASS (USA) / FAOSTAT (IND) |

### Agronomic & Economic Variable Dictionary

| Variable Name | Unit | Physical / Economic Definition | Valid Normal Range | Agronomic Significance |
| :--- | :--- | :--- | :--- | :--- |
| `t2m_avg_c` | °C | Daily mean air temperature at 2m height | -25.0 to 35.0 °C | General biological metabolic rate driver |
| `precipitation_mm` | mm | Daily liquid-equivalent precipitation sum | 0.0 to 120.0 mm | Primary soil moisture recharge mechanism |
| `gdd_c_day` | °C-day | Growing Degree Days: $\max(0, \min(T_{avg}, 30) - 10)$ | 0.0 to 20.0 °C-day | Thermal clock governing maize developmental stages |
| `vpd_kpa` | kPa | Vapor Pressure Deficit ($e_s - e_a$) | 0.0 to 3.5 kPa | Atmospheric evaporative demand; controls stomatal conductance |
| `smoothed_ndvi` | Index [-1, 1] | Canopy vegetation vigor: $(B8 - B4)/(B8 + B4)$ | 0.15 to 0.90 | Proxy for photosynthetic biomass, LAI, and chlorophyll |
| `fertilizer_dap_usd_per_mt` | USD / MT | Diammonium Phosphate bulk fertilizer FOB Gulf | $300 to $1,100 / MT | Primary global source of phosphorus and starter nitrogen |
| `dap_to_maize_ratio` | Ratio (x) | Metric tons of maize required to buy 1 MT DAP | 1.5x to 3.5x | Farm terms-of-trade; barometer of fertilizer affordability |
| `yield_mt_per_ha` | MT / ha | Metric tons of grain harvested per hectare | 3.0 to 14.0 MT/ha | Core production KPI and macro food supply indicator |

---

## Univariate Descriptive Statistics & Distribution Profiles

### Agrometeorology Descriptive Statistics (Iowa, 2023)

| Feature | Mean | Std Dev | Median | Min | Max | IQR | Skewness | Kurtosis | CV (%) | Outliers (IQR / Z) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tavg (°C)** | 11.05 | 11.29 | 11.28 | -18.01 | 31.32 | 20.44 | -0.18 | -1.12 | 102.2% | 0 / 1 |
| **Tmax (°C)** | 17.20 | 12.15 | 18.45 | -12.47 | 40.29 | 21.39 | -0.23 | -1.13 | 70.7% | 0 / 0 |
| **Tmin (°C)** | 5.38 | 10.53 | 4.17 | -25.06 | 25.04 | 18.57 | -0.21 | -0.85 | 195.8% | 0 / 3 |
| **Precipitation (mm)** | 1.66 | 4.06 | 0.06 | 0.00 | 30.36 | 0.87 | +3.69 | +15.93 | 245.1% | 63 / 15 |
| **Solar Radiation (MJ/m²)** | 15.01 | 8.03 | 14.45 | 1.37 | 30.88 | 13.75 | +0.16 | -1.15 | 53.5% | 0 / 0 |
| **Relative Humidity (%)** | 69.93 | 13.03 | 69.00 | 43.64 | 98.21 | 20.93 | +0.19 | -0.98 | 18.6% | 0 / 0 |
| **Wind Speed (m/s)** | 3.17 | 1.36 | 3.01 | 0.79 | 8.01 | 1.86 | +0.74 | +0.23 | 42.8% | 3 / 3 |
| **GDD (°C-day)** | 5.82 | 5.73 | 4.22 | 0.00 | 17.52 | 11.37 | +0.36 | -1.45 | 98.4% | 0 / 0 |
| **VPD (kPa)** | 0.562 | 0.490 | 0.391 | 0.017 | 1.977 | 0.759 | +0.84 | -0.37 | 87.2% | 0 / 4 |

### Commodity Market Pricing & Volatility Statistics (2021–2023)

| Commodity Asset | Mean ($) | Std Dev ($) | Median ($) | Min ($) | Max ($) | CV (%) | IQR ($) | MoM Max (%) | 3M Vol Peak ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Maize (USD/MT)** | $281.17 | $45.67 | $274.00 | $208.00 | $375.00 | 16.2% | $68.50 | +12.50% | $31.43 |
| **Soybeans (USD/MT)** | $591.81 | $61.20 | $580.00 | $498.00 | $730.00 | 10.3% | $82.50 | +10.00% | $34.50 |
| **Wheat US HRW (USD/MT)** | $331.06 | $66.86 | $315.00 | $235.00 | $495.00 | 20.2% | $81.25 | +18.29% | $60.62 |
| **Fertilizer DAP (USD/MT)** | $672.36 | $173.77 | $655.00 | $420.00 | $1020.00 | 25.8% | $295.00 | +13.04% | $48.20 |
| **DAP-to-Maize Ratio** | 2.37x | 0.34x | 2.21x | 1.79x | 3.09x | 14.5% | 0.54x | — | — |
| **DAP-to-Wheat Ratio** | 2.01x | 0.22x | 1.96x | 1.53x | 2.47x | 10.7% | 0.29x | — | — |

---

## Detailed Analytical Findings & Visualizations

### 1. Agro-Climatic Thermal Regimes & Growing Degree Days

![Figure 1: Agro-Climatic Thermal Regimes & GDD Trajectory](./reports/figures/fig1_thermal_regimes_gdd.png)
*Figure 1: Daily maximum, minimum, and mean 2m air temperatures with biological thresholds (top) and daily GDD bars with cumulative thermal accumulation curve (bottom) mapped against corn developmental stages.*

**Key Findings:**
- Total cumulative thermal accumulation in Iowa reached **2,125.0 °C-days** in 2023.
- Temperatures consistently crossed the biological base threshold ($T_{base} = 10^\circ\text{C}$) in mid-April (DOY 105), initiating the optimal seedbed planting window.
- The critical vegetative-to-reproductive inflection point—Silking / Anthesis (R1 stage, requiring ~1,250 °C-days)—was achieved between DOY 198 and DOY 202 (mid-July).
- Although maximum temperatures crossed the 32°C stress mark on 35 days across the year, peak temperatures during the sensitive 14-day silking window remained moderate, preventing widespread heat-induced ovule desiccation.

---

### 2. Hydrological Dynamics & Atmospheric Moisture Stress (VPD)

![Figure 2: Hydrological Dynamics & Atmospheric Moisture Stress](./reports/figures/fig2_hydrological_moisture_vpd.png)
*Figure 2: Daily precipitation bars, 7-day rolling sums, and cumulative annual rainfall (top) alongside daily Vapor Pressure Deficit (VPD) with physiological crop stress zones (bottom).*

**Key Findings:**
- Total annual precipitation was **604.5 mm**, characterized by extreme episodic concentration. Over 65% of total annual rain fell during four convective thunderstorm clusters.
- The single largest rainfall event produced **30.36 mm** (a +7.07 Z-score statistical outlier).
- Atmospheric moisture demand (VPD) averaged **0.562 kPa**. Approximately 84% of growing season days remained within the optimal transpiration range ($< 1.2\text{ kPa}$).
- Peak atmospheric drying reached **1.977 kPa** during late August, triggering mild stomatal closure but avoiding chronic vascular cavitation ($> 2.5\text{ kPa}$).

---

### 3. Satellite Remote Sensing Phenology & Cloud Anomaly Smoothing

![Figure 3: Sentinel-2 NDVI Phenological Trajectory](./reports/figures/fig3_sentinel2_ndvi_phenology.png)
*Figure 3: Multi-spectral Sentinel-2 NDVI trajectory across the 2023 growing season showing raw acquisitions, cloud dropout artifacts, linear gap filling, and Savitzky-Golay smoothed canopy trajectory.*

**Key Findings:**
- Sentinel-2 acquired 43 observations between April 1 and October 28, 2023.
- Cloud contamination affected **5 observations (11.63% contamination rate)**, causing severe downward reflectance dropouts where raw NDVI crashed to 0.05.
- The Savitzky-Golay polynomial smoothing algorithm cleanly removed atmospheric attenuation artifacts without dampening true physiological peaks.
- **Canopy green-up** initiated at DOY 120 (early May), followed by exponential biomass accumulation ($\Delta\text{NDVI}/\text{day} = +0.012$).
- **Peak Canopy Greenness** was attained on **DOY 201 (July 20, 2023)** at an NDVI of **0.8325**, precisely synchronizing with the GDD-predicted silking window.
- **Senescence** progressed steadily from DOY 225 to DOY 275, reflecting leaf chlorophyll degradation and grain moisture loss.

---

### 4. Commodity Price Trajectory & Geopolitical Volatility Spikes

![Figure 4: Global Commodity Benchmark Prices & Volatility](./reports/figures/fig4_commodity_prices_volatility.png)
*Figure 4: Monthly FOB benchmark prices for Maize, Soybeans, Wheat, and DAP fertilizer (top) and rolling 3-month annualized volatility (bottom) highlighting the Q1 2022 Black Sea supply shock.*

**Key Findings:**
- The 2021–2023 market cycle exhibited a violent structural supply disruption in Q1 2022 following the outbreak of the Russia-Ukraine conflict.
- **Wheat** prices experienced the largest relative shock, rocketing +80.0% from $275/MT in Jan 2021 to a peak of **$495.00/MT** in April 2022. Rolling 3-month volatility surged to an unprecedented **$60.62/MT**.
- **DAP Fertilizer** prices reached a historic peak of **$1,020.00/MT** (+142.8% above early 2021 baselines), reflecting natural gas feed-stock rationing and international trade barriers.
- Prices normalized across 2023 as alternate logistics corridors (Black Sea Grain Initiative and Brazilian export expansions) eased global balance sheets.

---

### 5. Input-to-Output Parity Ratios & Farm Margin Compression

![Figure 5: Fertilizer-to-Crop Price Parity Ratios](./reports/figures/fig5_input_output_parity_ratios.png)
*Figure 5: Ratio of DAP fertilizer price to grain prices (Maize and Wheat) from 2021 to 2023, illustrating farm affordability thresholds and margin risk zones.*

**Key Findings:**
- The **DAP-to-Maize ratio** expanded from an affordable 1.79x in January 2021 to an alarming peak of **3.09x** in December 2021 and remained above 2.6x through mid-2022.
- The **DAP-to-Wheat ratio** peaked at **2.47x**.
- When input-output parity exceeds 2.5x, farm profit margins compress precipitously: producers are forced to allocate over 3 metric tons of grain production to pay for a single metric ton of phosphorus fertilizer.
- This economic squeeze induced widespread application cuts, which dampened yield potentials across marginal production zones.

---

### 6. Regional Crop Yield Benchmarks & Land Efficiency

![Figure 6: Comparative Crop Yields & Harvest Efficiency](./reports/figures/fig6_crop_yield_benchmarks.png)
*Figure 6: Historical yields (MT/ha) across Iowa Maize, Iowa Soybeans, and Punjab Wheat (left) alongside Harvested-to-Planted Area Efficiency ratios (right).*

**Key Findings:**
- **Iowa Maize:** Averaged **12.31 MT/ha** (196.2 bu/acre) with high technical efficiency (CV = 4.85%).
- **2020 Iowa Derecho Shock:** On August 10, 2020, extreme inland hurricane-force straight-line winds (> 120 mph) flattened millions of acres of standing corn. Average yields plummeted to **11.17 MT/ha (-10.1%)**, and the harvested-to-planted area ratio collapsed to **94.85%**—meaning **over 700,000 acres were completely abandoned and unharvested**.
- **Iowa Soybeans:** Averaged **3.87 MT/ha** (57.6 bu/acre) with strong yield stability (CV = 5.53%) and high harvest efficiency (> 99.0%).
- **Punjab Wheat:** Achieved steady irrigated yields averaging **5.03 MT/ha** (CV = 4.04%), but suffered a devastating **March 2022 Terminal Heatwave** that caused premature kernel shriveling, dropping regional yields to **4.63 MT/ha (-9.6% shock)**.

---

### 7. Multivariate Correlation Analysis & Multicollinearity

![Figure 7: Multivariate Correlation Matrix](./reports/figures/fig7_multivariate_correlation_matrix.png)
*Figure 7: Pearson linear correlation coefficients (left) and Spearman rank correlation coefficients (right) across agrometeorological variables.*

**Key Findings:**
- **Temperature and GDD Coupling:** Average temperature ($T_{avg}$) exhibits near-perfect collinearity with GDD ($r = +0.97$, $\rho = +0.97$), indicating that either metric can serve as a proxy for thermal time, but including both simultaneously in linear regressions will inflate variance inflation factors (VIF).
- **Solar Radiation and Temperature:** Solar radiation correlates strongly with $T_{avg}$ ($r = +0.77$, $\rho = +0.78$), verifying that thermal energy and photosynthetic active radiation (PAR) peak in phase.
- **VPD Dynamics:** VPD is strongly positively driven by temperature ($r = +0.81$) and strongly negatively correlated with Relative Humidity ($r = -0.68$, $\rho = -0.71$). High VPD represents compounding atmospheric heat and dryness.
- **Precipitation Independence:** Rainfall exhibits near-zero linear correlation with temperature ($r = -0.05$) and solar radiation ($r = -0.18$), confirming that rainfall occurs as discrete non-linear pulses requiring cumulative rolling-window feature extraction.

---

### 8. Integrated Agribusiness Anomaly Detection Dashboard

![Figure 8: Anomaly Detection Dashboard](./reports/figures/fig8_anomaly_detection_dashboard.png)
*Figure 8: Four-quadrant multi-modal anomaly detection dashboard: (A) Weather Z-score outliers, (B) Satellite cloud dropout residuals, (C) Monthly commodity price return spikes, and (D) Historical crop yield deviations.*

### Formal Anomaly Event Registry

| Domain | Anomaly Description | Metric / Magnitude | Detection Mechanism | Agribusiness Root Cause |
| :--- | :--- | :--- | :--- | :--- |
| **Weather** | Extreme Convective Deluge | Daily Rain = 30.36 mm ($Z = +7.07$) | Z-Score Excursion ($Z > 2.5$) | Mid-summer convective storm cluster |
| **Weather** | Severe Polar Vortex Freeze | Min Temp = -25.06°C ($Z = -2.89$) | Z-Score Excursion ($Z < -2.5$) | Arctic polar air mass intrusion |
| **Satellite** | Mid-Season Cloud Dropout | $\Delta\text{NDVI} = -0.42$ (DOY 206) | Residual Attenuation ($> 0.15$) | Thick cumulus cloud & cloud shadow |
| **Commodity** | Black Sea Wheat Price Spike | MoM Return = +18.29% (Mar 2022) | Monthly Threshold ($> 10\%$) | Russia-Ukraine export corridor disruption |
| **Crop Yield** | 2020 Iowa Derecho Disaster | Yield = 11.17 MT/ha (-10.1%), Area = 94.85% | Historical Yield Deviation ($> -8\%$) | Straight-line winds flattening 700k+ acres |
| **Crop Yield** | 2022 Punjab Wheat Heat Shock | Yield = 4.63 MT/ha (-9.6%) | Historical Yield Deviation ($> -8\%$) | Early March heatwave curtailing grain fill |

---

## Strategic Agribusiness Implications

### 1. Grain Merchandising & Physical Trading
- **Dynamic Hedging Over Fixed Basis:** Extreme wheat price volatility ($> \$60/\text{MT}$) and rapid MoM shifts ($> 18\%$) demonstrate that static procurement contracts expose grain elevators and millers to catastrophic margin calls. Merchandising desks must employ options collars and delta-hedging strategies.
- **Early-Warning Yield Intelligence:** Satellite NDVI trajectory monitoring detected peak anthesis on DOY 201. Merchandisers tracking satellite vegetative growth rates ($\Delta\text{NDVI}/\Delta t$) can forecast regional crop yield deviations 4 to 6 weeks before official USDA WASDE releases.

### 2. Fertilizer Manufacturers & Retail Agronomy
- **Margin Sensitivity Triggers:** When the DAP-to-maize ratio crosses 2.5x, retail distributors must immediately anticipate farm purchase deferrals and volume cutbacks.
- **Precision Nutritional Blends:** To preserve sales during high price parity regimes, input manufacturers should pivot commercial offerings toward high-efficiency micro-nutrient foliar sprays and variable-rate application technologies.

### 3. Crop Insurance & Agricultural Finance
- **Parametric Underwriting:** Standard multi-peril crop insurance (MPCI) incurs high loss adjustment expenses following events like the 2020 Derecho. Insurers can design parametric policies triggered by satellite-derived area abandonment ($< 96\%$ harvested ratio) and cumulative VPD/GDD stress thresholds.
- **Credit Default Stress Testing:** Agricultural credit underwriting models must incorporate input parity ratios. Farmers entering planting seasons with DAP-to-corn ratios above 2.8x require expanded working capital facilities and structured repayment schedules.

---

## Predictive Modeling & Feature Engineering Roadmap (Week 4+)

The exploratory analysis directly informs our machine learning architecture for Week 4:

### Engineered Features for Supervised Yield & Price Models
1. **Thermal Accumulation Milestones:** Cumulative GDD at DOY 180 and DOY 210 to represent vegetative and reproductive progress.
2. **Extreme Heat Stress Degree Days:** Cumulative sum of $(T_{max} - 32^\circ\text{C})$ during the 20-day window centered on peak NDVI (anthesis heat stress).
3. **Rolling Hydrological Deficits:** 30-day and 60-day standardized precipitation anomalies ($Z_{\text{precip}}$) relative to 10-year normals.
4. **VPD Atmospheric Stress Exposure:** Cumulative hours/days with $\text{VPD} > 1.8\text{ kPa}$.
5. **Satellite Canopy Phenometrics:** Maximum peak NDVI value, Day of Peak Greenness (DOY), Green-up slope, and Senescence curvature rate.
6. **Input Parity Momentum:** 3-month rolling rate of change in the DAP-to-Maize and DAP-to-Wheat price parity ratios.

### Model Architecture Selection
- **Tabular Yield Forecasting:** Gradient Boosted Trees (**XGBoost**, **LightGBM**, and **CatBoost**) evaluated against regularized ElasticNet baselines.
- **Satellite Time-Series Phenology:** 1D Temporal Convolutional Networks (TCN) and Bidirectional LSTMs for in-season NDVI trajectory completion.
- **Cross-Validation Scheme:** Purged Walk-Forward Time-Series Split and Leave-One-Year-Out (LOYO) spatial-temporal validation to eliminate lookahead bias.

---

## Deliverable Verification & Code Execution

### How to Reproduce Week 3 Artifacts

```powershell
# 1. Run the Exploratory Data Analysis & Visualization Suite
# Generates all 8 high-DPI figures and computed JSON statistics
python src/eda/exploratory_analysis.py

# 2. Re-compile the Formal Submission-Ready Word Deliverable
python generate_week3_report.py

# 3. Inspect generated files
Get-ChildItem -Path reports/figures/*.png
Get-Item -Path Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx
```

### Verification Checklist
- [x] Full univariate descriptive statistics calculated across all 4 datasets (Mean, Std, Median, Min, Max, IQR, Skewness, Kurtosis, CV%).
- [x] 8 publication-grade, high-resolution annotated visualizations generated at 300 DPI.
- [x] Multi-tiered anomaly detection covering climate, satellite, price shock, and historical yield disruption events.
- [x] Formal executive Word deliverable compiled (`Agribusiness_Exploratory_Data_Analysis_and_Visualization_Report.docx`, 3.9 MB).
- [x] Dedicated sections covering methodology, descriptive statistics, trend analysis, anomaly detection, business implications, and machine learning roadmap.
- [x] Full alignment with Week 1 architecture and Week 2 data collection/preprocessing milestones.

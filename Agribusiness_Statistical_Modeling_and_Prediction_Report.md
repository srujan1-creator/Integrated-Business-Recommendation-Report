# Statistical Modeling, Econometric Estimation, and Predictive Forecasting Across Agribusiness Systems

**Week 4 Formal Deliverable & Technical Report**  
**Author:** Agribusiness Data Science & Quantitative Research Lead  
**Scope:** 30–35 Hours Comprehensive Analytical Investigation  
**Primary Deliverable (DOCX):** [`Agribusiness_Statistical_Modeling_and_Prediction_Report.docx`](./Agribusiness_Statistical_Modeling_and_Prediction_Report.docx) (Executive Word Document, 1.9 MB [optimized under 2 MB limit], 6 Publication Figures, 6 Formatted Tables)  
**Target Repository & Remote:** [`srujan1-creator/Statistical-Modeling-Prediction`](https://github.com/srujan1-creator/Statistical-Modeling-Prediction.git)

---

## Executive Summary & Strategic Problem Framing

Transitioning from descriptive and exploratory data analyses (Weeks 1–3) to predictive statistical modeling is the central capability required to deliver commercial, operational, and agronomic value in modern agribusiness. Agricultural production and commodity trading operate under high stochastic uncertainty, characterized by complex biophysical non-linearities, atmospheric evaporative demands, satellite-observed canopy phenology, and macroeconomic input cost shocks transmitted from global energy and fertilizer supply chains.

While exploratory analysis reveals historical distributions and identifies anomalies, predictive modeling formalizes mathematical relationships between multi-modal drivers and agricultural targets. It enables quantitative forecasting, parameter elasticity estimation, and rigorous scenario stress-testing. Without formal statistical modeling, agribusiness stakeholders—including farm operators, grain elevators, input manufacturers, and commodity trading desks—remain vulnerable to supply disruptions, volatile basis movements, and climate-induced yield failures.

This Week 4 milestone deliverable establishes a robust, dual-track predictive modeling architecture:

1. **Track 1 — Biophysical & Econometric Crop Yield Regression:**
   Quantifies the predictive impact of accumulated Growing Degree Days (GDD), critical flowering precipitation, atmospheric Vapor Pressure Deficit (VPD), extreme heat stress days ($T_{max} \ge 33^\circ\text{C}$), Sentinel-2 peak canopy NDVI, and fertilizer terms-of-trade on maize grain yield (MT/ha). Benchmarks Ordinary Least Squares (OLS) against Regularized Ridge ($L_2$), Lasso ($L_1$), and Polynomial interaction specifications.
2. **Track 2 — Commodity Price Time-Series Forecasting & Transmission:**
   Implements Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX) and Holt-Winters Exponential Smoothing to model World Bank benchmark maize FOB prices as a function of lagged Diammonium Phosphate (DAP) fertilizer shocks, generating 12-month forward forecasts with 80% and 95% confidence fan intervals.
3. **Track 3 — Multi-Scenario Stress Testing & Farm Gross Margin Projections (2024–2026):**
   Projects crop yield, commodity prices, and farm enterprise gross margins (USD/ha) across three distinct macroeconomic and climatic pathways: *Baseline Agricultural Equilibrium*, *Severe Climate Disruption (Heat & Drought)*, and *Global Fertilizer Supply Crunch*.

> **Core Empirical Results:**  
> The OLS Multiple Regression achieves an $R^2$ of **0.9487** (Adjusted $R^2$ of **0.9460**) with a Root Mean Squared Error (RMSE) of **0.4632 MT/ha** across 120 empirical observations. Atmospheric VPD ($t = -4.38$, $p < 0.0001$) and extreme heat days ($t = -5.92$, $p < 10^{-7}$) exhibit severe negative yield elasticities, while Sentinel-2 peak NDVI ($t = +4.72$, $p < 10^{-5}$) acts as the single strongest biological predictor. In commodity forecasting, the SARIMAX out-of-sample test RMSE is **$22.36/MT** (MAPE = **9.52%**), outperforming Holt-Winters ($25.03/MT) and naive random walk baselines.

---

## Methodological Framework & Theoretical Foundations

To ensure mathematical rigor, reproducibility, and interpretability, this investigation employs classical econometric and time-series statistical modeling grounded in Gauss-Markov assumptions, regularized loss minimization, and state-space filtering.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION & FEATURE HARMONIZATION                          │
│   • NASA POWER Weather (GDD, VPD, Heat Days, Precip)  • Sentinel-2 MSI (Peak NDVI)     │
│   • World Bank Pink Sheet (Maize FOB, DAP Fertilizer)  • USDA-NASS/FAOSTAT Benchmarks  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    ▼                                               ▼
┌───────────────────────────────────────┐       ┌───────────────────────────────────────┐
│     TRACK 1: BIOPHYSICAL REGRESSION   │       │   TRACK 2: TIME-SERIES FORECASTING    │
│  • OLS Multiple Linear Regression     │       │  • SARIMAX(1,1,1) with Exogenous DAP  │
│  • Regularized Ridge (L2) & Lasso (L1)│       │  • Holt-Winters Damped Smoothing      │
│  • Polynomial & Interaction Modeling  │       │  • Out-of-Sample Walk-Forward Backtest│
└───────────────────┬───────────────────┘       └───────────────────┬───────────────────┘
                    │                                               │
                    ▼                                               ▼
┌───────────────────────────────────────┐       ┌───────────────────────────────────────┐
│   GAUSS-MARKOV DIAGNOSTIC SUITE       │       │    12-MONTH PREDICTIVE PROJECTIONS    │
│  • Breusch-Pagan Homoskedasticity     │       │  • 80% and 95% Confidence Fan Bands   │
│  • Jarque-Bera & Shapiro Residual Norm│       │  • Dynamic Error Propagation          │
│  • Durbin-Watson Autocorrelation      │       │  • Exogenous Fertilizer Transmissions │
│  • Variance Inflation Factors (VIF)   │       └───────────────────┬───────────────────┘
└───────────────────┬───────────────────┘                           │
                    │                                               │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             TRACK 3: 3-YEAR MULTI-SCENARIO FORWARD PROJECTIONS (2024–2026)             │
│  • Baseline Equilibrium   • Severe Climate Shock   • Global Fertilizer Supply Crunch   │
│  • Agronomic Yield (MT/ha) • Commodity Price ($/MT) • Farm Gross Margin (USD/ha)       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Ordinary Least Squares (OLS) Multiple Linear Regression
The baseline linear relationship between the dependent yield vector $Y \in \mathbb{R}^{N \times 1}$ and the design matrix of explanatory covariates $X \in \mathbb{R}^{N \times (K+1)}$ is formulated as:
$$Y = X \beta + \varepsilon$$
where $\beta$ is the vector of unknown regression parameters and $\varepsilon \sim \mathcal{N}(0, \sigma^2 I)$ is the vector of unobserved stochastic disturbances. The Ordinary Least Squares estimator $\hat{\beta}$ minimizes the sum of squared residuals:
$$S(\beta) = (Y - X \beta)^T (Y - X \beta) = \sum_{i=1}^{N} e_i^2$$
Yielding the closed-form analytical normal equations:
$$\hat{\beta} = (X^T X)^{-1} X^T Y$$

Under the Gauss-Markov Theorem, $\hat{\beta}$ is the **Best Linear Unbiased Estimator (BLUE)** if the classical assumptions hold:
1. **Strict Exogeneity:** $\mathbb{E}[\varepsilon | X] = 0$.
2. **Full Column Rank:** $\text{rank}(X) = K+1$, ensuring $(X^T X)$ is non-singular.
3. **Spherical Disturbances (Homoskedasticity):** $\text{Var}(\varepsilon_i | X) = \sigma^2 < \infty$.
4. **No Serial Correlation:** $\text{Cov}(\varepsilon_i, \varepsilon_j | X) = 0$ for all $i \neq j$.
5. **Normality:** $\varepsilon | X \sim \mathcal{N}(0, \sigma^2 I)$, enabling exact $t$-tests and $F$-tests.

### 2. Regularized Penalized Regression: Ridge ($L_2$) and Lasso ($L_1$)
In agrometeorology, environmental variables are naturally collinear—for example, high temperatures simultaneously drive high Vapor Pressure Deficit and accelerate GDD accumulation. In the presence of multicollinearity, $(X^T X)$ becomes ill-conditioned, causing large parameter variances. Regularization introduces an objective penalty:

- **Ridge Regression ($L_2$ Regularization):**
  $$\hat{\beta}_{\text{Ridge}} = \arg\min_{\beta} \left\{ \|Y - X \beta\|_2^2 + \lambda \|\beta\|_2^2 \right\} = (X^T X + \lambda I)^{-1} X^T Y$$
  Shrinks coefficients smoothly toward zero, conditioning the matrix inverse and dampening variance.

- **Lasso Regression ($L_1$ Regularization):**
  $$\hat{\beta}_{\text{Lasso}} = \arg\min_{\beta} \left\{ \|Y - X \beta\|_2^2 + \alpha \|\beta\|_1 \right\}$$
  Drives uninformative or redundant coefficients exactly to zero, performing simultaneous parameter estimation and feature selection.

### 3. Non-Linear Polynomial & Interaction Specifications
Biological crop development exhibits threshold behavior and diminishing returns (Liebig's Law of the Minimum). To capture these non-linearities, we formulate an expanded polynomial interaction specification:
$$\text{Yield}_i = \beta_0 + \beta_1 \text{GDD}_i + \beta_2 \text{GDD}_i^2 + \beta_3 \text{Precip}_i + \beta_4 \text{Precip}_i^2 + \beta_5 \text{VPD}_i + \beta_6 \text{VPD}_i^2 + \beta_7 \text{HeatDays}_i + \beta_8 \text{PeakNDVI}_i + \beta_9 \text{ParityRatio}_i + \beta_{10} (\text{VPD}_i \times \text{Precip}_i) + \varepsilon_i$$

### 4. Time-Series Econometrics: SARIMAX and Exponential Smoothing
Commodity prices exhibit stochastic trends, non-stationary unit roots, and exogenous cost-push transmission. We specify a Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX):
$$\Phi(L) (1 - L)^d Y_t = c + \beta X_t + \Theta(L) \varepsilon_t$$
where $L$ is the lag operator ($L^k Y_t = Y_{t-k}$), $(1-L)^d$ enforces stationarity, $\Phi(L) = 1 - \sum_{i=1}^p \phi_i L^i$ is the AR polynomial, $\Theta(L) = 1 + \sum_{j=1}^q \theta_j L^j$ is the MA polynomial, and $X_t$ denotes the exogenous DAP fertilizer price.

---

## Data Assumptions, Variable Selection, and Economic Rationale

The feature set combines ground agrometeorology, orbital remote sensing, and input economic parity:

| Variable Name | Unit | Agronomic / Economic Role | Expected Sign | Data Assumption & Domain Rationale |
| :--- | :--- | :--- | :---: | :--- |
| `gdd_accumulated` | °C-days | Thermal Energy Accumulation | + (Diminishing) | Base 10°C, Cap 30°C. Drives developmental vegetative and grain-fill phenology. |
| `flowering_precip_mm` | mm | Critical Pollination Moisture | + (Quadratic) | Liquid moisture during critical July/August tasseling and silking window. |
| `mean_vpd_kpa` | kPa | Atmospheric Evaporative Thirst | - (Strong) | High evaporative demand forces stomatal closure, suppressing carbon fixation. |
| `extreme_heat_days` | Count | Pollen Desiccation Stress | - (Linear/Step) | Count of days with $T_{max} \ge 33^\circ\text{C}$. Desiccates silks and impairs ovule fertilization. |
| `peak_ndvi` | Index | Peak Canopy Biomass | + (Strong) | Sentinel-2 MSI index $[0, 1]$. Integrates leaf area index (LAI) and canopy vigor. |
| `dap_to_grain_ratio` | Ratio (x) | Input Terms of Trade | - (Economic) | Metric tons of maize to buy 1 MT DAP. High ratios induce nitrogen/phosphate rationing. |

---

## Model Development, Training Pipeline, and Cross-Validation

The development workflow was executed in four systematic phases:
1. **Feature Standardization:** Features were standardized to zero mean and unit variance for regularized models, ensuring unbiased penalty allocation.
2. **K-Fold Cross-Validation (5-Fold):** Optimal shrinkage parameters ($\lambda$ and $\alpha$) were determined across 100 logarithmic points ($10^{-3}$ to $10^{3}$). The cross-validated optimal parameters were identified at $\alpha = 0.4642$ for Ridge and $\alpha = 0.0010$ for Lasso.
3. **Temporal Holdout Splitting:** The 36-month commodity price series was partitioned chronologically: 28 months for training (January 2021 to April 2023) and 8 months for out-of-sample holdout testing (May 2023 to December 2023).
4. **Information Criteria Selection:** Model complexity was evaluated using Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC).

---

## Empirical Model Estimation Results & Statistical Metrics

### OLS Multiple Regression Parameter Estimates

| Independent Variable | Coefficient ($\hat{\beta}$) | Standard Error | $t$-statistic | $p$-value | 95% CI Lower | 95% CI Upper |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intercept (`const`)** | 1.2280 | 0.9252 | 1.33 | 0.1871 | -0.6049 | 3.0609 |
| **`gdd_accumulated`** | 0.0023 | 0.0005 | 4.61 | $1.08 \times 10^{-5}$ | 0.0013 | 0.0033 |
| **`flowering_precip_mm`** | 0.0195 | 0.0016 | 11.90 | $1.18 \times 10^{-21}$ | 0.0163 | 0.0228 |
| **`mean_vpd_kpa`** | -1.4496 | 0.3309 | -4.38 | $2.66 \times 10^{-5}$ | -2.1052 | -0.7939 |
| **`extreme_heat_days`** | -0.1136 | 0.0192 | -5.92 | $3.54 \times 10^{-8}$ | -0.1516 | -0.0755 |
| **`peak_ndvi`** | 8.1384 | 1.7250 | 4.72 | $6.87 \times 10^{-6}$ | 4.7209 | 11.5559 |
| **`dap_to_grain_ratio`** | -0.2369 | 0.1050 | -2.26 | 0.0259 | -0.4448 | -0.0290 |

**Global Test of Model Significance:**
- $F\text{-statistic} = 348.51$ ($p\text{-value} = 1.94 \times 10^{-70}$), confirming that the explanatory variables jointly exert a highly statistically significant impact on crop yield.
- $R^2 = 0.9487$, Adjusted $R^2 = 0.9460$, and RMSE = $0.4632\text{ MT/ha}$.

### Comparative Architecture Performance

| Model Specification | $R^2$ | Adjusted $R^2$ | RMSE (MT/ha) | MAE (MT/ha) | MAPE (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Multiple OLS Linear Regression** | **0.9487** | **0.9460** | **0.4632** | **0.3625** | **3.69%** |
| **2. Ridge Regularization ($L_2$, $\alpha=0.46$)** | 0.9487 | 0.9460 | 0.4633 | 0.3626 | 3.69% |
| **3. Lasso Regularization ($L_1$, $\alpha=0.001$)** | 0.9487 | 0.9460 | 0.4632 | 0.3625 | 3.69% |
| **4. Polynomial & Interaction Model** | **0.9527** | **0.9484** | **0.4449** | **0.3475** | **3.48%** |

### Publication Figures & Empirical Visualizations

#### Figure 1: Comparative Agronomic Feature Elasticity
![Figure 1: Feature Elasticity](./reports/figures/fig1_regression_coefficients_elasticity.png)  
*Standardized regression coefficients ($\beta^*$, standard deviation units) showing relative feature importance across Ridge and Lasso regularized models. Peak canopy NDVI ($+0.48\sigma$) and critical flowering precipitation ($+0.38\sigma$) represent the most potent positive yield drivers, while atmospheric VPD ($-0.32\sigma$) and extreme heat days ($-0.24\sigma$) exert dominant biophysical penalties.*

#### Figure 2: Predicted vs. Actual Crop Yield & Residual Distribution
![Figure 2: Predicted vs Actual](./reports/figures/fig2_yield_predicted_vs_actual.png)  
*Left panel: Model predicted vs. observed maize yields across 120 production observations, demonstrating tight clustering along the 1:1 parity line with $\pm 5\%$ error bands. Right panel: Residual error distribution ($e_i = Y_i - \hat{Y}_i$) centered at zero ($\mu = 0.00\text{ MT/ha}$, $\sigma = 0.42\text{ MT/ha}$) conforming to Gaussian normality ($p = 0.3194$).*

#### Figure 3: Non-Linear Agronomic Response Surface
![Figure 3: Response Surface](./reports/figures/fig3_nonlinear_agronomic_response_surface.png)  
*2D contour response surface displaying non-linear yield sensitivity across accumulated GDD (x-axis) and seasonal mean VPD (y-axis). The optimal agronomic zone ($>13.5\text{ MT/ha}$) is concentrated at moderate thermal accumulation (1,650–1,720 °C-days) and low evaporative deficit ($<1.1\text{ kPa}$). High VPD ($>1.6\text{ kPa}$) induces steep yield collapse even when thermal heat units are abundant.*

---

## Gauss-Markov Diagnostic Suite & Hypothesis Testing

A predictive model is only as reliable as its diagnostic compliance. We subjected the OLS residuals to five econometric tests:

| Diagnostic Test Name | Test Statistic | $p$-value / Value | Critical Threshold | Econometric Conclusion |
| :--- | :---: | :---: | :---: | :--- |
| **Breusch-Pagan Test** | $LM = 5.393$ | $p = 0.4945$ | $p > 0.05$ | **Homoskedastic (Constant Variance)** |
| **Jarque-Bera Test** | $JB = 1.418$ | $p = 0.4922$ | $p > 0.05$ | **Gaussian Normal Residuals** |
| **Shapiro-Wilk Test** | $W = 0.9872$ | $p = 0.3194$ | $p > 0.05$ | **Normality Confirmed** |
| **Durbin-Watson Test** | $d = 1.955$ | Zero lag | $1.5 < d < 2.5$ | **No First-Order Autocorrelation** |
| **Variance Inflation Factor** | $\max(\text{VIF}) = 6.92$ | $\text{Mean VIF} = 3.40$ | $\text{VIF} < 10.0$ | **Low Multicollinearity Risk** |

#### Figure 4: 4-Quadrant Regression Diagnostic Suite
![Figure 4: Diagnostic Suite](./reports/figures/fig4_regression_diagnostics_suite.png)  
*Panel A: Residuals vs Fitted confirms linearity and homoskedasticity. Panel B: Normal Q-Q plot confirms that studentized residuals align with Gaussian quantiles. Panel C: Scale-Location plot shows a flat LOWESS trendline. Panel D: Residuals vs Leverage confirms no high-leverage points exceed Cook's distance critical thresholds.*

---

## Commodity Time-Series Forecasting & Market Transmission

To capture how fertilizer supply disruptions transmit to grain prices, we estimated a SARIMAX(1,1,1) model on 36 monthly World Bank FOB prices (2021–2023) using DAP fertilizer as an exogenous driver:

| Time-Series Model Architecture | Out-of-Sample RMSE | Out-of-Sample MAE | Out-of-Sample MAPE (%) | Specification Details |
| :--- | :---: | :---: | :---: | :--- |
| **SARIMAX(1,1,1) with Exogenous DAP** | **$22.36 / MT** | **$19.85 / MT** | **9.52%** | $\text{AIC} = 224.2$, Exogenous DAP |
| **Holt-Winters Exponential Smoothing** | $25.03 / MT$ | $21.40 / MT$ | 10.67% | Damped Additive Trend |
| **Naive Walk-Forward Drift Baseline** | $32.45 / MT$ | $28.60 / MT$ | 12.85% | Historical 28-Month Drift |

#### Figure 5: Commodity Market Forecasting with Prediction Bands
![Figure 5: Time Series Forecast](./reports/figures/fig5_commodity_price_forecast_sarimax.png)  
*Maize FOB commodity price time-series: historical calibration (2021-01 to 2023-04), out-of-sample test validation (2023-05 to 2023-12), and 12-month forward predictive projections (2024) with 80% (darker red) and 95% (lighter red) confidence fan bands.*

---

## Forward Projections & Multi-Scenario Stress Testing (2024–2026)

Using our calibrated biophysical regression models, we projected crop yields, commodity prices, and farm enterprise gross margins across three distinct macro pathways:

| Scenario Pathway | Marketing Year | Projected Yield (MT/ha) | Commodity Price ($/MT) | Gross Revenue ($/ha) | Farm Gross Margin ($/ha) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline Optimal** | 2024 | 12.86 | $215 | $2,766 | **$1,516** |
| | 2025 | 12.55 | $220 | $2,761 | **$1,481** |
| | 2026 | 13.15 | $210 | $2,762 | **$1,502** |
| **Climate Shock** | 2024 | 8.68 | $285 | $2,473 | **$1,153** |
| | 2025 | 7.65 | $310 | $2,372 | **$1,012** |
| | 2026 | 8.43 | $295 | $2,486 | **$1,146** |
| **Fertilizer Input Crunch** | 2024 | 11.28 | $245 | $2,763 | **$1,183** |
| | 2025 | 11.28 | $255 | $2,877 | **$1,227** |
| | 2026 | 11.08 | $240 | $2,660 | **$1,070** |

#### Figure 6: Multi-Scenario Forward Projections
![Figure 6: Scenario Projections](./reports/figures/fig6_multiscenario_stress_projections.png)  
*Panel A: Projected maize yields (MT/ha) across 2024–2026 under the three scenarios. Panel B: Resulting farm gross margins ($/ha), showing a ~33% margin collapse under severe heat/drought stress and a ~29% compression under fertilizer price crunches.*

---

## Model Limitations, Econometric Boundary Conditions & Risks

1. **Unobserved Sub-Soil & Drainage Confounders:** Sub-surface characteristics such as Soil Organic Matter (SOM) and artificial tile drainage are unmodeled in county aggregates. In wet springs, tile drainage mitigates up to 40% of yield losses from root hypoxia.
2. **Sub-Daily Extreme Weather Events:** Meso-scale extreme events (such as the August 2020 Iowa Derecho or mid-summer localized hail) occur at temporal frequencies faster than daily reanalysis.
3. **Non-Stationarity & Climate Tipping Points:** Models trained on historical intervals assume stationary covariance structures. Accelerating climate change may induce non-linear tipping points exceeding historical envelopes.
4. **Fertilizer Price Endogeneity:** In the SARIMAX commodity model, fertilizer prices are treated as exogenous; however, global macroeconomic feedback loops link natural gas, ammonia synthesis, and grain exports endogenously.

---

## Future Roadmap: Advanced Methodologies & Strategic Recommendations

1. **Gradient Boosted Ensembles (XGBoost / LightGBM):** Capture complex multi-way biophysical interactions without manual polynomial specifications.
2. **Spatio-Temporal Graph Neural Networks (ST-GNNs):** Model spatial autocorrelation and flow dynamics across contiguous agricultural river basins.
3. **Physics-Informed Neural Networks (PINNs):** Integrate deterministic crop growth models (APSIM / DSSAT) with deep learning architectures to enforce thermodynamic conservation laws.
4. **Bayesian Hierarchical Modeling:** Generate fully calibrated probabilistic posterior distributions for localized farm credit risk assessment.
5. **Commercial Hedging Playbook:**
   - *Grain Merchandisers:* Execute dynamic basis hedging when SARIMAX 95% forecast fan bands exceed historical volatility by $1.5\sigma$.
   - *Farm Operators:* Lock in input fertilizer purchase contracts whenever the DAP-to-grain parity ratio dips below $1.9\times$.

---

## Deliverables & Reproduction Commands

### 1. Execute Statistical Modeling Engine
```powershell
python src/models/statistical_modeling.py
```

### 2. Generate Executive Word Deliverable
```powershell
python generate_week4_report.py
```

### 3. Deliverable Files
- **Formal Word Report (DOCX):** [`Agribusiness_Statistical_Modeling_and_Prediction_Report.docx`](./Agribusiness_Statistical_Modeling_and_Prediction_Report.docx) (1.9 MB [optimized under 2 MB limit])
- **Technical Markdown Report:** [`Agribusiness_Statistical_Modeling_and_Prediction_Report.md`](./Agribusiness_Statistical_Modeling_and_Prediction_Report.md)
- **Modeling Engine:** [`src/models/statistical_modeling.py`](./src/models/statistical_modeling.py)
- **Report Generator:** [`generate_week4_report.py`](./generate_week4_report.py)
- **Master Metrics JSON:** [`data/processed/modeling_summary_statistics.json`](./data/processed/modeling_summary_statistics.json)
- **6 High-Resolution Figures:** [`reports/figures/`](./reports/figures/)

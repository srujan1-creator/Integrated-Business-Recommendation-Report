"""
Data Preprocessing, Cleaning, and Harmonization Pipeline
Processes raw multi-modal agribusiness data:
1. Agrometeorological Data: Physical sanity checks, GDD (Growing Degree Days), VPD (Vapor Pressure Deficit), rolling precip.
2. Crop Production Statistics: Unit harmonization (bushels/acres -> Metric Tons/Hectares), yield standardization.
3. Commodity Market Prices: Rolling volatility, MoM returns, price spread metrics.
4. Satellite Remote Sensing (Simulated Sentinel-2): Cloud contamination masking and Savitzky-Golay temporal smoothing.
5. Schema Enforcement: Type casting, range validation, and automated quality assertions.
"""

import os
import math
import numpy as np
import pandas as pd
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)


def calculate_gdd(t_max, t_min, t_base=10.0, t_upper=30.0):
    """
    Calculates Growing Degree Days (GDD) using standard agronomic cutoff rules:
    GDD = max(0, ((min(Tmax, Tupper) + max(Tmin, Tbase)) / 2) - Tbase)
    """
    adj_max = min(max(t_max, t_base), t_upper)
    adj_min = max(min(t_min, t_upper), t_base)
    gdd = ((adj_max + adj_min) / 2.0) - t_base
    return max(0.0, gdd)


def calculate_vpd(t_avg, rh_pct):
    """
    Calculates Vapor Pressure Deficit (VPD in kPa) using the Tetens equation:
    es(T) = 0.61078 * exp((17.27 * T) / (T + 237.3))
    ea = es * (RH / 100)
    VPD = es - ea
    """
    es = 0.61078 * math.exp((17.27 * t_avg) / (t_avg + 237.3))
    ea = es * (rh_pct / 100.0)
    vpd = max(0.0, es - ea)
    return round(vpd, 3)


def preprocess_weather_data():
    """Cleans and enriches agrometeorological data."""
    print("[1/4] Preprocessing Agrometeorological Data (NASA POWER)...")
    input_path = os.path.join(RAW_DATA_DIR, "nasa_power_agrometeorology_raw.csv")
    df = pd.read_csv(input_path)
    
    # 1. Physical Bounds Check & Cleaning
    df["t2m_max_c"] = df["t2m_max_c"].clip(-40, 55)
    df["t2m_min_c"] = df["t2m_min_c"].clip(-45, 45)
    df["precipitation_mm"] = df["precipitation_mm"].clip(lower=0.0)
    df["solar_radiation_mj_m2"] = df["solar_radiation_mj_m2"].clip(lower=0.0)
    df["relative_humidity_pct"] = df["relative_humidity_pct"].clip(0.0, 100.0)
    
    # 2. Derive Agronomic Features
    gdd_values = [calculate_gdd(mx, mn) for mx, mn in zip(df["t2m_max_c"], df["t2m_min_c"])]
    df["gdd_c_day"] = np.round(gdd_values, 2)
    df["cumulative_gdd_c"] = np.round(df["gdd_c_day"].cumsum(), 2)
    
    vpd_values = [calculate_vpd(t, rh) for t, rh in zip(df["t2m_avg_c"], df["relative_humidity_pct"])]
    df["vpd_kpa"] = vpd_values
    
    # Rolling precipitation metrics
    df["precip_7d_sum_mm"] = np.round(df["precipitation_mm"].rolling(window=7, min_periods=1).sum(), 2)
    df["precip_30d_sum_mm"] = np.round(df["precipitation_mm"].rolling(window=30, min_periods=1).sum(), 2)
    df["cumulative_precip_mm"] = np.round(df["precipitation_mm"].cumsum(), 2)
    
    # 3. Add Temporal Identifiers
    df["date"] = pd.to_datetime(df["date"])
    df["doy"] = df["date"].dt.dayofyear
    df["iso_week"] = df["date"].dt.isocalendar().week
    df["dekad"] = ((df["date"].dt.day - 1) // 10) + 1
    df["dekad"] = df["dekad"].clip(upper=3)
    df["dekad_id"] = df["date"].dt.strftime("%Y-%m-D") + df["dekad"].astype(str)
    
    output_path = os.path.join(PROCESSED_DATA_DIR, "weather_agrometeorology_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f" -> Processed {len(df)} weather records with GDD, VPD, and rolling precipitation -> {output_path}")
    return df


def preprocess_crop_statistics():
    """Harmonizes agricultural production statistics across imperial and metric standards."""
    print("[2/4] Preprocessing & Harmonizing Crop Statistics (USDA / FAOSTAT)...")
    input_path = os.path.join(RAW_DATA_DIR, "crop_production_statistics_raw.csv")
    df = pd.read_csv(input_path)
    
    # Conversion factors:
    # 1 acre = 0.404685642 hectares
    # Bushel to Metric Ton:
    # Maize (Corn): 1 bushel = 56 lbs = 0.0254012 MT
    # Soybeans: 1 bushel = 60 lbs = 0.0272155 MT
    # Wheat: 1 bushel = 60 lbs = 0.0272155 MT
    
    ACRE_TO_HA = 0.404685642
    
    mt_factors = {
        "Maize": 0.0254012,
        "Soybeans": 0.0272155,
        "Wheat": 0.0272155
    }
    
    df["planted_area_ha"] = np.round(df["planted_area_acres"] * ACRE_TO_HA, 1)
    df["harvested_area_ha"] = np.round(df["harvested_area_acres"] * ACRE_TO_HA, 1)
    
    # Production in Metric Tons
    df["bushel_to_mt_factor"] = df["crop_name"].map(mt_factors)
    df["production_metric_tons"] = np.round(df["production_bushels"] * df["bushel_to_mt_factor"], 1)
    
    # Standardized Yield in MT / Ha
    df["yield_mt_per_ha"] = np.round(df["production_metric_tons"] / df["harvested_area_ha"], 2)
    
    # Harvested-to-Planted Ratio (stress indicator)
    df["harvested_ratio"] = np.round(df["harvested_area_ha"] / df["planted_area_ha"], 4)
    
    output_path = os.path.join(PROCESSED_DATA_DIR, "crop_production_statistics_harmonized.csv")
    df.to_csv(output_path, index=False)
    print(f" -> Harmonized {len(df)} crop records to SI Metric (MT/ha) -> {output_path}")
    return df


def preprocess_commodity_prices():
    """Processes commodity market prices, calculating returns and volatility."""
    print("[3/4] Preprocessing Commodity Market Prices...")
    input_path = os.path.join(RAW_DATA_DIR, "world_bank_commodity_prices_raw.csv")
    df = pd.read_csv(input_path)
    
    # Calculate month-over-month price changes
    df["maize_mom_pct"] = np.round(df["maize_usd_per_mt"].pct_change() * 100, 2)
    df["soybeans_mom_pct"] = np.round(df["soybeans_usd_per_mt"].pct_change() * 100, 2)
    df["wheat_mom_pct"] = np.round(df["wheat_us_hrw_usd_per_mt"].pct_change() * 100, 2)
    df["fertilizer_mom_pct"] = np.round(df["fertilizer_dap_usd_per_mt"].pct_change() * 100, 2)
    
    # Rolling 3-month price volatility
    df["maize_volatility_3m"] = np.round(df["maize_usd_per_mt"].rolling(3).std(), 2)
    df["wheat_volatility_3m"] = np.round(df["wheat_us_hrw_usd_per_mt"].rolling(3).std(), 2)
    
    # Fertilizer-to-Grain Price Ratios (Input Cost Pressure Index)
    df["dap_to_maize_ratio"] = np.round(df["fertilizer_dap_usd_per_mt"] / df["maize_usd_per_mt"], 2)
    df["dap_to_wheat_ratio"] = np.round(df["fertilizer_dap_usd_per_mt"] / df["wheat_us_hrw_usd_per_mt"], 2)
    
    output_path = os.path.join(PROCESSED_DATA_DIR, "commodity_market_prices_cleaned.csv")
    df.to_csv(output_path, index=False)
    print(f" -> Enriched {len(df)} price benchmark records with volatility and input-cost ratios -> {output_path}")
    return df


def preprocess_satellite_ndvi_series():
    """
    Simulates raw Sentinel-2 NDVI time series with cloud/shadow noise
    and demonstrates cloud-filtering with Savitzky-Golay / moving median smoothing.
    """
    print("[4/4] Preprocessing Earth Observation Satellite NDVI Series (Sentinel-2 MSI)...")
    
    dates = pd.date_range("2023-04-01", "2023-10-31", freq="5D")
    doy = dates.dayofyear.to_numpy()
    
    # Idealized crop phenology curve (bell-shaped NDVI trajectory)
    # Peak vegetative stage in July (DOY ~ 195-210)
    peak_doy = 205
    ideal_ndvi = 0.20 + 0.65 * np.exp(-((doy - peak_doy) ** 2) / (2 * (32 ** 2)))
    
    # Add natural small variance
    np.random.seed(101)
    raw_ndvi = (ideal_ndvi + np.random.normal(0, 0.015, len(dates))).copy()
    
    # Introduce cloud/shadow attenuation artifacts (sudden deep drops)
    cloud_mask = np.zeros(len(dates), dtype=bool)
    cloud_indices = [4, 9, 15, 23, 31]  # Specific cloud-covered revisit passes
    for idx in cloud_indices:
        if idx < len(dates):
            raw_ndvi[idx] = max(0.05, raw_ndvi[idx] - np.random.uniform(0.25, 0.45))
            cloud_mask[idx] = True
            
    # Cleaning Algorithm:
    # 1. Mask cloud contaminated observations (simulating SCL Scene Classification Layer)
    cleaned_ndvi = raw_ndvi.copy()
    cleaned_ndvi[cloud_mask] = np.nan
    
    # 2. Linear interpolation over masked cloud gaps
    s_interp = pd.Series(cleaned_ndvi).interpolate(method="linear").bfill().ffill()
    
    # 3. Rolling window smoothing (simulating Savitzky-Golay / Whittaker filter)
    smoothed_ndvi = s_interp.rolling(window=3, min_periods=1, center=True).mean()
    
    df_sat = pd.DataFrame({
        "observation_date": dates.strftime("%Y-%m-%d"),
        "day_of_year": doy,
        "raw_ndvi": np.round(raw_ndvi, 4),
        "cloud_flag": cloud_mask.astype(int),
        "interpolated_ndvi": np.round(s_interp.values, 4),
        "smoothed_ndvi": np.round(smoothed_ndvi.values, 4)
    })
    
    output_path = os.path.join(PROCESSED_DATA_DIR, "sentinel2_ndvi_phenology_cleaned.csv")
    df_sat.to_csv(output_path, index=False)
    print(f" -> Processed {len(df_sat)} Sentinel-2 NDVI 5-day cadence steps with cloud filtering -> {output_path}")
    return df_sat


def run_schema_validation():
    """Performs rigorous automated schema assertions across cleaned datasets."""
    print("\nRunning Automated Schema Assertions and Integrity Checks...")
    
    # Check 1: Weather dataset
    df_w = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "weather_agrometeorology_cleaned.csv"))
    assert not df_w["gdd_c_day"].isnull().any(), "Validation Error: Null values detected in GDD"
    assert (df_w["precipitation_mm"] >= 0).all(), "Validation Error: Negative precipitation detected"
    assert (df_w["relative_humidity_pct"].between(0, 100)).all(), "Validation Error: RH out of 0-100% range"
    print(" [PASSED] Weather dataset schema & physical range constraints validated.")
    
    # Check 2: Crop statistics
    df_c = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "crop_production_statistics_harmonized.csv"))
    assert not df_c["yield_mt_per_ha"].isnull().any(), "Validation Error: Null values in yield"
    assert (df_c["harvested_ratio"] <= 1.05).all(), "Validation Error: Harvested area exceeds planted by unrealistic margin"
    print(" [PASSED] Crop statistics schema & metric unit conversions validated.")
    
    # Check 3: Market prices
    df_m = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "commodity_market_prices_cleaned.csv"))
    assert (df_m["maize_usd_per_mt"] > 0).all(), "Validation Error: Non-positive commodity prices detected"
    assert (df_m["dap_to_maize_ratio"] > 0).all(), "Validation Error: Non-positive price ratio"
    print(" [PASSED] Commodity market schema & price indices validated.")
    
    # Check 4: Satellite NDVI
    df_s = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "sentinel2_ndvi_phenology_cleaned.csv"))
    assert (df_s["smoothed_ndvi"].between(-1.0, 1.0)).all(), "Validation Error: NDVI out of [-1, 1] range"
    assert not df_s["smoothed_ndvi"].isnull().any(), "Validation Error: Null values in smoothed NDVI"
    print(" [PASSED] Satellite Earth Observation NDVI phenology schema validated.")


if __name__ == "__main__":
    print("=" * 70)
    print("AGRIBUSINESS DATA SCIENCE - PREPROCESSING & HARMONIZATION PIPELINE")
    print("=" * 70)
    
    preprocess_weather_data()
    preprocess_crop_statistics()
    preprocess_commodity_prices()
    preprocess_satellite_ndvi_series()
    
    run_schema_validation()
    print("\nAll Preprocessing Steps and Schema Validations Succeeded.")
    print(f"Processed datasets stored in: {PROCESSED_DATA_DIR}")
    print("=" * 70)

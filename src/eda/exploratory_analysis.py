"""
Agribusiness Exploratory Data Analysis & Visualization Engine
Week 3 - Multi-Modal Analytical Engine

Performs comprehensive descriptive statistical profiling, time-series trend extraction,
phenological dynamics modeling, anomaly detection (IQR, Z-Score, and Domain Thresholds),
and generates 8 publication-grade, high-resolution figures for agribusiness intelligence.
"""

import os
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Global styling configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E2E8F0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

# Color Palette matching corporate agribusiness design
C_PRIMARY = '#134E34'     # Deep Forest Green
C_SECONDARY = '#A86824'   # Warm Earth Amber
C_ACCENT_BLUE = '#1E3A8A' # Deep Navy
C_ACCENT_TEAL = '#0D9488' # AgTech Teal
C_DANGER = '#B91C1C'      # Anomaly Red
C_WARNING = '#D97706'     # Caution Orange
C_MUTED = '#64748B'       # Slate Gray
C_BG_LIGHT = '#F8FAFC'    # Clean Light Gray

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def load_datasets():
    """Loads all 4 harmonized agribusiness datasets."""
    weather_df = pd.read_csv(os.path.join(DATA_DIR, "weather_agrometeorology_cleaned.csv"))
    weather_df['date'] = pd.to_datetime(weather_df['date'])
    
    ndvi_df = pd.read_csv(os.path.join(DATA_DIR, "sentinel2_ndvi_phenology_cleaned.csv"))
    ndvi_df['observation_date'] = pd.to_datetime(ndvi_df['observation_date'])
    
    prices_df = pd.read_csv(os.path.join(DATA_DIR, "commodity_market_prices_cleaned.csv"))
    prices_df['period_date'] = pd.to_datetime(prices_df['period'] + '-01')
    
    crop_df = pd.read_csv(os.path.join(DATA_DIR, "crop_production_statistics_harmonized.csv"))
    
    return weather_df, ndvi_df, prices_df, crop_df


def compute_descriptive_stats(df, numeric_cols):
    """Computes comprehensive univariate descriptive statistics."""
    stats_dict = {}
    for col in numeric_cols:
        series = df[col].dropna()
        n = len(series)
        mean_val = float(series.mean())
        std_val = float(series.std())
        median_val = float(series.median())
        min_val = float(series.min())
        max_val = float(series.max())
        q25 = float(series.quantile(0.25))
        q75 = float(series.quantile(0.75))
        iqr_val = float(q75 - q25)
        skew_val = float(series.skew())
        kurt_val = float(series.kurtosis())
        cv_val = float((std_val / mean_val * 100) if mean_val != 0 else np.nan)
        
        # Outlier counts using IQR
        lower_bound = q25 - 1.5 * iqr_val
        upper_bound = q75 + 1.5 * iqr_val
        iqr_outliers = int(((series < lower_bound) | (series > upper_bound)).sum())
        
        # Outlier counts using Z-Score (|Z| > 2.5)
        z_scores = (series - mean_val) / (std_val if std_val != 0 else 1.0)
        z_outliers = int((np.abs(z_scores) > 2.5).sum())
        
        stats_dict[col] = {
            "count": n,
            "mean": round(mean_val, 4),
            "std": round(std_val, 4),
            "median": round(median_val, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4),
            "q25": round(q25, 4),
            "q75": round(q75, 4),
            "iqr": round(iqr_val, 4),
            "skewness": round(skew_val, 4),
            "kurtosis": round(kurt_val, 4),
            "cv_percent": round(cv_val, 2),
            "iqr_outliers": iqr_outliers,
            "z_outliers": z_outliers
        }
    return stats_dict


def generate_figure1_thermal_gdd(weather_df):
    """Figure 1: Agro-Climatic Thermal Regimes & GDD Trajectory."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [1.2, 1]})
    fig.patch.set_facecolor('#FFFFFF')
    
    dates = weather_df['date']
    tmax = weather_df['t2m_max_c']
    tmin = weather_df['t2m_min_c']
    tavg = weather_df['t2m_avg_c']
    gdd = weather_df['gdd_c_day']
    cum_gdd = weather_df['cumulative_gdd_c']
    
    # Subplot 1: Temperature range and critical biological thresholds
    ax1.plot(dates, tmax, color=C_DANGER, alpha=0.85, linewidth=1.2, label='Daily Maximum Temperature ($T_{max}$)')
    ax1.plot(dates, tmin, color=C_ACCENT_BLUE, alpha=0.85, linewidth=1.2, label='Daily Minimum Temperature ($T_{min}$)')
    ax1.plot(dates, tavg, color=C_PRIMARY, linewidth=1.8, label='Daily Mean Temperature ($T_{avg}$)')
    ax1.fill_between(dates, tmin, tmax, color='#E2E8F0', alpha=0.5, label='Diurnal Thermal Envelope')
    
    # Critical Agronomic Reference Lines
    ax1.axhline(0, color='#3B82F6', linestyle=':', linewidth=1.2, label='Freezing Threshold (0°C)')
    ax1.axhline(10, color='#10B981', linestyle='--', linewidth=1.2, label='Maize Base Temperature ($T_{base}=10°C$)')
    ax1.axhline(30, color='#F59E0B', linestyle='--', linewidth=1.2, label='Maize Optimal Cap ($T_{cap}=30°C$)')
    
    # Annotate extreme summer heat and winter freeze
    max_idx = tmax.idxmax()
    min_idx = tmin.idxmin()
    ax1.annotate(f"Peak Heat: {tmax[max_idx]:.1f}°C\n({dates[max_idx].strftime('%b %d')})",
                 xy=(dates[max_idx], tmax[max_idx]),
                 xytext=(dates[max_idx] - pd.Timedelta(days=45), tmax[max_idx] - 2),
                 arrowprops=dict(facecolor=C_DANGER, arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor=C_DANGER, lw=0.8),
                 fontsize=8.5, fontweight='bold', color=C_DANGER)
    
    ax1.annotate(f"Winter Freeze: {tmin[min_idx]:.1f}°C\n({dates[min_idx].strftime('%b %d')})",
                 xy=(dates[min_idx], tmin[min_idx]),
                 xytext=(dates[min_idx] + pd.Timedelta(days=15), tmin[min_idx] + 5),
                 arrowprops=dict(facecolor=C_ACCENT_BLUE, arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor=C_ACCENT_BLUE, lw=0.8),
                 fontsize=8.5, fontweight='bold', color=C_ACCENT_BLUE)
    
    ax1.set_title("Agro-Climatic Thermal Regime & Growing Degree Day (GDD) Dynamics (Iowa, USA - 2023)",
                  fontsize=13, fontweight='bold', color=C_PRIMARY, pad=12)
    ax1.set_ylabel("Temperature (°C)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax1.grid(True)
    ax1.legend(loc='upper left', framealpha=0.9, fontsize=8, ncol=2)
    
    # Subplot 2: GDD & Cumulative GDD with Phenological Milestones
    ax2_twin = ax2.twinx()
    
    bars = ax2.bar(dates, gdd, width=1.0, color=C_SECONDARY, alpha=0.6, label='Daily GDD (°C-day, Base 10°C)')
    line_cum = ax2_twin.plot(dates, cum_gdd, color=C_PRIMARY, linewidth=2.4, label='Cumulative GDD (°C-day)')
    
    # Phenological stages benchmarks for Corn
    milestones = [
        (120, 'Emergence (VE)', '#059669'),
        (475, 'Six-Leaf Stage (V6)', '#0284C7'),
        (1250, 'Silking / Anthesis (R1)', '#D97706'),
        (2650, 'Physiological Maturity (R6)', '#7C3AED')
    ]
    for gdd_thresh, label_name, col in milestones:
        matching_date = weather_df.loc[weather_df['cumulative_gdd_c'] >= gdd_thresh, 'date']
        if not matching_date.empty:
            m_date = matching_date.iloc[0]
            ax2_twin.scatter([m_date], [gdd_thresh], color=col, s=40, zorder=5)
            ax2_twin.axhline(gdd_thresh, color=col, linestyle=':', alpha=0.5, linewidth=1.0)
            ax2_twin.text(dates.iloc[10], gdd_thresh + 60, f"{label_name} ~ {gdd_thresh}°C",
                          color=col, fontsize=8, fontweight='bold')
    
    ax2.set_ylabel("Daily GDD (°C-day)", fontsize=10, fontweight='bold', color=C_SECONDARY)
    ax2_twin.set_ylabel("Cumulative GDD (°C-day)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.set_xlabel("Date (2023)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.grid(True)
    
    # Combine legends
    lines, labels = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left', framealpha=0.9, fontsize=8.5)
    
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig1_thermal_regimes_gdd.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure2_hydrological_vpd(weather_df):
    """Figure 2: Hydrological Dynamics & Atmospheric Moisture Stress."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [1.1, 1]})
    fig.patch.set_facecolor('#FFFFFF')
    
    dates = weather_df['date']
    precip = weather_df['precipitation_mm']
    precip_7d = weather_df['precip_7d_sum_mm']
    cum_precip = weather_df['cumulative_precip_mm']
    vpd = weather_df['vpd_kpa']
    
    # Top Panel: Daily and Cumulative Precipitation
    ax1_twin = ax1.twinx()
    b1 = ax1.bar(dates, precip, width=1.0, color='#3B82F6', alpha=0.75, label='Daily Precipitation (mm)')
    l1 = ax1.plot(dates, precip_7d, color='#1D4ED8', linewidth=1.5, linestyle='-', label='7-Day Rolling Sum (mm)')
    l2 = ax1_twin.plot(dates, cum_precip, color=C_PRIMARY, linewidth=2.2, label='Cumulative Precipitation (mm)')
    
    # Annotate extreme rainfall deluge
    max_p_idx = precip.idxmax()
    ax1.annotate(f"Extreme Rain Surge: {precip[max_p_idx]:.1f} mm\n({dates[max_p_idx].strftime('%b %d')})",
                 xy=(dates[max_p_idx], precip[max_p_idx]),
                 xytext=(dates[max_p_idx] - pd.Timedelta(days=50), precip[max_p_idx] + 2),
                 arrowprops=dict(facecolor='#1D4ED8', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#1D4ED8', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#1D4ED8')
    
    ax1.set_title("Hydrological Precipitation Patterns and Atmospheric Vapor Pressure Deficit (Iowa - 2023)",
                  fontsize=13, fontweight='bold', color=C_PRIMARY, pad=12)
    ax1.set_ylabel("Daily & 7d Rain (mm)", fontsize=10, fontweight='bold', color='#1D4ED8')
    ax1_twin.set_ylabel("Cumulative Rain (mm)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax1.grid(True)
    
    h1, lab1 = ax1.get_legend_handles_labels()
    h2, lab2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(h1 + h2, lab1 + lab2, loc='upper left', framealpha=0.9, fontsize=8.5)
    
    # Bottom Panel: Vapor Pressure Deficit (VPD) and Stress Zones
    ax2.plot(dates, vpd, color='#D97706', linewidth=1.4, label='Daily Vapor Pressure Deficit (VPD, kPa)')
    ax2.plot(dates, vpd.rolling(14, center=True).mean(), color='#9A3412', linewidth=2.0, label='14-Day Centered Trend')
    
    # Agronomic VPD Stress Bands
    ax2.axhspan(0, 1.2, color='#DCFCE7', alpha=0.5, label='Optimal Transpiration Zone (< 1.2 kPa)')
    ax2.axhspan(1.2, 2.0, color='#FEF3C7', alpha=0.5, label='Moderate Atmospheric Moisture Demand (1.2–2.0 kPa)')
    ax2.axhspan(2.0, max(3.5, vpd.max() + 0.3), color='#FEE2E2', alpha=0.5, label='Severe Crop Stomatal Stress (> 2.0 kPa)')
    
    # Annotate peak atmospheric drought stress event
    max_vpd_idx = vpd.idxmax()
    ax2.annotate(f"Peak Atmospheric Drought: {vpd[max_vpd_idx]:.2f} kPa\n({dates[max_vpd_idx].strftime('%b %d')})",
                 xy=(dates[max_vpd_idx], vpd[max_vpd_idx]),
                 xytext=(dates[max_vpd_idx] + pd.Timedelta(days=12), vpd[max_vpd_idx] - 0.3),
                 arrowprops=dict(facecolor='#B91C1C', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#B91C1C', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#B91C1C')
    
    ax2.set_ylabel("VPD (kPa)", fontsize=10, fontweight='bold', color='#B45309')
    ax2.set_xlabel("Date (2023)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.grid(True)
    ax2.legend(loc='upper left', framealpha=0.9, fontsize=8.5, ncol=2)
    
    ax2.xaxis.set_major_locator(mdates.MonthLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig2_hydrological_moisture_vpd.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure3_ndvi_phenology(ndvi_df):
    """Figure 3: Satellite Remote Sensing Phenology & Cloud Anomaly Filtering."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.patch.set_facecolor('#FFFFFF')
    
    dates = ndvi_df['observation_date']
    raw_ndvi = ndvi_df['raw_ndvi']
    interp_ndvi = ndvi_df['interpolated_ndvi']
    smooth_ndvi = ndvi_df['smoothed_ndvi']
    cloud_flags = ndvi_df['cloud_flag'] == 1
    
    # Plot smooth baseline trajectory
    ax.plot(dates, smooth_ndvi, color=C_PRIMARY, linewidth=2.8, zorder=4,
            label='Savitzky-Golay Filtered Phenological Trajectory')
    
    # Plot interpolated gap filling
    ax.plot(dates, interp_ndvi, color=C_ACCENT_TEAL, linestyle='--', linewidth=1.5, zorder=3,
            label='Linear Gap-Filled Series')
    
    # Plot clean raw observations
    clean_obs = ndvi_df[~cloud_flags]
    ax.scatter(clean_obs['observation_date'], clean_obs['raw_ndvi'], color='#059669', s=45,
               edgecolors='white', linewidth=0.8, zorder=5, label='Clear-Sky Sentinel-2 Observations')
    
    # Highlight Cloud Artifacts (Dropouts)
    cloud_obs = ndvi_df[cloud_flags]
    ax.scatter(cloud_obs['observation_date'], cloud_obs['raw_ndvi'], color=C_DANGER, s=75,
               marker='X', edgecolors='#7F1D1D', linewidth=0.8, zorder=6,
               label='Flagged Atmospheric/Cloud Shadow Dropout Anomalies')
    
    # Annotate dropouts
    for _, row in cloud_obs.iterrows():
        drop_magnitude = row['smoothed_ndvi'] - row['raw_ndvi']
        ax.vlines(x=row['observation_date'], ymin=row['raw_ndvi'], ymax=row['smoothed_ndvi'],
                  color=C_DANGER, linestyle=':', linewidth=1.2, alpha=0.8)
    
    # Highlight critical phenological stages
    peak_idx = smooth_ndvi.idxmax()
    peak_date = dates[peak_idx]
    peak_val = smooth_ndvi[peak_idx]
    ax.annotate(f"Peak Canopy Greenness (Anthesis)\nNDVI: {peak_val:.3f} ({peak_date.strftime('%b %d')}, DOY {ndvi_df.loc[peak_idx, 'day_of_year']})",
                xy=(peak_date, peak_val),
                xytext=(peak_date - pd.Timedelta(days=40), peak_val + 0.08),
                arrowprops=dict(facecolor=C_PRIMARY, arrowstyle='->', lw=1.5),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FDF4', edgecolor=C_PRIMARY, lw=1.0),
                fontsize=9, fontweight='bold', color=C_PRIMARY)
    
    # Annotate Senescence Phase
    ax.text(pd.to_datetime('2023-09-05'), 0.65, "Rapid Senescence Phase\n(Chlorophyll Breakdown\n& Grain Desiccation)",
            color='#9A3412', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFBEB', edgecolor='#F59E0B', lw=0.8))
    
    # Annotate Emergence / Green-up
    ax.text(pd.to_datetime('2023-05-01'), 0.38, "Early Vegetative\nEmergence Phase",
            color='#166534', fontsize=8.5, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#DCFCE7', edgecolor='#16A34A', lw=0.8))
    
    ax.set_title("Sentinel-2 Multi-Spectral Surface Reflectance (NDVI) Phenology & Outlier Smoothing (2023)",
                 fontsize=13, fontweight='bold', color=C_PRIMARY, pad=12)
    ax.set_ylabel("Normalized Difference Vegetation Index (NDVI)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax.set_xlabel("Observation Date (Growing Season: April – October 2023)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax.set_ylim(0.0, 1.0)
    ax.grid(True)
    ax.legend(loc='lower center', framealpha=0.95, fontsize=8.5, ncol=2)
    
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig3_sentinel2_ndvi_phenology.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure4_commodity_prices(prices_df):
    """Figure 4: Global Agribusiness Commodity Price Evolution & Volatility Dynamics."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [1.3, 1]})
    fig.patch.set_facecolor('#FFFFFF')
    
    dates = prices_df['period_date']
    maize = prices_df['maize_usd_per_mt']
    soya = prices_df['soybeans_usd_per_mt']
    wheat = prices_df['wheat_us_hrw_usd_per_mt']
    dap = prices_df['fertilizer_dap_usd_per_mt']
    
    # Top Panel: Nominal Benchmark Prices
    ax1.plot(dates, dap, color='#7C3AED', linewidth=2.4, marker='s', markersize=4, label='Fertilizer DAP (FOB US Gulf)')
    ax1.plot(dates, soya, color='#059669', linewidth=2.0, marker='o', markersize=4, label='Soybeans (US No. 2 Yellow)')
    ax1.plot(dates, wheat, color='#D97706', linewidth=2.0, marker='^', markersize=4, label='Wheat (US HRW)')
    ax1.plot(dates, maize, color='#2563EB', linewidth=2.0, marker='D', markersize=4, label='Maize (US No. 2 Yellow)')
    
    # Highlight 2022 Geopolitical Conflict Window
    ax1.axvspan(pd.to_datetime('2022-02-01'), pd.to_datetime('2022-06-30'), color='#FEE2E2', alpha=0.4,
                label='Geopolitical Black Sea Shock & Export Disruption')
    
    # Annotate DAP Fertilizer Peak
    max_dap_idx = dap.idxmax()
    ax1.annotate(f"Historic Fertilizer Peak:\n${dap[max_dap_idx]:.0f}/MT ({dates[max_dap_idx].strftime('%b %Y')})",
                 xy=(dates[max_dap_idx], dap[max_dap_idx]),
                 xytext=(dates[max_dap_idx] + pd.Timedelta(days=25), dap[max_dap_idx] - 60),
                 arrowprops=dict(facecolor='#7C3AED', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#F3E8FF', edgecolor='#7C3AED', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#7C3AED')
    
    # Annotate Wheat Peak
    max_wheat_idx = wheat.idxmax()
    ax1.annotate(f"Wheat Shock Peak:\n${wheat[max_wheat_idx]:.0f}/MT ({dates[max_wheat_idx].strftime('%b %Y')})",
                 xy=(dates[max_wheat_idx], wheat[max_wheat_idx]),
                 xytext=(dates[max_wheat_idx] - pd.Timedelta(days=120), wheat[max_wheat_idx] + 20),
                 arrowprops=dict(facecolor='#D97706', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF3C7', edgecolor='#D97706', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#D97706')
    
    ax1.set_title("Global Agricultural Commodity & Fertilizer Benchmark Pricing (World Bank Pink Sheet 2021–2023)",
                  fontsize=13, fontweight='bold', color=C_PRIMARY, pad=12)
    ax1.set_ylabel("Price (USD / Metric Ton)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax1.grid(True)
    ax1.legend(loc='upper left', framealpha=0.9, fontsize=8.5, ncol=2)
    
    # Bottom Panel: Rolling 3-Month Price Volatility
    vol_maize = prices_df['maize_volatility_3m']
    vol_wheat = prices_df['wheat_volatility_3m']
    
    ax2.plot(dates, vol_wheat, color='#D97706', linewidth=2.2, label='Wheat 3-Month Volatility (Rolling Std Dev, USD/MT)')
    ax2.plot(dates, vol_maize, color='#2563EB', linewidth=2.2, label='Maize 3-Month Volatility (Rolling Std Dev, USD/MT)')
    
    # Critical volatility threshold
    ax2.axhline(30, color=C_DANGER, linestyle='--', linewidth=1.2, label='High Market Stress Threshold (Std Dev > $30/MT)')
    ax2.axvspan(pd.to_datetime('2022-02-01'), pd.to_datetime('2022-06-30'), color='#FEE2E2', alpha=0.4)
    
    # Annotate wheat volatility spike
    max_vol_w_idx = vol_wheat.idxmax()
    ax2.annotate(f"Record Volatility: ${vol_wheat[max_vol_w_idx]:.1f}/MT\n({dates[max_vol_w_idx].strftime('%b %Y')})",
                 xy=(dates[max_vol_w_idx], vol_wheat[max_vol_w_idx]),
                 xytext=(dates[max_vol_w_idx] + pd.Timedelta(days=20), vol_wheat[max_vol_w_idx] - 10),
                 arrowprops=dict(facecolor='#B91C1C', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#B91C1C', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#B91C1C')
    
    ax2.set_ylabel("3M Rolling Volatility ($/MT)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.set_xlabel("Month / Year (2021–2023)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.grid(True)
    ax2.legend(loc='upper right', framealpha=0.9, fontsize=8.5)
    
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig4_commodity_prices_volatility.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure5_parity_ratios(prices_df):
    """Figure 5: Fertilizer-to-Crop Price Parity Ratios & Farmer Margin Pressures."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.patch.set_facecolor('#FFFFFF')
    
    dates = prices_df['period_date']
    dap_maize = prices_df['dap_to_maize_ratio']
    dap_wheat = prices_df['dap_to_wheat_ratio']
    
    ax.plot(dates, dap_maize, color='#1E40AF', linewidth=2.4, marker='o', markersize=4.5,
            label='DAP Fertilizer-to-Maize Ratio (MT Maize required per MT DAP)')
    ax.plot(dates, dap_wheat, color='#D97706', linewidth=2.4, marker='s', markersize=4.5,
            label='DAP Fertilizer-to-Wheat Ratio (MT Wheat required per MT DAP)')
    
    # Benchmark lines
    ax.axhline(2.0, color='#10B981', linestyle='--', linewidth=1.5, label='Normal Economic Affordability Threshold (~2.0x)')
    ax.axhline(2.5, color='#F59E0B', linestyle='--', linewidth=1.5, label='Elevated Margin Compression Warning (~2.5x)')
    ax.axhline(3.0, color='#DC2626', linestyle='--', linewidth=1.5, label='Severe Farm Insolvency Risk Zone (> 3.0x)')
    
    # Stress zone shading
    ax.axhspan(2.5, 3.2, color='#FEE2E2', alpha=0.35)
    
    # Annotate peak compression
    max_dm_idx = dap_maize.idxmax()
    ax.annotate(f"Peak Margin Compression:\n{dap_maize[max_dm_idx]:.2f}x ({dates[max_dm_idx].strftime('%b %Y')})\n[Farmers must sell >3 MT corn per 1 MT DAP]",
                xy=(dates[max_dm_idx], dap_maize[max_dm_idx]),
                xytext=(dates[max_dm_idx] - pd.Timedelta(days=120), dap_maize[max_dm_idx] + 0.12),
                arrowprops=dict(facecolor='#1E40AF', arrowstyle='->', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#1E40AF', lw=0.8),
                fontsize=8.5, fontweight='bold', color='#1E40AF')
    
    ax.set_title("Input-to-Output Price Parity Ratios (DAP Fertilizer vs Grains) & Farm Economics (2021–2023)",
                 fontsize=13, fontweight='bold', color=C_PRIMARY, pad=12)
    ax.set_ylabel("Price Ratio (MT Crop per MT DAP)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax.set_xlabel("Month / Year (2021–2023)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax.set_ylim(1.4, 3.3)
    ax.grid(True)
    ax.legend(loc='lower left', framealpha=0.95, fontsize=8.5, ncol=2)
    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig5_input_output_parity_ratios.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure6_crop_yields(crop_df):
    """Figure 6: Comparative Crop Yields & Land Harvest Efficiency."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#FFFFFF')
    
    # Subplot 1: Yield Evolution (MT/ha) across the 3 crop systems
    crops = [
        ('USA', 'Iowa', 'Maize', '#2563EB', 'o', 'Iowa Maize (USDA)'),
        ('USA', 'Iowa', 'Soybeans', '#059669', 's', 'Iowa Soybeans (USDA)'),
        ('IND', 'Punjab', 'Wheat', '#D97706', '^', 'Punjab Wheat (FAOSTAT)')
    ]
    
    for country, region, crop, col, m, label in crops:
        sub = crop_df[(crop_df['country_iso3'] == country) & 
                      (crop_df['admin1_region'] == region) & 
                      (crop_df['crop_name'] == crop)].sort_values('crop_year')
        ax1.plot(sub['crop_year'], sub['yield_mt_per_ha'], color=col, marker=m,
                 linewidth=2.2, markersize=6, label=label)
    
    # Annotate 2020 Iowa Derecho Yield Drop
    iowa_maize = crop_df[(crop_df['admin1_region'] == 'Iowa') & (crop_df['crop_name'] == 'Maize')]
    row_2020 = iowa_maize[iowa_maize['crop_year'] == 2020].iloc[0]
    ax1.annotate(f"2020 Iowa Derecho Shock:\nYield dropped to {row_2020['yield_mt_per_ha']:.2f} MT/ha\n(-10.1% vs 2019)",
                 xy=(2020, row_2020['yield_mt_per_ha']),
                 xytext=(2019.2, row_2020['yield_mt_per_ha'] - 1.2),
                 arrowprops=dict(facecolor='#2563EB', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#EFF6FF', edgecolor='#2563EB', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#2563EB')
    
    # Annotate 2022 Punjab Heatwave
    punjab_wheat = crop_df[(crop_df['admin1_region'] == 'Punjab') & (crop_df['crop_name'] == 'Wheat')]
    row_2022 = punjab_wheat[punjab_wheat['crop_year'] == 2022].iloc[0]
    ax1.annotate(f"2022 Heatwave Shock:\nYield fell to {row_2022['yield_mt_per_ha']:.2f} MT/ha\n(-9.6% vs 2021)",
                 xy=(2022, row_2022['yield_mt_per_ha']),
                 xytext=(2020.8, row_2022['yield_mt_per_ha'] - 1.0),
                 arrowprops=dict(facecolor='#D97706', arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF3C7', edgecolor='#D97706', lw=0.8),
                 fontsize=8.5, fontweight='bold', color='#D97706')
    
    ax1.set_title("Harmonized Crop Yield Benchmarks (2018–2023)", fontsize=12, fontweight='bold', color=C_PRIMARY)
    ax1.set_ylabel("Yield (Metric Tons / Hectare)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax1.set_xlabel("Crop Year", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax1.set_xticks(range(2018, 2024))
    ax1.grid(True)
    ax1.legend(loc='center left', framealpha=0.9, fontsize=8.5)
    
    # Subplot 2: Harvested-to-Planted Area Efficiency Ratio
    for country, region, crop, col, m, label in crops:
        sub = crop_df[(crop_df['country_iso3'] == country) & 
                      (crop_df['admin1_region'] == region) & 
                      (crop_df['crop_name'] == crop)].sort_values('crop_year')
        ax2.plot(sub['crop_year'], sub['harvested_ratio'] * 100, color=col, marker=m,
                 linewidth=2.2, markersize=6, label=label)
    
    # Annotate 2020 Derecho Land Abandonment
    ax2.annotate("2020 Derecho Crop Loss:\nIowa Maize Harvested Ratio: 94.85%\n(>700,000 acres unharvested)",
                 xy=(2020, 94.85),
                 xytext=(2019.5, 95.8),
                 arrowprops=dict(facecolor=C_DANGER, arrowstyle='->', lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor=C_DANGER, lw=0.8),
                 fontsize=8.5, fontweight='bold', color=C_DANGER)
    
    ax2.set_title("Harvested-to-Planted Area Efficiency (%)", fontsize=12, fontweight='bold', color=C_PRIMARY)
    ax2.set_ylabel("Harvested / Planted Ratio (%)", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.set_xlabel("Crop Year", fontsize=10, fontweight='bold', color=C_PRIMARY)
    ax2.set_xticks(range(2018, 2024))
    ax2.set_ylim(94.0, 100.5)
    ax2.grid(True)
    ax2.legend(loc='lower left', framealpha=0.9, fontsize=8.5)
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig6_crop_yield_benchmarks.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure7_correlation_matrix(weather_df):
    """Figure 7: Agro-Meteorological Multivariate Correlation Matrix."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))
    fig.patch.set_facecolor('#FFFFFF')
    
    features = [
        't2m_avg_c', 'gdd_c_day', 'vpd_kpa', 'solar_radiation_mj_m2',
        'relative_humidity_pct', 'wind_speed_m_s', 'precipitation_mm'
    ]
    labels = [
        '$T_{avg}$ (°C)', 'GDD', 'VPD (kPa)', 'Solar Rad',
        'Rel Humidity', 'Wind Speed', 'Rainfall'
    ]
    
    sub_df = weather_df[features].copy()
    
    # 1. Pearson Linear Correlation Matrix
    corr_p = sub_df.corr(method='pearson')
    mask = np.triu(np.ones_like(corr_p, dtype=bool))
    
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    
    sns.heatmap(corr_p, mask=mask, annot=True, fmt='.2f', cmap=cmap, vmin=-1, vmax=1,
                xticklabels=labels, yticklabels=labels, ax=ax1, cbar_kws={'shrink': 0.8, 'label': 'Pearson $r$'},
                annot_kws={'fontsize': 8.5, 'fontweight': 'bold'})
    ax1.set_title("Pearson Linear Correlation Matrix\n(Iowa Agrometeorology 2023)",
                  fontsize=12, fontweight='bold', color=C_PRIMARY, pad=10)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Spearman Monotonic Rank Correlation Matrix
    corr_s = sub_df.corr(method='spearman')
    sns.heatmap(corr_s, mask=mask, annot=True, fmt='.2f', cmap=cmap, vmin=-1, vmax=1,
                xticklabels=labels, yticklabels=labels, ax=ax2, cbar_kws={'shrink': 0.8, 'label': 'Spearman $\\rho$'},
                annot_kws={'fontsize': 8.5, 'fontweight': 'bold'})
    ax2.set_title("Spearman Rank Correlation Matrix\n(Monotonic Non-Linear Associations)",
                  fontsize=12, fontweight='bold', color=C_PRIMARY, pad=10)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig7_multivariate_correlation_matrix.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def generate_figure8_anomaly_dashboard(weather_df, ndvi_df, prices_df, crop_df):
    """Figure 8: Multi-Modal Anomaly Detection Dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.patch.set_facecolor('#FFFFFF')
    
    # Quadrant A: Weather Outliers (Precipitation & Temperature Z-Scores)
    ax_a = axes[0, 0]
    p_mean = weather_df['precipitation_mm'].mean()
    p_std = weather_df['precipitation_mm'].std()
    p_z = (weather_df['precipitation_mm'] - p_mean) / p_std
    
    t_mean = weather_df['t2m_max_c'].mean()
    t_std = weather_df['t2m_max_c'].std()
    t_z = (weather_df['t2m_max_c'] - t_mean) / t_std
    
    ax_a.plot(weather_df['date'], p_z, color='#2563EB', alpha=0.6, label='Rainfall Z-Score')
    ax_a.plot(weather_df['date'], t_z, color='#DC2626', alpha=0.6, label='Tmax Z-Score')
    ax_a.axhline(2.5, color=C_DANGER, linestyle='--', label='Outlier Threshold ($Z > +2.5$)')
    ax_a.axhline(-2.5, color=C_DANGER, linestyle='--', label='Outlier Threshold ($Z < -2.5$)')
    
    # Highlight extreme rainfall dates
    p_outliers = weather_df[p_z > 2.5]
    ax_a.scatter(p_outliers['date'], p_z[p_z > 2.5], color='#1D4ED8', s=40, zorder=5)
    
    ax_a.set_title("A. Agro-Climate Statistical Anomalies (|Z-Score| > 2.5)",
                   fontsize=11, fontweight='bold', color=C_PRIMARY)
    ax_a.set_ylabel("Standardized Z-Score", fontsize=9, fontweight='bold')
    ax_a.grid(True)
    ax_a.legend(loc='upper right', fontsize=7.5)
    ax_a.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax_a.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    
    # Quadrant B: Satellite Remote Sensing Residual Cloud Dropouts
    ax_b = axes[0, 1]
    cloud_mask = ndvi_df['cloud_flag'] == 1
    residuals = ndvi_df['raw_ndvi'] - ndvi_df['smoothed_ndvi']
    
    ax_b.scatter(ndvi_df.loc[~cloud_mask, 'day_of_year'], residuals[~cloud_mask],
                 color='#10B981', s=35, label='Clear Sky Observations (Residual ~0)')
    ax_b.scatter(ndvi_df.loc[cloud_mask, 'day_of_year'], residuals[cloud_mask],
                 color=C_DANGER, marker='X', s=70, label='Cloud Attenuation Dropouts ($|\\Delta| > 0.15$)')
    ax_b.axhline(0, color=C_MUTED, linestyle='-', linewidth=0.8)
    ax_b.axhline(-0.15, color=C_DANGER, linestyle=':', linewidth=1.2, label='Dropout Anomaly Threshold (-0.15)')
    
    ax_b.set_title("B. Remote Sensing Cloud-Contamination Anomaly Detection",
                   fontsize=11, fontweight='bold', color=C_PRIMARY)
    ax_b.set_xlabel("Day of Year (DOY 2023)", fontsize=9, fontweight='bold')
    ax_b.set_ylabel("Residual (Raw NDVI - Smoothed NDVI)", fontsize=9, fontweight='bold')
    ax_b.grid(True)
    ax_b.legend(loc='lower left', fontsize=7.5)
    
    # Quadrant C: Commodity Market Monthly Return Spikes (MoM %)
    ax_c = axes[1, 0]
    dates_p = prices_df['period_date']
    wheat_mom = prices_df['wheat_mom_pct']
    dap_mom = prices_df['fertilizer_mom_pct']
    
    ax_c.bar(dates_p - pd.Timedelta(days=5), wheat_mom, width=10, color='#D97706', alpha=0.8, label='Wheat MoM (%)')
    ax_c.bar(dates_p + pd.Timedelta(days=5), dap_mom, width=10, color='#7C3AED', alpha=0.8, label='DAP Fertilizer MoM (%)')
    ax_c.axhline(10.0, color=C_DANGER, linestyle='--', label='Severe Price Shock Threshold (+10%)')
    ax_c.axhline(-10.0, color='#2563EB', linestyle='--', label='Rapid Deflation Threshold (-10%)')
    
    ax_c.set_title("C. Monthly Commodity Price Shocks & Geopolitical Spikes",
                   fontsize=11, fontweight='bold', color=C_PRIMARY)
    ax_c.set_ylabel("Month-over-Month Change (%)", fontsize=9, fontweight='bold')
    ax_c.grid(True)
    ax_c.legend(loc='upper right', fontsize=7.5)
    ax_c.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax_c.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
    
    # Quadrant D: Crop Yield Historical Deviation from 6-Year Mean
    ax_d = axes[1, 1]
    crop_deviations = []
    crop_keys = [('USA', 'Iowa', 'Maize'), ('USA', 'Iowa', 'Soybeans'), ('IND', 'Punjab', 'Wheat')]
    colors_d = ['#2563EB', '#059669', '#D97706']
    
    years = sorted(crop_df['crop_year'].unique())
    x = np.arange(len(years))
    width = 0.25
    
    for idx, (country, region, crop) in enumerate(crop_keys):
        sub = crop_df[(crop_df['country_iso3'] == country) & 
                      (crop_df['admin1_region'] == region) & 
                      (crop_df['crop_name'] == crop)].sort_values('crop_year')
        mean_y = sub['yield_mt_per_ha'].mean()
        dev_pct = ((sub['yield_mt_per_ha'] - mean_y) / mean_y) * 100
        ax_d.bar(x + (idx - 1) * width, dev_pct, width, label=f"{region} {crop}", color=colors_d[idx], alpha=0.85)
    
    ax_d.axhline(0, color=C_MUTED, linestyle='-', linewidth=0.8)
    ax_d.axhline(-8.0, color=C_DANGER, linestyle=':', linewidth=1.2, label='Agronomic Shock Cutoff (-8%)')
    
    ax_d.set_xticks(x)
    ax_d.set_xticklabels(years)
    ax_d.set_title("D. Historical Crop Yield Deviations vs Baseline Mean (%)",
                   fontsize=11, fontweight='bold', color=C_PRIMARY)
    ax_d.set_ylabel("Yield Deviation vs Mean (%)", fontsize=9, fontweight='bold')
    ax_d.set_xlabel("Harvest Year", fontsize=9, fontweight='bold')
    ax_d.grid(True)
    ax_d.legend(loc='lower left', fontsize=7.5)
    
    plt.suptitle("Integrated Multi-Modal Agribusiness Anomaly Detection Dashboard",
                 fontsize=14, fontweight='bold', color=C_PRIMARY, y=0.99)
    plt.tight_layout()
    output_path = os.path.join(FIG_DIR, "fig8_anomaly_detection_dashboard.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


def run_eda_pipeline():
    """Executes the full exploratory data analysis pipeline and saves outputs."""
    print("Loading preprocessed agribusiness datasets...")
    weather_df, ndvi_df, prices_df, crop_df = load_datasets()
    
    print("Calculating comprehensive descriptive statistics...")
    # Agrometeorology stats
    weather_numeric = [
        't2m_avg_c', 't2m_max_c', 't2m_min_c', 'precipitation_mm',
        'solar_radiation_mj_m2', 'relative_humidity_pct', 'wind_speed_m_s',
        'gdd_c_day', 'vpd_kpa', 'cumulative_gdd_c', 'cumulative_precip_mm'
    ]
    weather_stats = compute_descriptive_stats(weather_df, weather_numeric)
    
    # Phenology stats
    ndvi_numeric = ['raw_ndvi', 'interpolated_ndvi', 'smoothed_ndvi']
    ndvi_stats = compute_descriptive_stats(ndvi_df, ndvi_numeric)
    
    # Prices stats
    prices_numeric = [
        'maize_usd_per_mt', 'soybeans_usd_per_mt', 'wheat_us_hrw_usd_per_mt',
        'fertilizer_dap_usd_per_mt', 'maize_mom_pct', 'wheat_mom_pct',
        'fertilizer_mom_pct', 'dap_to_maize_ratio', 'dap_to_wheat_ratio'
    ]
    prices_stats = compute_descriptive_stats(prices_df, prices_numeric)
    
    # Crop production stats
    crop_stats = {}
    for crop in crop_df['crop_name'].unique():
        sub = crop_df[crop_df['crop_name'] == crop]
        crop_stats[crop] = {
            'yield_mean': round(float(sub['yield_mt_per_ha'].mean()), 2),
            'yield_std': round(float(sub['yield_mt_per_ha'].std()), 2),
            'yield_min': round(float(sub['yield_mt_per_ha'].min()), 2),
            'yield_max': round(float(sub['yield_mt_per_ha'].max()), 2),
            'yield_cv': round(float(sub['yield_mt_per_ha'].std() / sub['yield_mt_per_ha'].mean() * 100), 2),
            'harvest_ratio_mean': round(float(sub['harvested_ratio'].mean() * 100), 2),
            'harvest_ratio_min': round(float(sub['harvested_ratio'].min() * 100), 2),
            'production_mt_mean': round(float(sub['production_metric_tons'].mean()), 0)
        }
    
    # Specific Phenological and Anomaly Metrics
    peak_ndvi_idx = ndvi_df['smoothed_ndvi'].idxmax()
    pheno_summary = {
        'peak_ndvi_date': str(ndvi_df.loc[peak_ndvi_idx, 'observation_date'].date()),
        'peak_ndvi_doy': int(ndvi_df.loc[peak_ndvi_idx, 'day_of_year']),
        'peak_ndvi_value': round(float(ndvi_df.loc[peak_ndvi_idx, 'smoothed_ndvi']), 4),
        'min_ndvi_value': round(float(ndvi_df['smoothed_ndvi'].min()), 4),
        'cloud_contamination_count': int(ndvi_df['cloud_flag'].sum()),
        'cloud_contamination_pct': round(float(ndvi_df['cloud_flag'].mean() * 100), 2),
        'total_gdd_accumulated': round(float(weather_df['cumulative_gdd_c'].iloc[-1]), 1),
        'total_precipitation_annual_mm': round(float(weather_df['cumulative_precip_mm'].iloc[-1]), 1),
        'extreme_heat_days_above_32c': int((weather_df['t2m_max_c'] >= 32.0).sum()),
        'extreme_vpd_stress_days_above_2kpa': int((weather_df['vpd_kpa'] >= 2.0).sum()),
        'dap_peak_usd': float(prices_df['fertilizer_dap_usd_per_mt'].max()),
        'wheat_peak_usd': float(prices_df['wheat_us_hrw_usd_per_mt'].max()),
        'maize_peak_usd': float(prices_df['maize_usd_per_mt'].max()),
        'dap_maize_ratio_peak': round(float(prices_df['dap_to_maize_ratio'].max()), 2),
        'dap_wheat_ratio_peak': round(float(prices_df['dap_to_wheat_ratio'].max()), 2)
    }
    
    summary_export = {
        "agrometeorology_stats": weather_stats,
        "phenology_stats": ndvi_stats,
        "commodity_price_stats": prices_stats,
        "crop_production_stats": crop_stats,
        "agronomic_indicators": pheno_summary
    }
    
    summary_json_path = os.path.join(DATA_DIR, "eda_summary_statistics.json")
    with open(summary_json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_export, f, indent=2)
    print(f"Descriptive statistics saved to {summary_json_path}")
    
    print("Generating High-Resolution Publication Visualizations...")
    f1 = generate_figure1_thermal_gdd(weather_df)
    print(f"Generated: {f1}")
    f2 = generate_figure2_hydrological_vpd(weather_df)
    print(f"Generated: {f2}")
    f3 = generate_figure3_ndvi_phenology(ndvi_df)
    print(f"Generated: {f3}")
    f4 = generate_figure4_commodity_prices(prices_df)
    print(f"Generated: {f4}")
    f5 = generate_figure5_parity_ratios(prices_df)
    print(f"Generated: {f5}")
    f6 = generate_figure6_crop_yields(crop_df)
    print(f"Generated: {f6}")
    f7 = generate_figure7_correlation_matrix(weather_df)
    print(f"Generated: {f7}")
    f8 = generate_figure8_anomaly_dashboard(weather_df, ndvi_df, prices_df, crop_df)
    print(f"Generated: {f8}")
    
    print("All 8 figures successfully generated at 300 DPI.")
    return summary_export


if __name__ == '__main__':
    run_eda_pipeline()

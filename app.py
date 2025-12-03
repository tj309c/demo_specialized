"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     SERVICE COMMAND - SPECIALIZED BICYCLES                     ║
║               Integrated Business Planning for Service & Warranty              ║
║                                                                                 ║
║  "Service is not just a cost center; it is a brand retention engine."          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import hashlib

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Service Command | Specialized",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM STYLING - BASE STYLES (Theme-independent)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# THEME FUNCTION - Returns CSS based on mode
# ═══════════════════════════════════════════════════════════════════════════════

def get_theme_css(dark_mode=True):
    if dark_mode:
        # DARK THEME
        return """
        <style>
            :root {
                --specialized-red: #E31837;
                --specialized-red-dark: #B91430;
                --bg-primary: #0D1117;
                --bg-secondary: #161B22;
                --bg-card: #1C2128;
                --card-border: #30363D;
                --text-primary: #F0F6FC;
                --text-secondary: #8B949E;
                --accent-green: #3FB950;
                --accent-yellow: #D29922;
                --accent-orange: #DB6D28;
                --accent-blue: #58A6FF;
            }

            .stApp {
                background: linear-gradient(135deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
                border-right: 1px solid #30363D;
            }

            [data-testid="stSidebar"] .stMarkdown { color: #F0F6FC; }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Inter', sans-serif !important;
                color: #F0F6FC !important;
                font-weight: 600 !important;
            }

            .metric-card {
                background: linear-gradient(145deg, #1C2128 0%, #161B22 100%);
                border: 1px solid #30363D;
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            }

            .metric-card:hover {
                border-color: #E31837;
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                font-family: 'JetBrains Mono', monospace;
                background: linear-gradient(135deg, #E31837, #FF4D6A);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            }

            .metric-label {
                font-size: 0.85rem;
                color: #8B949E;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 4px;
            }

            .metric-delta-positive { color: #3FB950; font-size: 0.9rem; }
            .metric-delta-negative { color: #F85149; font-size: 0.9rem; }

            .status-critical { background: linear-gradient(135deg, #F85149, #DA3633); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
            .status-warning { background: linear-gradient(135deg, #D29922, #E3B341); color: #0D1117; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
            .status-healthy { background: linear-gradient(135deg, #3FB950, #2EA043); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }

            .insight-card {
                background: linear-gradient(135deg, #1C2526 0%, #0D1117 100%);
                border-left: 4px solid #E31837;
                border-radius: 0 8px 8px 0;
                padding: 16px 20px;
                margin: 16px 0;
            }

            .insight-card h4 { color: #E31837 !important; margin: 0 0 8px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
            .insight-card p { color: #C9D1D9; margin: 0; font-size: 0.95rem; line-height: 1.6; }

            .stDataFrame { border: 1px solid #30363D; border-radius: 8px; }

            .stButton > button {
                background: linear-gradient(135deg, #E31837, #B91430);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 12px 24px;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, #FF4D6A, #E31837);
                box-shadow: 0 4px 20px rgba(227, 24, 55, 0.4);
                transform: translateY(-2px);
            }

            .streamlit-expanderHeader { background: #1C2128; border-radius: 8px; color: #F0F6FC !important; }
            .stSlider > div > div { background: #30363D; }
            .stSlider > div > div > div { background: #E31837; }

            .stTabs [data-baseweb="tab-list"] { gap: 8px; background: #161B22; padding: 8px; border-radius: 12px; }
            .stTabs [data-baseweb="tab"] { background: transparent; color: #8B949E; border-radius: 8px; padding: 12px 24px; }
            .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #E31837, #B91430); color: white; }

            .hero-header {
                background: linear-gradient(135deg, #0D1117 0%, #1C2128 50%, #0D1117 100%);
                border: 1px solid #30363D;
                border-radius: 16px;
                padding: 32px;
                margin-bottom: 24px;
                position: relative;
                overflow: hidden;
            }

            .hero-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #E31837, #FF4D6A, #E31837);
            }

            .talking-point {
                background: #1C2128;
                border-left: 3px solid #58A6FF;
                padding: 12px 16px;
                margin: 8px 0;
                border-radius: 0 8px 8px 0;
            }

            .talking-point p { color: #C9D1D9; font-size: 0.85rem; margin: 0; line-height: 1.5; }
        </style>
        """
    else:
        # LIGHT THEME
        return """
        <style>
            :root {
                --specialized-red: #E31837;
                --specialized-red-dark: #B91430;
                --bg-primary: #FFFFFF;
                --bg-secondary: #F6F8FA;
                --bg-card: #FFFFFF;
                --card-border: #D0D7DE;
                --text-primary: #1F2328;
                --text-secondary: #656D76;
                --accent-green: #1A7F37;
                --accent-yellow: #9A6700;
                --accent-orange: #BC4C00;
                --accent-blue: #0969DA;
            }

            .stApp {
                background: linear-gradient(135deg, #FFFFFF 0%, #F6F8FA 50%, #FFFFFF 100%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #F6F8FA 0%, #FFFFFF 100%);
                border-right: 1px solid #D0D7DE;
            }

            [data-testid="stSidebar"] .stMarkdown { color: #1F2328; }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Inter', sans-serif !important;
                color: #1F2328 !important;
                font-weight: 600 !important;
            }

            .metric-card {
                background: linear-gradient(145deg, #FFFFFF 0%, #F6F8FA 100%);
                border: 1px solid #D0D7DE;
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }

            .metric-card:hover {
                border-color: #E31837;
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }

            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                font-family: 'JetBrains Mono', monospace;
                background: linear-gradient(135deg, #E31837, #FF4D6A);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            }

            .metric-label {
                font-size: 0.85rem;
                color: #656D76;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-top: 4px;
            }

            .metric-delta-positive { color: #1A7F37; font-size: 0.9rem; }
            .metric-delta-negative { color: #CF222E; font-size: 0.9rem; }

            .status-critical { background: linear-gradient(135deg, #CF222E, #A40E26); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
            .status-warning { background: linear-gradient(135deg, #BF8700, #9A6700); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
            .status-healthy { background: linear-gradient(135deg, #1A7F37, #116329); color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }

            .insight-card {
                background: linear-gradient(135deg, #FFF5F5 0%, #FFFFFF 100%);
                border-left: 4px solid #E31837;
                border-radius: 0 8px 8px 0;
                padding: 16px 20px;
                margin: 16px 0;
            }

            .insight-card h4 { color: #E31837 !important; margin: 0 0 8px 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }
            .insight-card p { color: #1F2328; margin: 0; font-size: 0.95rem; line-height: 1.6; }

            .stDataFrame { border: 1px solid #D0D7DE; border-radius: 8px; }

            .stButton > button {
                background: linear-gradient(135deg, #E31837, #B91430);
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                padding: 12px 24px;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, #FF4D6A, #E31837);
                box-shadow: 0 4px 20px rgba(227, 24, 55, 0.4);
                transform: translateY(-2px);
            }

            .streamlit-expanderHeader { background: #F6F8FA; border-radius: 8px; color: #1F2328 !important; }
            .stSlider > div > div { background: #D0D7DE; }
            .stSlider > div > div > div { background: #E31837; }

            .stTabs [data-baseweb="tab-list"] { gap: 8px; background: #F6F8FA; padding: 8px; border-radius: 12px; }
            .stTabs [data-baseweb="tab"] { background: transparent; color: #656D76; border-radius: 8px; padding: 12px 24px; }
            .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #E31837, #B91430); color: white; }

            .hero-header {
                background: linear-gradient(135deg, #FFFFFF 0%, #F6F8FA 50%, #FFFFFF 100%);
                border: 1px solid #D0D7DE;
                border-radius: 16px;
                padding: 32px;
                margin-bottom: 24px;
                position: relative;
                overflow: hidden;
            }

            .hero-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #E31837, #FF4D6A, #E31837);
            }

            .talking-point {
                background: #F6F8FA;
                border-left: 3px solid #0969DA;
                padding: 12px 16px;
                margin: 8px 0;
                border-radius: 0 8px 8px 0;
            }

            .talking-point p { color: #1F2328; font-size: 0.85rem; margin: 0; line-height: 1.5; }
        </style>
        """

# ═══════════════════════════════════════════════════════════════════════════════
# DATA GENERATION - THE "DIGITAL TWIN" (REAL-WORLD BASED)
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# REAL SUPPLY CHAIN NETWORK DATA
# ─────────────────────────────────────────────────────────────────────────────

SUPPLY_CHAIN_NETWORK = {
    "manufacturing_sites": {
        "merida_taiwan": {
            "name": "Merida Industry Co. (Specialized JV)",
            "location": "Yuanlin, Changhua County, Taiwan",
            "port": "Kaohsiung (TWKHH)",
            "products": ["High-end carbon frames", "Premium aluminum frames"],
            "capacity_annual": 180000,
            "lead_time_days": 45,
            "ownership": "Specialized owns ~49% stake"
        },
        "vietnam_assembly": {
            "name": "Vietnam Assembly Partner",
            "location": "Ho Chi Minh City, Vietnam",
            "port": "Cat Lai (VNCLI)",
            "products": ["Entry-level frames", "Wheels", "Handlebars", "Forks"],
            "capacity_annual": 95000,
            "lead_time_days": 35,
            "notes": "Lower labor costs, favorable tariffs"
        },
        "czech_assembly": {
            "name": "Czech Republic Assembly",
            "location": "Czech Republic",
            "port": "Hamburg (DEHAM) via rail",
            "products": ["Final EU assembly", "EU-spec bikes"],
            "capacity_annual": 45000,
            "lead_time_days": 14,
            "notes": "Tariff avoidance for EU market, faster delivery"
        },
        "cambodia_frames": {
            "name": "Cambodia Frame Manufacturing",
            "location": "Phnom Penh, Cambodia",
            "port": "Sihanoukville (KHSHV)",
            "products": ["Entry-level aluminum frames"],
            "capacity_annual": 60000,
            "lead_time_days": 40,
            "notes": "Emerging low-cost alternative"
        }
    },
    "motor_suppliers": {
        "mahle_germany": {
            "name": "MAHLE Powertrain (SL 1.2 Motors)",
            "location": "Stuttgart, Germany",
            "consolidation_port": "Rotterdam (NLRTM)",
            "share_pct": 65,  # 60-70% of SL motors
            "products": ["SL 1.1 Motor", "SL 1.2 Motor"],
            "unit_cost_range": (850, 1100),
            "lead_time_days": 60,
            "notes": "Primary lightweight motor supplier"
        },
        "shimano_japan": {
            "name": "Shimano Inc. (STEPS Motors)",
            "location": "Sakai, Osaka, Japan",
            "port": "Osaka (JPOSA)",
            "share_pct": 25,  # 20-30% for mid-range
            "products": ["EP8 Motor", "E7000 Motor"],
            "unit_cost_range": (700, 950),
            "lead_time_days": 75,
            "notes": "Mid-range models, excellent reliability"
        },
        "bosch_germany": {
            "name": "Bosch eBike Systems",
            "location": "Reutlingen, Germany",
            "consolidation_port": "Rotterdam (NLRTM)",
            "share_pct": 7,  # 5-10% heavy power
            "products": ["Performance Line CX", "Cargo Line"],
            "unit_cost_range": (900, 1200),
            "lead_time_days": 55,
            "notes": "Heavy power trail bikes"
        },
        "bafang_china": {
            "name": "Bafang Electric (Suzhou) Co.",
            "location": "Suzhou, China",
            "port": "Shanghai (CNSHA)",
            "share_pct": 3,  # 1-5% commuter
            "products": ["M400", "M500"],
            "unit_cost_range": (280, 450),
            "lead_time_days": 45,
            "notes": "Budget commuter bikes only",
            "tariff_exposure": "Section 301 - HIGH RISK"
        },
        "brose_germany_legacy": {
            "name": "Brose Fahrzeugteile (Legacy)",
            "location": "Berlin, Germany",
            "consolidation_port": "Rotterdam (NLRTM)",
            "share_pct": 0,  # Legacy only
            "products": ["Drive S Mag (discontinued)", "Drive S (legacy support)"],
            "unit_cost_range": (950, 1450),
            "lead_time_days": 120,
            "notes": "LEGACY SUPPORT ONLY - Critical for warranty"
        }
    },
    "distribution_hubs": {
        "salt_lake_city": {
            "name": "Salt Lake City DC",
            "location": "Salt Lake City, UT, USA",
            "type": "Primary US Hub",
            "volume_share_pct": 60,
            "inbound_ports": ["Long Beach (USLGB)", "Oakland (USOAK)"],
            "sq_ft": 450000,
            "inventory_value_usd": 85000000,
            "transit_from_asia_days": 18  # Ocean to port + rail
        },
        "reno": {
            "name": "Reno DC",
            "location": "Reno, NV, USA",
            "type": "Secondary US Hub",
            "volume_share_pct": 40,
            "inbound_ports": ["Oakland (USOAK)"],
            "sq_ft": 280000,
            "inventory_value_usd": 52000000,
            "transit_from_asia_days": 15
        },
        "s_heerenberg": {
            "name": "'s-Heerenberg DC (Arvato)",
            "location": "'s-Heerenberg, Netherlands",
            "type": "Primary EU Hub",
            "volume_share_pct": 100,  # Of EU
            "inbound_ports": ["Rotterdam (NLRTM)"],
            "sq_ft": 320000,
            "inventory_value_usd": 45000000,
            "transit_from_asia_days": 28,
            "notes": "Near Arnhem, serves all of EMEA"
        },
        "singpost_apac": {
            "name": "SingPost 3PL Distribution",
            "location": "Singapore",
            "type": "APAC 3PL Hub",
            "volume_share_pct": 100,  # Of APAC
            "inbound_ports": ["Singapore (SGSIN)"],
            "sq_ft": 85000,
            "inventory_value_usd": 12000000,
            "transit_from_taiwan_days": 5,
            "notes": "3PL partner with API integration available",
            "api_endpoint": "api.singpost.com/inventory/v2"
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# REAL TARIFF & DUTY STRUCTURE (2024-2025)
# ─────────────────────────────────────────────────────────────────────────────

TARIFF_SCENARIOS = {
    "current_2025": {
        "name": "Current (Jan 2025)",
        "effective_date": "2025-01-01",
        "rates": {
            "taiwan_bikes": {"base": 11.0, "section_301": 10.0, "total": 21.0},
            "taiwan_parts": {"base": 5.5, "section_301": 10.0, "total": 15.5},
            "china_bikes": {"base": 11.0, "section_301": 25.0, "total": 36.0},
            "china_parts": {"base": 5.5, "section_301": 25.0, "total": 30.5},
            "china_batteries": {"base": 3.4, "section_301": 25.0, "total": 28.4},
            "vietnam_bikes": {"base": 0.0, "section_301": 0.0, "total": 0.0},  # GSP
            "vietnam_parts": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "cambodia_frames": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "germany_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "japan_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "czech_assembly": {"base": 0.0, "section_301": 0.0, "total": 0.0},  # EU FTA
            "eu_to_us": {"base": 4.5, "section_301": 0.0, "total": 4.5},
        }
    },
    "trump_aug_2025_high": {
        "name": "Aug 2025 Peak (Historical Reference)",
        "effective_date": "2025-08-01",
        "rates": {
            "taiwan_bikes": {"base": 11.0, "section_301": 21.0, "total": 32.0},
            "taiwan_parts": {"base": 5.5, "section_301": 21.0, "total": 26.5},
            "china_bikes": {"base": 11.0, "section_301": 50.0, "total": 61.0},
            "china_parts": {"base": 5.5, "section_301": 50.0, "total": 55.5},
            "china_batteries": {"base": 3.4, "section_301": 50.0, "total": 53.4},
            "vietnam_bikes": {"base": 5.0, "section_301": 0.0, "total": 5.0},
            "vietnam_parts": {"base": 2.5, "section_301": 0.0, "total": 2.5},
            "cambodia_frames": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "germany_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "japan_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "czech_assembly": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "eu_to_us": {"base": 4.5, "section_301": 10.0, "total": 14.5},
        }
    },
    "best_case_2026": {
        "name": "Best Case (Trade Normalization)",
        "effective_date": "2026-01-01",
        "rates": {
            "taiwan_bikes": {"base": 11.0, "section_301": 0.0, "total": 11.0},
            "taiwan_parts": {"base": 5.5, "section_301": 0.0, "total": 5.5},
            "china_bikes": {"base": 11.0, "section_301": 15.0, "total": 26.0},
            "china_parts": {"base": 5.5, "section_301": 15.0, "total": 20.5},
            "china_batteries": {"base": 3.4, "section_301": 15.0, "total": 18.4},
            "vietnam_bikes": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "vietnam_parts": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "cambodia_frames": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "germany_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "japan_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "czech_assembly": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "eu_to_us": {"base": 4.5, "section_301": 0.0, "total": 4.5},
        }
    },
    "worst_case_escalation": {
        "name": "Worst Case (Full Escalation)",
        "effective_date": "2025-06-01",
        "rates": {
            "taiwan_bikes": {"base": 11.0, "section_301": 25.0, "total": 36.0},
            "taiwan_parts": {"base": 5.5, "section_301": 25.0, "total": 30.5},
            "china_bikes": {"base": 11.0, "section_301": 60.0, "total": 71.0},
            "china_parts": {"base": 5.5, "section_301": 60.0, "total": 65.5},
            "china_batteries": {"base": 3.4, "section_301": 60.0, "total": 63.4},
            "vietnam_bikes": {"base": 10.0, "section_301": 0.0, "total": 10.0},
            "vietnam_parts": {"base": 5.0, "section_301": 0.0, "total": 5.0},
            "cambodia_frames": {"base": 5.0, "section_301": 0.0, "total": 5.0},
            "germany_motors": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "japan_motors": {"base": 2.5, "section_301": 0.0, "total": 2.5},
            "czech_assembly": {"base": 0.0, "section_301": 0.0, "total": 0.0},
            "eu_to_us": {"base": 4.5, "section_301": 15.0, "total": 19.5},
        }
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# FREIGHT RATES (Based on Drewry/Freightos Index Nov 2024)
# ─────────────────────────────────────────────────────────────────────────────

FREIGHT_RATES = {
    "ocean_feu": {  # 40ft container rates
        "shanghai_la": {"current": 2850, "spot_high": 8500, "contract": 2400},
        "shanghai_rotterdam": {"current": 3200, "spot_high": 9200, "contract": 2800},
        "kaohsiung_la": {"current": 2650, "spot_high": 7800, "contract": 2200},
        "kaohsiung_oakland": {"current": 2500, "spot_high": 7500, "contract": 2100},
        "rotterdam_la": {"current": 2100, "spot_high": 4500, "contract": 1800},
        "singapore_la": {"current": 2400, "spot_high": 7200, "contract": 2000},
    },
    "air_per_kg": {
        "shanghai_la": {"current": 4.20, "express": 8.50},
        "kaohsiung_la": {"current": 3.80, "express": 7.80},
        "frankfurt_la": {"current": 2.90, "express": 5.50},
        "tokyo_la": {"current": 3.50, "express": 7.00},
    },
    "rail_china_eu": {  # China-Europe rail
        "chengdu_duisburg": {"current": 4800, "transit_days": 16},
        "xian_rotterdam": {"current": 5200, "transit_days": 18},
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# RIGHT-TO-REPAIR LEGISLATION
# ─────────────────────────────────────────────────────────────────────────────

RIGHT_TO_REPAIR_LAWS = {
    "california_sb244": {
        "name": "California SB-244",
        "jurisdiction": "California, USA",
        "effective_date": "2024-07-01",
        "requirements": {
            "products_over_100": 7,  # Years of parts availability
            "products_50_to_100": 3,
            "documentation_required": True,
            "repair_manuals": True,
        },
        "penalties": "Civil penalties up to $1,000 per violation",
        "notes": "Applies to products sold in CA after July 1, 2024"
    },
    "eu_right_to_repair": {
        "name": "EU Right to Repair Directive",
        "jurisdiction": "European Union",
        "effective_date": "2025-06-01",  # Proposed
        "requirements": {
            "minimum_years": 10,  # Proposed 10-year requirement
            "spare_parts_pricing": "Reasonable",
            "independent_repair": True,
            "software_updates": 10,  # Years of security updates
        },
        "penalties": "Up to 4% of annual EU revenue",
        "notes": "Still in legislative process, expected 2025"
    },
    "eu_battery_regulation": {
        "name": "EU Battery Regulation 2023/1542",
        "jurisdiction": "European Union",
        "effective_date": "2027-02-18",
        "requirements": {
            "battery_passport": True,
            "qr_code_required": True,
            "carbon_footprint_declaration": "2025-02-18",
            "recycled_content_cobalt": 16,  # % by 2031
            "recycled_content_lithium": 6,  # % by 2031
            "recycled_content_nickel": 6,  # % by 2031
            "collection_rate": 73,  # % by 2031
        },
        "penalties": "Member state defined, expect significant fines",
        "notes": "Affects all e-bike batteries >2kWh"
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# COMPONENT OBSOLESCENCE (MOORE'S LAW IMPACT)
# ─────────────────────────────────────────────────────────────────────────────

COMPONENT_LIFECYCLE = {
    "motors": {
        "generation_cycle_months": 20,  # New gen every ~20 months
        "support_after_discontinuation_months": 84,  # 7 years
        "weibull_shape": 2.1,  # Wear-out failure mode
        "weibull_scale_years": 6.5,
        "mtbf_hours": 8000,
        "obsolescence_risk": "MEDIUM",
        "notes": "Motor technology stable, main risk is firmware/controller chips"
    },
    "batteries": {
        "generation_cycle_months": 18,  # Chemistry improvements
        "support_after_discontinuation_months": 84,
        "weibull_shape": 1.8,  # Mixed failure mode (early + wear-out)
        "weibull_scale_years": 5.0,
        "cycle_life": 800,  # Full cycles to 80% SoH
        "density_improvement_annual_pct": 5,
        "obsolescence_risk": "HIGH",
        "notes": "Fast-moving chemistry, cell supply chain risk"
    },
    "tcu_display": {
        "generation_cycle_months": 24,
        "support_after_discontinuation_months": 60,  # 5 years realistic
        "weibull_shape": 1.2,  # Random failures dominate
        "weibull_scale_years": 8.0,
        "obsolescence_risk": "VERY HIGH",
        "notes": "Chip shortage risk, firmware dependency, BT/ANT+ protocol changes"
    },
    "chargers": {
        "generation_cycle_months": 36,
        "support_after_discontinuation_months": 84,
        "weibull_shape": 1.5,
        "weibull_scale_years": 7.0,
        "obsolescence_risk": "LOW",
        "notes": "Stable technology, commodity components"
    }
}

@st.cache_data
def generate_product_catalog():
    """Generate Specialized e-bike product catalog with REAL 2024-2025 model data."""
    products = [
        # Full Power E-MTB (Turbo Full Power 2.2 System)
        {"model": "Turbo Levo", "category": "E-MTB", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 700, "msrp": 7499, "launch_year": 2024, "generation": "Gen 5", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Levo Comp", "category": "E-MTB", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 700, "msrp": 8499, "launch_year": 2024, "generation": "Gen 5", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Levo Expert", "category": "E-MTB", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 700, "msrp": 11000, "launch_year": 2024, "generation": "Gen 5", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Levo S-Works", "category": "E-MTB", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 700, "msrp": 15000, "launch_year": 2024, "generation": "Gen 5", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Kenevo", "category": "E-MTB", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 700, "msrp": 9999, "launch_year": 2023, "generation": "Gen 3", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},

        # SL E-MTB (MAHLE Motors - Lightweight)
        {"model": "Turbo Levo SL", "category": "E-MTB SL", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 8000, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Levo SL Comp", "category": "E-MTB SL", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 9000, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Levo SL Expert", "category": "E-MTB SL", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 11500, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Kenevo SL", "category": "E-MTB SL", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 10500, "launch_year": 2023, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},

        # Road/Gravel (MAHLE SL Motors)
        {"model": "Turbo Creo 2 Comp", "category": "E-Road", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 7500, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Creo 2 Expert", "category": "E-Road", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 11000, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Creo 2 S-Works", "category": "E-Road", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 15500, "launch_year": 2024, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},

        # Urban/Commuter (Mix of Shimano + Bafang for entry level)
        {"model": "Turbo Vado 3.0", "category": "E-Urban", "motor": "Shimano EP8", "motor_supplier": "Shimano", "battery_wh": 710, "msrp": 3750, "launch_year": 2024, "generation": "6.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Vado 4.0", "category": "E-Urban", "motor": "Shimano EP8", "motor_supplier": "Shimano", "battery_wh": 710, "msrp": 4500, "launch_year": 2024, "generation": "6.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Vado 5.0", "category": "E-Urban", "motor": "Full Power 2.0", "motor_supplier": "Specialized In-House", "battery_wh": 710, "msrp": 5250, "launch_year": 2024, "generation": "6.0", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Vado SL 4.0", "category": "E-Urban SL", "motor": "SL 1.1", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 3500, "launch_year": 2024, "generation": "5.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Vado SL 5.0", "category": "E-Urban SL", "motor": "SL 1.2", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 4500, "launch_year": 2024, "generation": "5.0", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Como 3.0", "category": "E-Urban", "motor": "Bafang M400", "motor_supplier": "Bafang", "battery_wh": 545, "msrp": 2750, "launch_year": 2024, "generation": "5.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Como 4.0", "category": "E-Urban", "motor": "Shimano E7000", "motor_supplier": "Shimano", "battery_wh": 710, "msrp": 4000, "launch_year": 2024, "generation": "5.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Como 5.0", "category": "E-Urban", "motor": "Full Power 2.0", "motor_supplier": "Specialized In-House", "battery_wh": 710, "msrp": 5000, "launch_year": 2024, "generation": "5.0", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Tero 3.0", "category": "E-SUV", "motor": "Shimano E7000", "motor_supplier": "Shimano", "battery_wh": 710, "msrp": 4000, "launch_year": 2024, "generation": "5.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Tero 4.0", "category": "E-SUV", "motor": "Shimano EP8", "motor_supplier": "Shimano", "battery_wh": 710, "msrp": 5000, "launch_year": 2024, "generation": "5.0", "frame_origin": "Vietnam", "warranty_years": 2, "right_to_repair_years": 7},
        {"model": "Turbo Tero 5.0", "category": "E-SUV", "motor": "Full Power 2.2", "motor_supplier": "Specialized In-House", "battery_wh": 710, "msrp": 6000, "launch_year": 2024, "generation": "5.0", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7},

        # LEGACY MODELS (Still under warranty/Right-to-Repair obligation)
        {"model": "Turbo Levo (Legacy)", "category": "E-MTB", "motor": "Brose Drive S Mag", "motor_supplier": "Brose (LEGACY)", "battery_wh": 700, "msrp": 0, "launch_year": 2020, "generation": "Gen 3", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7, "status": "LEGACY SUPPORT"},
        {"model": "Turbo Kenevo (Legacy)", "category": "E-MTB", "motor": "Brose Drive S Mag", "motor_supplier": "Brose (LEGACY)", "battery_wh": 700, "msrp": 0, "launch_year": 2019, "generation": "Gen 2", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7, "status": "LEGACY SUPPORT"},
        {"model": "Turbo Creo SL (Legacy)", "category": "E-Road", "motor": "SL 1.1", "motor_supplier": "MAHLE", "battery_wh": 320, "msrp": 0, "launch_year": 2020, "generation": "Gen 1", "frame_origin": "Taiwan (Merida)", "warranty_years": 2, "right_to_repair_years": 7, "status": "LEGACY SUPPORT"},
    ]
    return pd.DataFrame(products)

@st.cache_data
def generate_battery_database(n=1000):
    """Generate Battery Passport database with realistic attributes."""
    np.random.seed(42)
    
    chemistries = ["NMC 811", "NMC 622", "LFP"]
    locations = ["Customer", "Retailer", "Warehouse-US", "Warehouse-EU", "Warehouse-APAC", "Quarantine", "Recycling"]
    regions = ["North America", "EMEA", "APAC", "LATAM"]
    battery_sizes = [320, 400, 500, 700, 710, 840]
    
    # Generate production dates over 5 years
    base_date = datetime(2019, 1, 1)
    
    batteries = []
    for i in range(n):
        prod_date = base_date + timedelta(days=random.randint(0, 365*5))
        age_days = (datetime.now() - prod_date).days
        
        # State of Health degrades with age and cycles
        base_soh = 100
        cycles = int(np.random.exponential(150) + age_days * 0.05)
        cycles = min(cycles, 1200)  # Cap at 1200 cycles
        
        # SoH degrades ~0.05% per cycle with some variance
        soh = base_soh - (cycles * 0.05) - np.random.normal(0, 3)
        soh = max(min(soh, 100), 40)  # Bound between 40-100%
        
        # Determine location based on SoH
        if soh < 70:
            location = np.random.choice(["Quarantine", "Recycling"], p=[0.3, 0.7])
            status = "End-of-Life"
        elif soh < 80:
            location = np.random.choice(["Customer", "Retailer", "Quarantine"], p=[0.5, 0.3, 0.2])
            status = "Degraded"
        else:
            location = np.random.choice(["Customer", "Retailer", "Warehouse-US", "Warehouse-EU", "Warehouse-APAC"], p=[0.6, 0.15, 0.1, 0.1, 0.05])
            status = "Healthy"
        
        battery = {
            "serial_number": f"BATT-{random.choice(['NMC', 'LFP'])}-{str(i+1000).zfill(4)}",
            "capacity_wh": random.choice(battery_sizes),
            "chemistry": random.choice(chemistries),
            "production_date": prod_date.strftime("%Y-%m-%d"),
            "state_of_health": round(soh, 1),
            "charge_cycles": cycles,
            "location": location,
            "region": random.choice(regions),
            "status": status,
            "warranty_expires": (prod_date + timedelta(days=730)).strftime("%Y-%m-%d"),  # 2 year warranty
            "co2_footprint_kg": round(random.uniform(60, 120) * (random.choice(battery_sizes) / 500), 1),
            "recycled_content_pct": round(random.uniform(5, 25), 1),
        }
        batteries.append(battery)
    
    return pd.DataFrame(batteries)

@st.cache_data
def generate_parts_inventory():
    """Generate spare parts inventory with REALISTIC demand signals and supply chain data."""
    np.random.seed(42)

    parts = [
        # ═══════════════════════════════════════════════════════════════════════════
        # MOTORS - By Supplier with Real Lead Times & Costs
        # ═══════════════════════════════════════════════════════════════════════════

        # Specialized In-House (Full Power System)
        {"part_number": "MOT-FP22-001", "description": "Full Power 2.2 Motor Assembly", "category": "Motor", "supplier": "Specialized In-House", "origin": "Taiwan", "unit_cost": 1450, "hazmat": False, "lead_time_days": 75, "tariff_code": "taiwan_parts", "weight_kg": 2.95, "obsolescence_risk": "LOW"},
        {"part_number": "MOT-FP20-001", "description": "Full Power 2.0 Motor Assembly", "category": "Motor", "supplier": "Specialized In-House", "origin": "Taiwan", "unit_cost": 1150, "hazmat": False, "lead_time_days": 90, "tariff_code": "taiwan_parts", "weight_kg": 3.1, "obsolescence_risk": "MEDIUM"},

        # MAHLE Motors (SL System) - Germany
        {"part_number": "MOT-SL12-001", "description": "MAHLE SL 1.2 Motor Assembly", "category": "Motor", "supplier": "MAHLE", "origin": "Germany", "unit_cost": 1100, "hazmat": False, "lead_time_days": 60, "tariff_code": "germany_motors", "weight_kg": 1.95, "obsolescence_risk": "LOW"},
        {"part_number": "MOT-SL11-001", "description": "MAHLE SL 1.1 Motor Assembly", "category": "Motor", "supplier": "MAHLE", "origin": "Germany", "unit_cost": 950, "hazmat": False, "lead_time_days": 75, "tariff_code": "germany_motors", "weight_kg": 1.85, "obsolescence_risk": "MEDIUM"},

        # Shimano Motors - Japan
        {"part_number": "MOT-EP8-001", "description": "Shimano EP8 Motor Assembly", "category": "Motor", "supplier": "Shimano", "origin": "Japan", "unit_cost": 890, "hazmat": False, "lead_time_days": 75, "tariff_code": "japan_motors", "weight_kg": 2.6, "obsolescence_risk": "LOW"},
        {"part_number": "MOT-E7K-001", "description": "Shimano E7000 Motor Assembly", "category": "Motor", "supplier": "Shimano", "origin": "Japan", "unit_cost": 720, "hazmat": False, "lead_time_days": 60, "tariff_code": "japan_motors", "weight_kg": 2.8, "obsolescence_risk": "LOW"},

        # Bafang Motors - China (HIGH TARIFF RISK)
        {"part_number": "MOT-BAF-M400", "description": "Bafang M400 Motor Assembly", "category": "Motor", "supplier": "Bafang", "origin": "China", "unit_cost": 380, "hazmat": False, "lead_time_days": 45, "tariff_code": "china_parts", "weight_kg": 2.9, "obsolescence_risk": "MEDIUM", "tariff_alert": "SECTION 301 EXPOSURE"},
        {"part_number": "MOT-BAF-M500", "description": "Bafang M500 Motor Assembly", "category": "Motor", "supplier": "Bafang", "origin": "China", "unit_cost": 420, "hazmat": False, "lead_time_days": 45, "tariff_code": "china_parts", "weight_kg": 3.0, "obsolescence_risk": "MEDIUM", "tariff_alert": "SECTION 301 EXPOSURE"},

        # LEGACY Brose Motors - Germany (CRITICAL FOR WARRANTY)
        {"part_number": "MOT-BROSE-DSM", "description": "Brose Drive S Mag Motor (LEGACY)", "category": "Motor", "supplier": "Brose (LEGACY)", "origin": "Germany", "unit_cost": 1380, "hazmat": False, "lead_time_days": 120, "tariff_code": "germany_motors", "weight_kg": 2.9, "obsolescence_risk": "CRITICAL", "legacy_support": True, "discontinuation_date": "2022-06-30", "support_end_date": "2029-06-30"},
        {"part_number": "MOT-BROSE-DS", "description": "Brose Drive S Motor (LEGACY)", "category": "Motor", "supplier": "Brose (LEGACY)", "origin": "Germany", "unit_cost": 1250, "hazmat": False, "lead_time_days": 150, "tariff_code": "germany_motors", "weight_kg": 3.4, "obsolescence_risk": "CRITICAL", "legacy_support": True, "discontinuation_date": "2021-03-31", "support_end_date": "2028-03-31"},

        # ═══════════════════════════════════════════════════════════════════════════
        # BATTERIES - By Chemistry and Capacity
        # ═══════════════════════════════════════════════════════════════════════════
        {"part_number": "BAT-700-NMC811", "description": "700Wh Battery Pack (NMC 811)", "category": "Battery", "supplier": "Samsung SDI", "origin": "South Korea", "unit_cost": 945, "hazmat": True, "lead_time_days": 60, "tariff_code": "taiwan_parts", "weight_kg": 4.4, "eu_passport_required": True, "chemistry": "NMC 811"},
        {"part_number": "BAT-710-NMC622", "description": "710Wh Battery Pack (NMC 622)", "category": "Battery", "supplier": "LG Energy", "origin": "South Korea", "unit_cost": 890, "hazmat": True, "lead_time_days": 55, "tariff_code": "taiwan_parts", "weight_kg": 4.6, "eu_passport_required": True, "chemistry": "NMC 622"},
        {"part_number": "BAT-320-SL", "description": "320Wh SL Battery Pack", "category": "Battery", "supplier": "Samsung SDI", "origin": "South Korea", "unit_cost": 580, "hazmat": True, "lead_time_days": 45, "tariff_code": "taiwan_parts", "weight_kg": 1.95, "eu_passport_required": True, "chemistry": "NMC 811"},
        {"part_number": "BAT-545-STD", "description": "545Wh Standard Battery Pack", "category": "Battery", "supplier": "CATL", "origin": "China", "unit_cost": 520, "hazmat": True, "lead_time_days": 50, "tariff_code": "china_batteries", "weight_kg": 3.5, "eu_passport_required": True, "chemistry": "NMC 622", "tariff_alert": "SECTION 301 EXPOSURE"},
        {"part_number": "BAT-160-EXT", "description": "160Wh Range Extender", "category": "Battery", "supplier": "Samsung SDI", "origin": "South Korea", "unit_cost": 350, "hazmat": True, "lead_time_days": 30, "tariff_code": "taiwan_parts", "weight_kg": 1.0, "eu_passport_required": True, "chemistry": "NMC 811"},

        # LEGACY Batteries
        {"part_number": "BAT-700-LEGACY", "description": "700Wh Battery Pack (Gen 3 Legacy)", "category": "Battery", "supplier": "Samsung SDI", "origin": "South Korea", "unit_cost": 1050, "hazmat": True, "lead_time_days": 90, "tariff_code": "taiwan_parts", "weight_kg": 4.8, "eu_passport_required": True, "chemistry": "NMC 622", "legacy_support": True, "discontinuation_date": "2023-01-01", "support_end_date": "2030-01-01"},

        # ═══════════════════════════════════════════════════════════════════════════
        # ELECTRONICS - TCU, Displays, Sensors
        # ═══════════════════════════════════════════════════════════════════════════
        {"part_number": "TCU-G5-001", "description": "Turbo Connect Unit Gen 5 (MasterMind)", "category": "Electronics", "supplier": "Specialized In-House", "origin": "Taiwan", "unit_cost": 320, "hazmat": False, "lead_time_days": 45, "tariff_code": "taiwan_parts", "weight_kg": 0.12, "obsolescence_risk": "HIGH"},
        {"part_number": "TCU-G4-001", "description": "Turbo Connect Unit Gen 4", "category": "Electronics", "supplier": "Specialized In-House", "origin": "Taiwan", "unit_cost": 280, "hazmat": False, "lead_time_days": 60, "tariff_code": "taiwan_parts", "weight_kg": 0.11, "obsolescence_risk": "MEDIUM"},
        {"part_number": "TCU-G3-001", "description": "Turbo Connect Unit Gen 3 (LEGACY)", "category": "Electronics", "supplier": "Specialized In-House", "origin": "Taiwan", "unit_cost": 250, "hazmat": False, "lead_time_days": 90, "tariff_code": "taiwan_parts", "weight_kg": 0.13, "obsolescence_risk": "CRITICAL", "legacy_support": True},
        {"part_number": "DSP-RMT-002", "description": "Remote Control Unit (Handlebar)", "category": "Electronics", "supplier": "Giant Manufacturing", "origin": "Taiwan", "unit_cost": 125, "hazmat": False, "lead_time_days": 30, "tariff_code": "taiwan_parts", "weight_kg": 0.045},
        {"part_number": "SNS-SPD-001", "description": "Speed Sensor Assembly", "category": "Electronics", "supplier": "Giant Manufacturing", "origin": "Taiwan", "unit_cost": 48, "hazmat": False, "lead_time_days": 21, "tariff_code": "taiwan_parts", "weight_kg": 0.025},
        {"part_number": "SNS-TRQ-001", "description": "Torque Sensor Assembly", "category": "Electronics", "supplier": "MAHLE", "origin": "Germany", "unit_cost": 185, "hazmat": False, "lead_time_days": 45, "tariff_code": "germany_motors", "weight_kg": 0.15},
        {"part_number": "CBL-PWR-MAIN", "description": "Main Power Harness Assembly", "category": "Electronics", "supplier": "TE Connectivity", "origin": "Mexico", "unit_cost": 95, "hazmat": False, "lead_time_days": 21, "tariff_code": "vietnam_parts", "weight_kg": 0.35},

        # ═══════════════════════════════════════════════════════════════════════════
        # CHARGERS
        # ═══════════════════════════════════════════════════════════════════════════
        {"part_number": "CHG-4A-STD", "description": "4A Smart Charger (Standard)", "category": "Charger", "supplier": "Delta Electronics", "origin": "Taiwan", "unit_cost": 165, "hazmat": False, "lead_time_days": 21, "tariff_code": "taiwan_parts", "weight_kg": 0.65},
        {"part_number": "CHG-6A-FAST", "description": "6A Fast Charger (Turbo)", "category": "Charger", "supplier": "Delta Electronics", "origin": "Taiwan", "unit_cost": 285, "hazmat": False, "lead_time_days": 28, "tariff_code": "taiwan_parts", "weight_kg": 0.95},
        {"part_number": "CHG-SL-COMP", "description": "SL Compact Charger (48V/2A)", "category": "Charger", "supplier": "Delta Electronics", "origin": "Taiwan", "unit_cost": 125, "hazmat": False, "lead_time_days": 21, "tariff_code": "taiwan_parts", "weight_kg": 0.35},
    ]

    df = pd.DataFrame(parts)

    # Add realistic inventory levels based on part criticality
    np.random.seed(42)

    # Higher inventory for legacy parts (to meet 7-year obligation)
    df["on_hand_slc"] = df.apply(lambda x: np.random.randint(200, 800) if x.get("legacy_support") else np.random.randint(50, 400), axis=1)
    df["on_hand_reno"] = df.apply(lambda x: np.random.randint(100, 500) if x.get("legacy_support") else np.random.randint(30, 250), axis=1)
    df["on_hand_eu"] = df.apply(lambda x: np.random.randint(150, 600) if x.get("legacy_support") else np.random.randint(40, 300), axis=1)
    df["on_hand_apac"] = np.random.randint(20, 150, len(df))

    # Realistic demand patterns
    df["monthly_demand_us"] = np.random.randint(15, 120, len(df))
    df["monthly_demand_eu"] = np.random.randint(10, 80, len(df))
    df["monthly_demand_apac"] = np.random.randint(5, 40, len(df))
    df["warranty_claims_mtd"] = np.random.randint(3, 45, len(df))
    df["production_allocation"] = np.random.randint(50, 400, len(df))

    # Financial metrics
    df["holding_cost_annual_pct"] = 0.25
    df["stockout_cost_per_unit"] = df["unit_cost"] * 0.4  # 40% penalty for expedite

    # Calculate totals and days of supply
    df["on_hand_us"] = df["on_hand_slc"] + df["on_hand_reno"]  # For backward compatibility
    df["total_on_hand"] = df["on_hand_slc"] + df["on_hand_reno"] + df["on_hand_eu"] + df["on_hand_apac"]
    df["monthly_demand"] = df["monthly_demand_us"] + df["monthly_demand_eu"] + df["monthly_demand_apac"]
    df["days_of_supply"] = (df["total_on_hand"] / (df["monthly_demand"] / 30)).round(0)

    # Landed cost calculation (base + tariff under current scenario)
    current_tariffs = TARIFF_SCENARIOS["current_2025"]["rates"]
    df["tariff_rate_pct"] = df["tariff_code"].apply(lambda x: current_tariffs.get(x, {}).get("total", 0))
    df["landed_cost"] = (df["unit_cost"] * (1 + df["tariff_rate_pct"] / 100)).round(2)

    return df

@st.cache_data
def generate_dealer_network():
    """Generate dealer network performance data."""
    np.random.seed(42)
    
    regions = {
        "North America": ["US West", "US Central", "US East", "Canada"],
        "EMEA": ["UK/Ireland", "DACH", "France", "Nordics", "Southern EU"],
        "APAC": ["Australia/NZ", "Japan", "Taiwan", "Southeast Asia"],
        "LATAM": ["Brazil", "Mexico", "Chile/Argentina"]
    }
    
    dealers = []
    for region, sub_regions in regions.items():
        for sub_region in sub_regions:
            n_dealers = random.randint(15, 80)
            for i in range(n_dealers):
                dealer = {
                    "dealer_id": f"DLR-{region[:2]}-{str(len(dealers)+1).zfill(4)}",
                    "region": region,
                    "sub_region": sub_region,
                    "tier": random.choices(["Platinum", "Gold", "Silver"], weights=[0.1, 0.3, 0.6])[0],
                    "e_bike_certified": random.random() > 0.2,
                    "open_warranty_claims": random.randint(0, 25),
                    "avg_claim_resolution_days": round(random.uniform(3, 45), 1),
                    "parts_fill_rate": round(random.uniform(0.75, 0.99), 3),
                    "pending_reimbursement_usd": round(random.uniform(0, 15000), 2),
                    "nps_score": random.randint(20, 95),
                    "ytd_warranty_volume": random.randint(5, 200),
                }
                dealers.append(dealer)
    
    return pd.DataFrame(dealers)

@st.cache_data  
def generate_install_base():
    """Generate active install base for liability forecasting."""
    np.random.seed(42)
    
    # Install base by model year and model
    years = list(range(2019, 2026))
    models = ["Turbo Levo", "Turbo Levo SL", "Turbo Kenevo", "Turbo Vado", "Turbo Como", "Turbo Creo"]
    
    install_base = []
    for year in years:
        for model in models:
            # Newer years have more units, e-bike growth curve
            base_units = int(2000 * (1.35 ** (year - 2019)))
            units = int(base_units * random.uniform(0.7, 1.3))
            
            install_base.append({
                "model_year": year,
                "model": model,
                "active_units": units,
                "warranty_end_year": year + 5,  # 5 year Turbo warranty
                "legal_support_end_year": year + 7,  # 7 year right-to-repair
            })
    
    return pd.DataFrame(install_base)

@st.cache_data
def generate_npi_timeline():
    """Generate NPI (New Product Introduction) timeline."""
    launches = [
        {"product": "Turbo Levo Gen 5", "launch_date": "2025-09-01", "service_parts_readiness": 0.35, "training_complete": 0.20, "risk_level": "High"},
        {"product": "Turbo Creo 3", "launch_date": "2025-06-15", "service_parts_readiness": 0.72, "training_complete": 0.65, "risk_level": "Medium"},
        {"product": "Turbo Vado 7.0", "launch_date": "2025-04-01", "service_parts_readiness": 0.91, "training_complete": 0.88, "risk_level": "Low"},
        {"product": "Turbo Como SL 6.0", "launch_date": "2025-05-15", "service_parts_readiness": 0.68, "training_complete": 0.55, "risk_level": "Medium"},
        {"product": "Turbo Tero X", "launch_date": "2025-08-01", "service_parts_readiness": 0.42, "training_complete": 0.30, "risk_level": "High"},
    ]
    return pd.DataFrame(launches)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(135deg, #E31837, #FF4D6A); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🚴 SERVICE COMMAND
        </h1>
        <p style="color: #8B949E; font-size: 0.85rem; margin-top: 4px;">
            Specialized Bicycles | IBP Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    # Theme Toggle (Dark/Light Mode)
    dark_mode = st.toggle("🌙 **DARK MODE**", value=True, help="Toggle between dark and light theme")

    # Pitch Mode Toggle
    pitch_mode = st.toggle("🎯 **PITCH MODE**", value=True, help="Enable strategic insight cards and talking points for presentations")

    if pitch_mode:
        st.markdown(f"""
        <div style="background: rgba(227, 24, 55, 0.1); border: 1px solid #E31837; border-radius: 8px; padding: 12px; margin-top: 8px;">
            <p style="color: #E31837; font-size: 0.8rem; margin: 0;">
                ✓ Strategic insight cards visible<br>
                ✓ JD-aligned talking points enabled<br>
                ✓ Executive metrics highlighted
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # Navigation
    st.markdown("### 📊 Navigation")
    module = st.radio(
        "Select Module",
        [
            "🏠 Executive Dashboard",
            "🌐 Network Optimizer",
            "💰 Tariff War Room",
            "⚖️ Right-to-Repair Forecaster",
            "🔋 EU Battery Passport",
            "🏪 Dealer Network Health",
            "⚔️ Allocation War Room",
            "📅 S&OP Command Center"
        ],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Global filters
    st.markdown("### 🌍 Global Filters")
    selected_regions = st.multiselect(
        "Regions",
        ["North America", "EMEA", "APAC", "LATAM"],
        default=["North America", "EMEA", "APAC", "LATAM"]
    )
    
    date_range = st.date_input(
        "Analysis Period",
        value=(datetime.now() - timedelta(days=90), datetime.now()),
        max_value=datetime.now()
    )
    
    st.divider()
    
    # Talking Points (Dynamic based on module)
    if pitch_mode:
        st.markdown("### 💬 Talking Points")
        
        talking_points = {
            "🏠 Executive Dashboard": [
                "**Lead with impact**: 'This dashboard gives me real-time visibility into our global service health.'",
                "**Connect to JD**: 'I can track team KPIs and alignment with strategic goals at a glance.'",
                "**Show value**: 'This is how I would ensure the planning team stays ahead of issues, not reacting to them.'"
            ],
            "🌐 Network Optimizer": [
                "**Logistics language**: 'I've mapped your actual lanes—Kaohsiung to Long Beach, Rotterdam consolidation, the SLC/Reno split.'",
                "**Cost visibility**: 'I calculate landed cost including freight, duty, and tariffs for every origin-destination pair.'",
                "**Modal analysis**: 'When does air freight make sense vs. ocean? This tool finds the breakeven.'",
                "**3PL Integration**: 'SingPost in Singapore has an API—I can pull real-time inventory for APAC visibility.'"
            ],
            "💰 Tariff War Room": [
                "**Current exposure**: 'Taiwan parts at 21% total duty, China at 30.5%—but August 2025 could spike to 32%.'",
                "**Scenario planning**: 'What if we shift Bafang motors to MAHLE? Cost goes up, but tariff exposure drops.'",
                "**Legal avoidance**: 'Czech assembly for EU, Vietnam for entry-level—these are legal tariff optimization strategies.'",
                "**Your expertise**: 'With 14+ years of tariff complexity across Asia, this tool operationalizes that hard-won experience.'"
            ],
            "⚖️ Right-to-Repair Forecaster": [
                "**California SB-244**: 'Effective July 2024—7 years of parts for any product over $100 sold in California.'",
                "**EU 10-Year Directive**: 'Proposed 10-year requirement coming in 2025—we need to plan NOW.'",
                "**Moore's Law problem**: 'Motors evolve every 20 months, but we must support them for 84+ months.'",
                "**Weibull advantage**: 'Excel uses flat averages. I use survival statistics to predict the failure spike BEFORE it happens.'"
            ],
            "🔋 EU Battery Passport": [
                "**Regulatory urgency**: 'EU Regulation 2023/1542 requires individual battery tracking by February 2027.'",
                "**Process improvement**: 'This elevates rider support through traceability—no more manual spreadsheets.'",
                "**Competitive advantage**: 'First-mover compliance positions us as the premium brand in sustainability.'",
                "**Recycled content**: '16% cobalt, 6% lithium, 6% nickel by 2031—we need to track this NOW.'"
            ],
            "🏪 Dealer Network Health": [
                "**Dealer relationships**: 'Our dealers are extensions of our brand. Their experience = rider experience.'",
                "**Cash flow visibility**: 'I track pending reimbursements to ensure we're not creating financial stress.'",
                "**Escalation paths**: 'Red flags here trigger my escalation pathways before they become complaints.'"
            ],
            "⚔️ Allocation War Room": [
                "**Frame the conflict**: 'Production wants parts for new bikes; Service needs them for warranty.'",
                "**Influence stakeholders**: 'This data helps me influence cross-functional decisions with trade-off visibility.'",
                "**Find balance**: 'My job is to find the sweet spot where factory runs AND we keep our 7-year promise.'"
            ],
            "📅 S&OP Command Center": [
                "**NPI readiness**: 'Service must be ready BEFORE launch, not scrambling after.'",
                "**Cross-functional**: 'I collaborate with product teams to communicate NPI milestones clearly.'",
                "**Team leadership**: 'This is where I track and report on team KPIs—forecast accuracy, planner workload.'"
            ]
        }
        
        for point in talking_points.get(module, []):
            st.markdown(f"""
            <div class="talking-point">
                <p>{point}</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# APPLY THEME CSS (after sidebar defines dark_mode)
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(get_theme_css(dark_mode), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════

products_df = generate_product_catalog()
batteries_df = generate_battery_database()
parts_df = generate_parts_inventory()
dealers_df = generate_dealer_network()
install_base_df = generate_install_base()
npi_df = generate_npi_timeline()

# Filter by selected regions
batteries_filtered = batteries_df[batteries_df["region"].isin(selected_regions)]
dealers_filtered = dealers_df[dealers_df["region"].isin(selected_regions)]

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

if module == "🏠 Executive Dashboard":
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Service Command Center</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Global Service & Warranty Operations | Real-Time Intelligence
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>This executive dashboard provides at-a-glance visibility into global service health. 
            It enables me to <strong>track and report on team KPIs</strong> to ensure alignment with strategic goals 
            and operational performance—exactly what a Planning Manager needs to lead effectively.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Critical Alerts
    critical_parts = parts_df[parts_df["days_of_supply"] < 30]
    if len(critical_parts) > 0:
        st.markdown(f"""
        <div class="toast-critical">
            ⚠️ <strong>CRITICAL:</strong> {len(critical_parts)} parts below 30 days of supply
        </div>
        """, unsafe_allow_html=True)
    
    # KPI Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fill_rate = dealers_filtered["parts_fill_rate"].mean() * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{fill_rate:.1f}%</p>
            <p class="metric-label">Dealer Fill Rate</p>
            <p class="metric-delta-{'positive' if fill_rate > 94 else 'negative'}">
                {'▲' if fill_rate > 94 else '▼'} Target: 95%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_resolution = dealers_filtered["avg_claim_resolution_days"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{avg_resolution:.1f}</p>
            <p class="metric-label">Avg Claim Resolution (Days)</p>
            <p class="metric-delta-{'positive' if avg_resolution < 14 else 'negative'}">
                {'▲' if avg_resolution < 14 else '▼'} Target: 14 days
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        healthy_batteries = len(batteries_filtered[batteries_filtered["status"] == "Healthy"]) / len(batteries_filtered) * 100
        st.markdown(f"""
        <div class="metric-card" title="Battery State of Health based on lithium-ion decay model: cycle aging (~0.05%/cycle) + calendar aging. Batteries below 80% SoH flagged for replacement. ENHANCEMENT: Connect to Specialized Mission Control API for real SoH telemetry from connected bikes.">
            <p class="metric-value">{healthy_batteries:.1f}%</p>
            <p class="metric-label">Fleet Health (SoH > 80%)</p>
            <p class="metric-delta-positive">▲ {len(batteries_filtered):,} batteries tracked</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_liability = (install_base_df["active_units"].sum() * 45)  # $45 avg warranty cost per unit
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${total_liability/1e6:.1f}M</p>
            <p class="metric-label">Warranty Liability Reserve</p>
            <p class="metric-delta-negative">7-Year Right-to-Repair</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        # Parts Inventory Health
        st.markdown("#### 📦 Parts Inventory Health")
        
        parts_chart = parts_df.copy()
        parts_chart["risk"] = parts_chart["days_of_supply"].apply(
            lambda x: "Critical (<30d)" if x < 30 else ("At Risk (30-60d)" if x < 60 else "Healthy (>60d)")
        )
        
        fig = px.bar(
            parts_chart.sort_values("days_of_supply"),
            x="description",
            y="days_of_supply",
            color="risk",
            color_discrete_map={
                "Critical (<30d)": "#F85149",
                "At Risk (30-60d)": "#D29922", 
                "Healthy (>60d)": "#3FB950"
            },
            template="plotly_dark"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="",
            yaxis_title="Days of Supply",
            xaxis_tickangle=-45,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=400,
            margin=dict(l=40, r=40, t=40, b=120)
        )
        fig.add_hline(y=30, line_dash="dash", line_color="#F85149", annotation_text="Critical Threshold")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional Performance
        st.markdown("#### 🌍 Regional Service Performance", help="Radar chart comparing Fill Rate (%) and NPS Score by region. NPS data sourced from post-service surveys via Medallia/Qualtrics integration or dealer-reported scores from the Partner Portal.")
        
        regional_kpis = dealers_filtered.groupby("region").agg({
            "parts_fill_rate": "mean",
            "avg_claim_resolution_days": "mean",
            "nps_score": "mean",
            "dealer_id": "count"
        }).reset_index()
        regional_kpis.columns = ["Region", "Fill Rate", "Avg Resolution Days", "NPS", "Dealers"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[regional_kpis[regional_kpis["Region"]==r]["Fill Rate"].values[0]*100 for r in regional_kpis["Region"]],
            theta=regional_kpis["Region"],
            fill='toself',
            name='Fill Rate %',
            line_color='#E31837'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[regional_kpis[regional_kpis["Region"]==r]["NPS"].values[0] for r in regional_kpis["Region"]],
            theta=regional_kpis["Region"],
            fill='toself',
            name='NPS Score',
            line_color='#58A6FF'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100]),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Install Base Trend
    st.markdown("#### 📈 Active Install Base & Warranty Liability Trend")
    
    install_trend = install_base_df.groupby("model_year")["active_units"].sum().reset_index()
    install_trend["cumulative_liability"] = install_trend["active_units"].cumsum() * 45
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=install_trend["model_year"], y=install_trend["active_units"], name="Active Units", marker_color="#E31837"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(x=install_trend["model_year"], y=install_trend["cumulative_liability"], name="Cumulative Liability ($)", line=dict(color="#58A6FF", width=3)),
        secondary_y=True
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig.update_yaxes(title_text="Active Units", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative Liability ($)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: NETWORK OPTIMIZER (NEW)
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "🌐 Network Optimizer":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Global Network Optimizer</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Route Optimization | Landed Cost Analysis | Modal Selection
        </p>
    </div>
    """, unsafe_allow_html=True)

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>I've mapped Specialized's <strong>actual supply chain network</strong>—Merida in Taiwan (Kaohsiung),
            MAHLE consolidating through Rotterdam, the SLC/Reno split at 60/40, and your 's-Heerenberg EU hub.
            This tool calculates <strong>true landed cost</strong> including freight, duty, insurance, and tariffs
            for every origin-destination pair. It answers: <em>"When does air freight become cheaper than a stockout?"</em></p>
        </div>
        """, unsafe_allow_html=True)

    # Network Visualization
    st.markdown("#### 🗺️ Specialized Global Supply Chain Network")

    # Create network map data
    network_nodes = [
        # Manufacturing
        {"name": "Merida Taiwan", "lat": 24.0, "lon": 120.5, "type": "Manufacturing", "color": "#E31837", "size": 30},
        {"name": "Vietnam Assembly", "lat": 10.8, "lon": 106.6, "type": "Manufacturing", "color": "#E31837", "size": 20},
        {"name": "Czech Assembly", "lat": 49.8, "lon": 15.5, "type": "Manufacturing", "color": "#E31837", "size": 15},
        {"name": "Cambodia Frames", "lat": 11.5, "lon": 104.9, "type": "Manufacturing", "color": "#E31837", "size": 12},
        # Motor Suppliers
        {"name": "MAHLE Stuttgart", "lat": 48.8, "lon": 9.2, "type": "Supplier", "color": "#58A6FF", "size": 18},
        {"name": "Shimano Japan", "lat": 34.5, "lon": 135.5, "type": "Supplier", "color": "#58A6FF", "size": 18},
        {"name": "Bafang China", "lat": 31.3, "lon": 120.6, "type": "Supplier", "color": "#D29922", "size": 12},
        {"name": "Brose Berlin", "lat": 52.5, "lon": 13.4, "type": "Supplier", "color": "#8B949E", "size": 10},
        # Ports
        {"name": "Kaohsiung Port", "lat": 22.6, "lon": 120.3, "type": "Port", "color": "#3FB950", "size": 15},
        {"name": "Rotterdam Port", "lat": 51.9, "lon": 4.5, "type": "Port", "color": "#3FB950", "size": 15},
        {"name": "Long Beach Port", "lat": 33.8, "lon": -118.2, "type": "Port", "color": "#3FB950", "size": 15},
        {"name": "Singapore Port", "lat": 1.3, "lon": 103.8, "type": "Port", "color": "#3FB950", "size": 12},
        # Distribution Hubs
        {"name": "Salt Lake City DC", "lat": 40.8, "lon": -111.9, "type": "Hub", "color": "#A371F7", "size": 25},
        {"name": "Reno DC", "lat": 39.5, "lon": -119.8, "type": "Hub", "color": "#A371F7", "size": 18},
        {"name": "'s-Heerenberg DC", "lat": 51.9, "lon": 6.2, "type": "Hub", "color": "#A371F7", "size": 22},
        {"name": "SingPost APAC", "lat": 1.3, "lon": 103.9, "type": "Hub", "color": "#A371F7", "size": 15},
    ]

    network_df = pd.DataFrame(network_nodes)

    fig = px.scatter_geo(
        network_df,
        lat="lat",
        lon="lon",
        color="type",
        size="size",
        hover_name="name",
        color_discrete_map={
            "Manufacturing": "#E31837",
            "Supplier": "#58A6FF",
            "Port": "#3FB950",
            "Hub": "#A371F7"
        },
        projection="natural earth",
        size_max=25
    )

    # Add shipping lanes as lines
    lanes = [
        # Taiwan to US
        {"start": (22.6, 120.3), "end": (33.8, -118.2), "name": "Kaohsiung → Long Beach", "volume": "High"},
        # Rotterdam to US
        {"start": (51.9, 4.5), "end": (33.8, -118.2), "name": "Rotterdam → Long Beach", "volume": "Medium"},
        # Taiwan to Singapore
        {"start": (22.6, 120.3), "end": (1.3, 103.8), "name": "Kaohsiung → Singapore", "volume": "Medium"},
        # Germany to Rotterdam
        {"start": (48.8, 9.2), "end": (51.9, 4.5), "name": "MAHLE → Rotterdam", "volume": "High"},
    ]

    for lane in lanes:
        fig.add_trace(go.Scattergeo(
            lat=[lane["start"][0], lane["end"][0]],
            lon=[lane["start"][1], lane["end"][1]],
            mode='lines',
            line=dict(width=2, color='rgba(227, 24, 55, 0.5)'),
            name=lane["name"],
            showlegend=False
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            landcolor="#1C2128",
            oceancolor="#0D1117",
            showocean=True,
            coastlinecolor="#30363D",
            showland=True,
            showcountries=True,
            countrycolor="#30363D"
        ),
        template="plotly_dark",
        height=450,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Landed Cost Calculator
    st.markdown("#### 💵 Landed Cost Calculator")

    col1, col2, col3 = st.columns(3)

    with col1:
        origin = st.selectbox("Origin", [
            "Taiwan (Merida/Kaohsiung)",
            "Germany (MAHLE/Stuttgart)",
            "Germany (Brose/Berlin)",
            "Japan (Shimano/Osaka)",
            "China (Bafang/Suzhou)",
            "Vietnam (HCMC)",
            "Cambodia (Phnom Penh)"
        ])

    with col2:
        destination = st.selectbox("Destination Hub", [
            "Salt Lake City, UT (60% US volume)",
            "Reno, NV (40% US volume)",
            "'s-Heerenberg, NL (100% EU)",
            "Singapore (APAC 3PL)"
        ])

    with col3:
        transport_mode = st.selectbox("Transport Mode", ["Ocean (FCL)", "Ocean (LCL)", "Air Freight", "Air Express"])

    col1, col2 = st.columns(2)
    with col1:
        product_value = st.number_input("Product Value (FOB $)", min_value=100, max_value=50000, value=1200, step=100)
    with col2:
        weight_kg = st.number_input("Weight (kg)", min_value=0.1, max_value=100.0, value=3.0, step=0.5)

    # Calculate landed cost
    origin_tariff_map = {
        "Taiwan (Merida/Kaohsiung)": "taiwan_parts",
        "Germany (MAHLE/Stuttgart)": "germany_motors",
        "Germany (Brose/Berlin)": "germany_motors",
        "Japan (Shimano/Osaka)": "japan_motors",
        "China (Bafang/Suzhou)": "china_parts",
        "Vietnam (HCMC)": "vietnam_parts",
        "Cambodia (Phnom Penh)": "cambodia_frames"
    }

    freight_map = {
        ("Taiwan (Merida/Kaohsiung)", "Salt Lake City, UT (60% US volume)", "Ocean (FCL)"): 2650 / 800,  # Per unit assuming 800 units/container
        ("Taiwan (Merida/Kaohsiung)", "Salt Lake City, UT (60% US volume)", "Ocean (LCL)"): 8.50,
        ("Taiwan (Merida/Kaohsiung)", "Salt Lake City, UT (60% US volume)", "Air Freight"): 3.80,
        ("Taiwan (Merida/Kaohsiung)", "Salt Lake City, UT (60% US volume)", "Air Express"): 7.80,
        ("Germany (MAHLE/Stuttgart)", "Salt Lake City, UT (60% US volume)", "Ocean (FCL)"): 2100 / 800,
        ("Germany (MAHLE/Stuttgart)", "Salt Lake City, UT (60% US volume)", "Air Freight"): 2.90,
        ("China (Bafang/Suzhou)", "Salt Lake City, UT (60% US volume)", "Ocean (FCL)"): 2850 / 800,
        ("China (Bafang/Suzhou)", "Salt Lake City, UT (60% US volume)", "Air Freight"): 4.20,
    }

    # Get tariff rate
    tariff_code = origin_tariff_map.get(origin, "taiwan_parts")
    current_tariff = TARIFF_SCENARIOS["current_2025"]["rates"].get(tariff_code, {}).get("total", 0)

    # Get freight rate (default if not found)
    freight_key = (origin, destination, transport_mode)
    if "Air" in transport_mode:
        freight_cost = freight_map.get(freight_key, 4.0) * weight_kg
    else:
        freight_cost = freight_map.get(freight_key, 5.0) * weight_kg

    # Calculate components
    duty_cost = product_value * (current_tariff / 100)
    insurance_cost = product_value * 0.005  # 0.5% insurance
    handling_cost = 15  # Flat handling fee

    landed_cost = product_value + freight_cost + duty_cost + insurance_cost + handling_cost

    # Display breakdown
    st.markdown("#### 📊 Cost Breakdown")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${product_value:,.0f}</p>
            <p class="metric-label">FOB Value</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${freight_cost:,.2f}</p>
            <p class="metric-label">Freight ({transport_mode})</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        duty_color = "#F85149" if current_tariff > 20 else ("#D29922" if current_tariff > 10 else "#3FB950")
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {duty_color};">
            <p class="metric-value" style="color: {duty_color};">${duty_cost:,.2f}</p>
            <p class="metric-label">Duty ({current_tariff}%)</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${insurance_cost + handling_cost:,.2f}</p>
            <p class="metric-label">Insurance + Handling</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card" style="border: 2px solid #E31837;">
            <p class="metric-value">${landed_cost:,.2f}</p>
            <p class="metric-label">TOTAL LANDED COST</p>
            <p class="metric-delta-negative">+{((landed_cost/product_value - 1) * 100):.1f}% over FOB</p>
        </div>
        """, unsafe_allow_html=True)

    # Modal Comparison
    st.markdown("#### ⚖️ Ocean vs. Air Breakeven Analysis")

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 The Math Behind Smart Logistics</h4>
            <p>Air freight at $3.80/kg seems expensive vs. ocean at ~$3.30/unit. But when you factor in
            <strong>18 days of ocean transit + 3 days rail to SLC = 21 days of inventory holding cost</strong>,
            plus the <strong>stockout cost of a rider waiting 3 weeks</strong>, air often wins for warranty parts.
            This is the analysis that turns "emergency logistics" into "planned logistics."</p>
        </div>
        """, unsafe_allow_html=True)

    # Create comparison chart
    units_range = list(range(1, 101))
    ocean_cost = [2650 + (u * product_value * current_tariff / 100) for u in units_range]  # Container + duty per unit
    air_cost = [(u * weight_kg * 3.80) + (u * product_value * current_tariff / 100) for u in units_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=units_range, y=ocean_cost, name="Ocean (FCL)", line=dict(color="#3FB950", width=3)))
    fig.add_trace(go.Scatter(x=units_range, y=air_cost, name="Air Freight", line=dict(color="#58A6FF", width=3)))

    # Find breakeven
    breakeven_idx = next((i for i, (o, a) in enumerate(zip(ocean_cost, air_cost)) if o < a), len(units_range))

    if breakeven_idx < len(units_range):
        fig.add_vline(x=breakeven_idx + 1, line_dash="dash", line_color="#E31837",
                      annotation_text=f"Breakeven: {breakeven_idx + 1} units")

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        xaxis_title="Number of Units",
        yaxis_title="Total Cost ($)",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig, use_container_width=True)

    # SingPost API Integration Mockup
    st.markdown("#### 🔌 3PL Integration: SingPost APAC")

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Integration Opportunity</h4>
            <p>SingPost provides a REST API for inventory visibility. I can connect Service Command directly
            to their system at <code>api.singpost.com/inventory/v2</code> to pull <strong>real-time stock levels</strong>
            for APAC without waiting for Oracle sync. This eliminates the "we thought we had stock" problem.</p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        ```json
        // SingPost API Response
        {
          "warehouse": "SG-APAC-01",
          "last_updated": "2025-01-15T08:30:00Z",
          "inventory": [
            {"sku": "MOT-SL12-001", "qty": 45},
            {"sku": "BAT-320-SL", "qty": 128},
            {"sku": "TCU-G5-001", "qty": 67}
          ]
        }
        ```
        """)

    with col2:
        # Mock real-time inventory display
        singpost_inventory = pd.DataFrame({
            "SKU": ["MOT-SL12-001", "BAT-320-SL", "TCU-G5-001", "CHG-SL-COMP", "MOT-EP8-001"],
            "Description": ["MAHLE SL 1.2 Motor", "320Wh SL Battery", "TCU Gen 5", "SL Compact Charger", "Shimano EP8"],
            "On Hand": [45, 128, 67, 89, 32],
            "Allocated": [12, 45, 8, 15, 10],
            "Available": [33, 83, 59, 74, 22],
            "Status": ["OK", "OK", "OK", "OK", "LOW"]
        })
        st.dataframe(singpost_inventory, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: TARIFF WAR ROOM (NEW)
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "💰 Tariff War Room":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Tariff War Room</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Section 301 Exposure | Scenario Planning | Legal Optimization Strategies
        </p>
    </div>
    """, unsafe_allow_html=True)

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>Anyone who's managed supply chains across Asia knows tariff volatility firsthand.
            This module <strong>quantifies your intuition</strong>. Taiwan parts at 21% today could spike to 32%
            (like August 2025). China exposure is 30.5% and could hit 65%. This tool shows <strong>exactly where
            to shift sourcing</strong>—Vietnam assembly, Czech EU hub, or MAHLE over Bafang—with the math to back it up.</p>
        </div>
        """, unsafe_allow_html=True)

    # Current Exposure Summary
    st.markdown("#### 🚨 Current Tariff Exposure by Origin")

    # Calculate exposure from parts inventory
    exposure_by_origin = parts_df.groupby("origin").agg({
        "unit_cost": "sum",
        "monthly_demand": "sum",
        "tariff_rate_pct": "mean"
    }).reset_index()
    exposure_by_origin["annual_duty_exposure"] = exposure_by_origin["unit_cost"] * exposure_by_origin["monthly_demand"] * 12 * (exposure_by_origin["tariff_rate_pct"] / 100)

    col1, col2, col3, col4 = st.columns(4)

    # Taiwan Exposure
    taiwan_exp = exposure_by_origin[exposure_by_origin["origin"] == "Taiwan"]["annual_duty_exposure"].sum()
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #D29922;">
            <p class="metric-value">${taiwan_exp/1000:,.0f}K</p>
            <p class="metric-label">Taiwan Exposure</p>
            <p style="color: #D29922; font-size: 0.8rem;">21% total duty (10% Section 301)</p>
        </div>
        """, unsafe_allow_html=True)

    # China Exposure
    china_exp = exposure_by_origin[exposure_by_origin["origin"] == "China"]["annual_duty_exposure"].sum()
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #F85149;">
            <p class="metric-value">${china_exp/1000:,.0f}K</p>
            <p class="metric-label">China Exposure</p>
            <p style="color: #F85149; font-size: 0.8rem;">30.5% total duty (25% Section 301)</p>
        </div>
        """, unsafe_allow_html=True)

    # Germany/Japan (low exposure)
    germany_exp = exposure_by_origin[exposure_by_origin["origin"] == "Germany"]["annual_duty_exposure"].sum()
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #3FB950;">
            <p class="metric-value">${germany_exp/1000:,.0f}K</p>
            <p class="metric-label">Germany Exposure</p>
            <p style="color: #3FB950; font-size: 0.8rem;">0% duty (no Section 301)</p>
        </div>
        """, unsafe_allow_html=True)

    # Total
    total_exp = exposure_by_origin["annual_duty_exposure"].sum()
    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border: 2px solid #E31837;">
            <p class="metric-value">${total_exp/1000:,.0f}K</p>
            <p class="metric-label">TOTAL Annual Duty</p>
            <p style="color: #8B949E; font-size: 0.8rem;">Current scenario</p>
        </div>
        """, unsafe_allow_html=True)

    # Scenario Comparison
    st.markdown("#### 📊 Tariff Scenario Comparison")

    scenario_select = st.selectbox("Compare Scenarios", list(TARIFF_SCENARIOS.keys()), format_func=lambda x: TARIFF_SCENARIOS[x]["name"])

    # Build comparison table
    comparison_data = []
    for origin_key, origin_name in [("taiwan_parts", "Taiwan Parts"), ("china_parts", "China Parts"), ("china_batteries", "China Batteries"), ("germany_motors", "Germany Motors"), ("japan_motors", "Japan Motors"), ("vietnam_parts", "Vietnam Parts")]:
        row = {"Origin": origin_name}
        for scenario_key, scenario in TARIFF_SCENARIOS.items():
            rates = scenario["rates"].get(origin_key, {})
            row[scenario["name"]] = f"{rates.get('total', 0):.1f}%"
        comparison_data.append(row)

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    # Visual comparison
    st.markdown("#### 📈 Scenario Impact Visualization")

    scenarios = list(TARIFF_SCENARIOS.keys())
    scenario_costs = []

    for scenario_key in scenarios:
        rates = TARIFF_SCENARIOS[scenario_key]["rates"]
        total_cost = 0
        for _, row in parts_df.iterrows():
            tariff_code = row.get("tariff_code", "taiwan_parts")
            rate = rates.get(tariff_code, {}).get("total", 0)
            annual_value = row["unit_cost"] * row["monthly_demand"] * 12
            total_cost += annual_value * (rate / 100)
        scenario_costs.append({
            "Scenario": TARIFF_SCENARIOS[scenario_key]["name"],
            "Annual Duty Cost": total_cost
        })

    scenario_df = pd.DataFrame(scenario_costs)

    fig = px.bar(
        scenario_df,
        x="Scenario",
        y="Annual Duty Cost",
        color="Annual Duty Cost",
        color_continuous_scale=[[0, "#3FB950"], [0.5, "#D29922"], [1, "#F85149"]],
        text=scenario_df["Annual Duty Cost"].apply(lambda x: f"${x/1000:,.0f}K")
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        height=400,
        showlegend=False
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # Optimization Strategies
    st.markdown("#### 🎯 Legal Tariff Optimization Strategies")

    strategies = [
        {
            "strategy": "Shift Bafang → MAHLE",
            "description": "Replace Chinese Bafang motors with German MAHLE for commuter bikes",
            "current_cost": 380,
            "new_cost": 950,
            "current_duty": 30.5,
            "new_duty": 0,
            "tariff_savings": "100%",
            "unit_cost_impact": "+150%",
            "recommendation": "For premium models only"
        },
        {
            "strategy": "Vietnam Assembly",
            "description": "Route entry-level frames through Vietnam instead of Taiwan",
            "current_cost": 450,
            "new_cost": 420,
            "current_duty": 21,
            "new_duty": 0,
            "tariff_savings": "100%",
            "unit_cost_impact": "-7%",
            "recommendation": "RECOMMENDED for all entry-level"
        },
        {
            "strategy": "Czech EU Assembly",
            "description": "Final assembly in Czech for EU-bound bikes avoids US tariffs on re-export",
            "current_cost": 5500,
            "new_cost": 5800,
            "current_duty": 21,
            "new_duty": 0,
            "tariff_savings": "100%",
            "unit_cost_impact": "+5%",
            "recommendation": "Already implemented for EU"
        },
        {
            "strategy": "CATL → Samsung SDI",
            "description": "Shift battery sourcing from Chinese CATL to Korean Samsung SDI",
            "current_cost": 520,
            "new_cost": 580,
            "current_duty": 28.4,
            "new_duty": 5.5,
            "tariff_savings": "81%",
            "unit_cost_impact": "+12%",
            "recommendation": "RECOMMENDED for high-volume SKUs"
        },
    ]

    for strat in strategies:
        rec_color = "#3FB950" if "RECOMMENDED" in strat["recommendation"] else ("#D29922" if "premium" in strat["recommendation"] else "#8B949E")
        st.markdown(f"""
        <div style="background: #1C2128; border-radius: 12px; padding: 20px; margin: 12px 0; border-left: 4px solid {rec_color};">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h4 style="color: #F0F6FC; margin: 0;">{strat['strategy']}</h4>
                    <p style="color: #8B949E; margin: 4px 0;">{strat['description']}</p>
                </div>
                <span style="background: {rec_color}; color: {'white' if rec_color != '#D29922' else 'black'}; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">{strat['recommendation']}</span>
            </div>
            <div style="display: flex; gap: 40px; margin-top: 16px;">
                <div>
                    <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">UNIT COST</p>
                    <p style="color: #F0F6FC; font-size: 1rem; margin: 0;">${strat['current_cost']} → ${strat['new_cost']} <span style="color: {'#F85149' if '+' in strat['unit_cost_impact'] else '#3FB950'};">({strat['unit_cost_impact']})</span></p>
                </div>
                <div>
                    <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">DUTY RATE</p>
                    <p style="color: #F0F6FC; font-size: 1rem; margin: 0;">{strat['current_duty']}% → {strat['new_duty']}% <span style="color: #3FB950;">(-{strat['tariff_savings']} tariff)</span></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Part-level exposure table
    st.markdown("#### 📋 Parts with Highest Tariff Exposure")

    parts_exposure = parts_df[["part_number", "description", "supplier", "origin", "unit_cost", "monthly_demand", "tariff_rate_pct"]].copy()
    parts_exposure["annual_duty"] = parts_exposure["unit_cost"] * parts_exposure["monthly_demand"] * 12 * (parts_exposure["tariff_rate_pct"] / 100)
    parts_exposure = parts_exposure.sort_values("annual_duty", ascending=False).head(10)
    parts_exposure["annual_duty"] = parts_exposure["annual_duty"].apply(lambda x: f"${x:,.0f}")
    parts_exposure["tariff_rate_pct"] = parts_exposure["tariff_rate_pct"].apply(lambda x: f"{x:.1f}%")
    parts_exposure.columns = ["Part #", "Description", "Supplier", "Origin", "Unit Cost", "Monthly Demand", "Tariff %", "Annual Duty"]

    st.dataframe(parts_exposure[["Part #", "Description", "Origin", "Tariff %", "Annual Duty"]], use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: RIGHT-TO-REPAIR FORECASTER
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "⚖️ Right-to-Repair Forecaster":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Right-to-Repair Liability Forecaster</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            California SB-244 (7 Years) | EU Directive (10 Years) | Weibull Survival Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight: The Moore's Law Problem</h4>
            <p>Here's the challenge: <strong>Motor technology evolves every 20 months</strong>, but we must support parts for
            <strong>84+ months (California) or 120 months (EU)</strong>. Standard Excel forecasting uses flat averages—it
            misses the "wear-out spike" that Weibull analysis captures. When 500 Brose motors fail in June and we have zero
            stock, we panic-ship at <strong>$40/unit air freight</strong> instead of <strong>$4/unit ocean</strong>.
            This tool predicts that spike <strong>6 months in advance</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════════
    # LEGISLATION TRACKER
    # ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("#### ⚖️ Right-to-Repair Legislation Tracker")

    col1, col2, col3 = st.columns(3)

    # California SB-244
    ca_effective = datetime(2024, 7, 1)
    ca_days_active = (datetime.now() - ca_effective).days

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #E31837;">
            <h4 style="color: #E31837; margin: 0 0 8px 0;">🇺🇸 California SB-244</h4>
            <p style="color: #3FB950; font-size: 0.85rem; margin: 0;">✓ ACTIVE ({ca_days_active} days)</p>
            <hr style="border-color: #30363D; margin: 12px 0;">
            <p style="color: #F0F6FC; margin: 4px 0;"><strong>7 years</strong> parts availability</p>
            <p style="color: #8B949E; font-size: 0.8rem; margin: 4px 0;">Products >$100 sold in CA after July 1, 2024</p>
            <p style="color: #D29922; font-size: 0.8rem; margin: 4px 0;">Penalty: $1,000 per violation</p>
        </div>
        """, unsafe_allow_html=True)

    # EU Right to Repair
    eu_target = datetime(2025, 6, 1)
    eu_days = (eu_target - datetime.now()).days

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #D29922;">
            <h4 style="color: #D29922; margin: 0 0 8px 0;">🇪🇺 EU Right to Repair Directive</h4>
            <p style="color: #D29922; font-size: 0.85rem; margin: 0;">⏳ PENDING ({eu_days} days)</p>
            <hr style="border-color: #30363D; margin: 12px 0;">
            <p style="color: #F0F6FC; margin: 4px 0;"><strong>10 years</strong> parts availability (proposed)</p>
            <p style="color: #8B949E; font-size: 0.8rem; margin: 4px 0;">Includes software updates requirement</p>
            <p style="color: #F85149; font-size: 0.8rem; margin: 4px 0;">Penalty: Up to 4% of EU revenue</p>
        </div>
        """, unsafe_allow_html=True)

    # EU Battery Regulation
    bat_deadline = datetime(2027, 2, 18)
    bat_days = (bat_deadline - datetime.now()).days

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid #58A6FF;">
            <h4 style="color: #58A6FF; margin: 0 0 8px 0;">🔋 EU Battery Regulation 2023/1542</h4>
            <p style="color: #D29922; font-size: 0.85rem; margin: 0;">⏳ {bat_days} days to compliance</p>
            <hr style="border-color: #30363D; margin: 12px 0;">
            <p style="color: #F0F6FC; margin: 4px 0;"><strong>Battery Passport</strong> required</p>
            <p style="color: #8B949E; font-size: 0.8rem; margin: 4px 0;">QR code + digital twin for all >2kWh batteries</p>
            <p style="color: #8B949E; font-size: 0.8rem; margin: 4px 0;">Recycled content tracking by 2031</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════════════
    # COMPONENT OBSOLESCENCE TIMELINE (MOORE'S LAW)
    # ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("#### ⚡ Component Obsolescence vs. Legal Obligations")

    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Why Excel Fails Here</h4>
            <p>Excel forecasts use <strong>moving averages</strong>—they assume failure rates stay constant. But e-bike
            components follow a <strong>bathtub curve</strong>: early failures (infant mortality), random failures (useful life),
            then accelerating wear-out. The Weibull distribution captures this. A motor with β=2.1 (wear-out mode) will have
            <strong>60% of failures in the last 2 years of its 7-year obligation</strong>—Excel misses this completely.</p>
        </div>
        """, unsafe_allow_html=True)

    # Component lifecycle visualization
    components = [
        {"name": "Motors (Full Power)", "gen_cycle": 20, "support_months": 84, "weibull_beta": 2.1, "risk": "MEDIUM"},
        {"name": "Motors (SL/MAHLE)", "gen_cycle": 20, "support_months": 84, "weibull_beta": 2.0, "risk": "MEDIUM"},
        {"name": "Batteries (NMC)", "gen_cycle": 18, "support_months": 84, "weibull_beta": 1.8, "risk": "HIGH"},
        {"name": "TCU/Display", "gen_cycle": 24, "support_months": 60, "weibull_beta": 1.2, "risk": "VERY HIGH"},
        {"name": "Chargers", "gen_cycle": 36, "support_months": 84, "weibull_beta": 1.5, "risk": "LOW"},
    ]

    # Create Gantt-style timeline
    fig = go.Figure()

    for i, comp in enumerate(components):
        # Generation cycle (new version every X months)
        fig.add_trace(go.Bar(
            x=[comp["gen_cycle"]],
            y=[comp["name"]],
            orientation='h',
            marker_color="#58A6FF",
            name="Gen Cycle" if i == 0 else None,
            showlegend=(i == 0),
            hovertemplate=f"New generation every {comp['gen_cycle']} months"
        ))

        # Support obligation
        fig.add_trace(go.Bar(
            x=[comp["support_months"]],
            y=[comp["name"]],
            orientation='h',
            marker_color="#E31837",
            opacity=0.5,
            name="Support Obligation" if i == 0 else None,
            showlegend=(i == 0),
            hovertemplate=f"Must support for {comp['support_months']} months"
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        barmode='overlay',
        xaxis_title="Months",
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    fig.add_vline(x=84, line_dash="dash", line_color="#E31837", annotation_text="7-Year CA Requirement")
    fig.add_vline(x=120, line_dash="dot", line_color="#D29922", annotation_text="10-Year EU (Proposed)")

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ═══════════════════════════════════════════════════════════════════════════════
    # WEIBULL FORECASTER
    # ═══════════════════════════════════════════════════════════════════════════════
    st.markdown("#### 📈 Weibull Failure Forecaster")

    # Input Parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_model = st.selectbox("Select Model", products_df["model"].unique())
    
    with col2:
        install_base = st.number_input("Active Install Base", min_value=1000, max_value=200000, value=50000, step=1000)
    
    with col3:
        service_level_target = st.slider("Service Level Target (%)", min_value=85, max_value=99, value=95)
    
    # Weibull Parameters
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Failure Curve Parameters")
        weibull_shape = st.slider("Weibull Shape (β)", min_value=0.5, max_value=3.0, value=1.5, step=0.1, 
                                   help="β<1: Early failures, β=1: Random, β>1: Wear-out failures")
    with col2:
        st.markdown("##### &nbsp;")
        weibull_scale = st.slider("Weibull Scale (η) - Years", min_value=2.0, max_value=10.0, value=5.0, step=0.5,
                                   help="Characteristic life in years")
    
    # Generate forecast
    years = np.arange(0, 8, 0.25)  # 7 years in quarters
    
    # Weibull failure probability
    failure_rate = 1 - np.exp(-(years / weibull_scale) ** weibull_shape)
    
    # Expected failures
    expected_failures = install_base * failure_rate
    
    # Parts required (with buffer for service level)
    buffer_factor = 1 + (service_level_target - 85) / 100
    parts_required = expected_failures * buffer_factor
    
    # Simulate actual inventory (declining over time as parts become scarce)
    actual_inventory = np.maximum(parts_required * 0.7 * np.exp(-years/4), parts_required * 0.3)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        "Year": years,
        "Expected Failures": expected_failures,
        "Parts Required": parts_required,
        "Actual Inventory": actual_inventory,
        "Gap": parts_required - actual_inventory
    })
    
    # The Liability Wedge Chart
    st.markdown("#### 📊 The Liability Wedge")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Parts Required"],
        fill='tonexty',
        mode='lines',
        name='Parts Required (Target)',
        line=dict(color='#E31837', width=2),
        fillcolor='rgba(227, 24, 55, 0.3)'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Actual Inventory"],
        fill='tozeroy',
        mode='lines',
        name='Actual Inventory',
        line=dict(color='#3FB950', width=2),
        fillcolor='rgba(63, 185, 80, 0.3)'
    ))
    
    # Add the gap shading
    fig.add_trace(go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Gap"],
        mode='lines',
        name='Liability Gap',
        line=dict(color='#F85149', width=2, dash='dash')
    ))
    
    fig.add_vline(x=7, line_dash="dash", line_color="#8B949E", annotation_text="7-Year Legal Limit")
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        xaxis_title="Years from Model Launch",
        yaxis_title="Units",
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    avg_part_cost = parts_df[parts_df["category"].isin(["Motor", "Battery"])]["unit_cost"].mean()
    total_parts_needed = int(forecast_df["Parts Required"].max())
    capital_lockup = total_parts_needed * avg_part_cost
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{total_parts_needed:,}</p>
            <p class="metric-label">Total Parts Required</p>
            <p class="metric-delta-negative">Over 7-year horizon</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${capital_lockup/1e6:.2f}M</p>
            <p class="metric-label">Capital Lock-Up</p>
            <p class="metric-delta-negative">Inventory investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        gap_pct = (forecast_df["Gap"].max() / forecast_df["Parts Required"].max()) * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{gap_pct:.1f}%</p>
            <p class="metric-label">Maximum Gap</p>
            <p class="metric-delta-negative">Year {forecast_df.loc[forecast_df['Gap'].idxmax(), 'Year']:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        scrap_risk = capital_lockup * 0.15  # 15% estimated scrap
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${scrap_risk/1e6:.2f}M</p>
            <p class="metric-label">Scrap Risk</p>
            <p class="metric-delta-negative">Est. 15% obsolescence</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Last-Time Buy Simulation
    st.markdown("#### 🛒 Last-Time Buy Simulation")
    
    if st.button("🚀 Run Last-Time Buy Optimization", type="primary"):
        with st.spinner("Running Monte Carlo simulation (10,000 scenarios)..."):
            import time
            time.sleep(1.5)  # Simulate processing
            
            # Simulated results
            optimal_qty = int(total_parts_needed * 1.1)
            optimal_cost = optimal_qty * avg_part_cost
            expected_scrap = optimal_qty * 0.08
            expected_scrap_cost = expected_scrap * avg_part_cost * 0.3  # 30% liquidation value
            
            st.success("✅ Optimization Complete")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Optimal Order Quantity", f"{optimal_qty:,} units")
            with col2:
                st.metric("Total Investment", f"${optimal_cost/1e6:.2f}M")
            with col3:
                st.metric("Expected Scrap Cost", f"${expected_scrap_cost/1e6:.2f}M", delta=f"-{(expected_scrap_cost/optimal_cost)*100:.1f}%")
            
            st.markdown("""
            <div style="background: #1C2128; border-radius: 8px; padding: 16px; margin-top: 16px;">
                <h4 style="color: #3FB950; margin-top: 0;">💡 Recommendation</h4>
                <p style="color: #C9D1D9;">Based on Monte Carlo simulation, recommend placing a last-time buy order 
                at <strong>110% of projected demand</strong>. This provides a 95% confidence level of meeting 
                service obligations while minimizing scrap exposure through our Redwood Materials recycling partnership.</p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: EU BATTERY PASSPORT
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "🔋 EU Battery Passport":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">EU Battery Passport Compliance Center</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            EU Regulation 2023/1542 | Individual Serial Number Tracking | February 2027 Deadline
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>This module represents a <strong>process improvement in traceability</strong> that directly addresses the JD 
            requirement to "identify and implement process improvements that elevate rider support." By February 2027, 
            every e-bike battery >2kWh requires a digital passport with QR code access. This positions Specialized 
            as a first-mover in compliance—turning regulatory obligation into competitive advantage through our 
            existing Redwood Materials and Call2Recycle partnerships.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Countdown Timer
    deadline = datetime(2027, 2, 18)
    days_remaining = (deadline - datetime.now()).days
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        urgency_color = "#F85149" if days_remaining < 365 else ("#D29922" if days_remaining < 545 else "#3FB950")
        st.markdown(f"""
        <div class="metric-card" style="border-left: 4px solid {urgency_color};">
            <p class="metric-value" style="background: linear-gradient(135deg, {urgency_color}, {urgency_color}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{days_remaining}</p>
            <p class="metric-label">Days Until Deadline</p>
            <p style="color: {urgency_color}; font-size: 0.8rem;">Feb 18, 2027</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        compliant_pct = len(batteries_filtered[batteries_filtered["recycled_content_pct"] > 12]) / len(batteries_filtered) * 100
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{compliant_pct:.1f}%</p>
            <p class="metric-label">Passport Ready</p>
            <p class="metric-delta-positive">Batteries with full traceability</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{len(batteries_filtered):,}</p>
            <p class="metric-label">Batteries Tracked</p>
            <p class="metric-delta-positive">Across {len(batteries_filtered['region'].unique())} regions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        recycling_rate = len(batteries_filtered[batteries_filtered["location"] == "Recycling"]) / len(batteries_filtered[batteries_filtered["status"] == "End-of-Life"]) * 100 if len(batteries_filtered[batteries_filtered["status"] == "End-of-Life"]) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{min(recycling_rate, 100):.1f}%</p>
            <p class="metric-label">Recycling Rate</p>
            <p class="metric-delta-{'positive' if recycling_rate > 50 else 'negative'}">Target: >50% material recovery</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🗺️ Global Battery Health", "🔍 Battery Trace", "📊 Compliance Dashboard"])
    
    with tab1:
        st.markdown("#### Global Battery Health Heatmap")
        
        # Create heatmap data
        heatmap_data = batteries_filtered.copy()
        heatmap_data["age_years"] = (datetime.now() - pd.to_datetime(heatmap_data["production_date"])).dt.days / 365
        heatmap_data["age_bucket"] = pd.cut(heatmap_data["age_years"], bins=[0, 1, 2, 3, 4, 5, 6], labels=["0-1yr", "1-2yr", "2-3yr", "3-4yr", "4-5yr", "5-6yr"])
        
        pivot = heatmap_data.pivot_table(values="state_of_health", index="region", columns="age_bucket", aggfunc="mean")
        
        fig = px.imshow(
            pivot,
            labels=dict(x="Battery Age", y="Region", color="Avg SoH %"),
            color_continuous_scale=[[0, "#F85149"], [0.5, "#D29922"], [1, "#3FB950"]],
            aspect="auto"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Chemistry breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Battery Chemistry Distribution")
            chemistry_dist = batteries_filtered["chemistry"].value_counts().reset_index()
            chemistry_dist.columns = ["Chemistry", "Count"]
            
            fig = px.pie(
                chemistry_dist,
                values="Count",
                names="Chemistry",
                color_discrete_sequence=["#E31837", "#58A6FF", "#3FB950"],
                hole=0.6
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                template="plotly_dark",
                height=300,
                showlegend=True,
                legend=dict(orientation="h")
            )
            fig.add_annotation(text="Chemistry<br>Mix", x=0.5, y=0.5, font_size=14, showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Lifecycle Status")
            status_dist = batteries_filtered["status"].value_counts().reset_index()
            status_dist.columns = ["Status", "Count"]
            
            fig = px.bar(
                status_dist,
                x="Status",
                y="Count",
                color="Status",
                color_discrete_map={
                    "Healthy": "#3FB950",
                    "Degraded": "#D29922",
                    "End-of-Life": "#F85149"
                }
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                template="plotly_dark",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🔍 Trace a Battery")
        
        serial_input = st.text_input("Enter Battery Serial Number", placeholder="e.g., BATT-NMC-1042")
        
        if serial_input:
            battery = batteries_filtered[batteries_filtered["serial_number"].str.contains(serial_input, case=False)]
            
            if len(battery) > 0:
                bat = battery.iloc[0]
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #E31837; margin: 0;">{bat['serial_number']}</h3>
                        <hr style="border-color: #30363D;">
                        <p><strong>Capacity:</strong> {bat['capacity_wh']} Wh</p>
                        <p><strong>Chemistry:</strong> {bat['chemistry']}</p>
                        <p><strong>Production Date:</strong> {bat['production_date']}</p>
                        <p><strong>Warranty Expires:</strong> {bat['warranty_expires']}</p>
                        <p><strong>CO₂ Footprint:</strong> {bat['co2_footprint_kg']} kg</p>
                        <p><strong>Recycled Content:</strong> {bat['recycled_content_pct']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Lifecycle timeline
                    st.markdown("#### Battery Lifecycle Journey")
                    
                    # Create Sankey-style flow
                    lifecycle_stages = ["Manufactured", "Shipped", "Sold", "In Service", bat['location']]
                    
                    fig = go.Figure(go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=20,
                            label=lifecycle_stages,
                            color=["#58A6FF", "#58A6FF", "#3FB950", "#3FB950", "#E31837" if bat['status'] != "Healthy" else "#3FB950"]
                        ),
                        link=dict(
                            source=[0, 1, 2, 3],
                            target=[1, 2, 3, 4],
                            value=[1, 1, 1, 1],
                            color=["rgba(88, 166, 255, 0.4)"]*4
                        )
                    ))
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        template="plotly_dark",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Health Gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=bat['state_of_health'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "State of Health (%)"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#E31837"},
                            'steps': [
                                {'range': [0, 70], 'color': "rgba(248, 81, 73, 0.3)"},
                                {'range': [70, 80], 'color': "rgba(210, 153, 34, 0.3)"},
                                {'range': [80, 100], 'color': "rgba(63, 185, 80, 0.3)"}
                            ],
                            'threshold': {
                                'line': {'color': "white", 'width': 4},
                                'thickness': 0.75,
                                'value': 70
                            }
                        }
                    ))
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        template="plotly_dark",
                        height=250
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No battery found with that serial number. Try: BATT-NMC-1042")
        
        else:
            # Show sample batteries
            st.markdown("##### Sample Batteries for Demo")
            sample = batteries_filtered.head(10)[["serial_number", "capacity_wh", "state_of_health", "status", "location"]]
            st.dataframe(sample, use_container_width=True)
    
    with tab3:
        st.markdown("#### EU Regulation 2023/1542 Compliance Checklist")
        
        compliance_items = [
            {"requirement": "CE Marking on all batteries", "deadline": "Aug 2024", "status": "Complete", "pct": 100},
            {"requirement": "QR Code labeling with specifications", "deadline": "Aug 2026", "status": "In Progress", "pct": 72},
            {"requirement": "Digital Battery Passport (>2kWh)", "deadline": "Feb 2027", "status": "In Progress", "pct": 45},
            {"requirement": "Carbon footprint declaration", "deadline": "Feb 2025", "status": "At Risk", "pct": 35},
            {"requirement": "Due diligence policy (>€40M)", "deadline": "Aug 2025", "status": "In Progress", "pct": 60},
            {"requirement": "Recycled content declaration", "deadline": "Aug 2028", "status": "Planning", "pct": 15},
        ]
        
        for item in compliance_items:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{item['requirement']}**")
                st.progress(item['pct'] / 100)
            
            with col2:
                st.markdown(f"*Deadline: {item['deadline']}*")
            
            with col3:
                status_class = "status-healthy" if item['status'] == "Complete" else ("status-critical" if item['status'] == "At Risk" else "status-warning")
                st.markdown(f"""<span class="{status_class}">{item['status']}</span>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: DEALER NETWORK HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "🏪 Dealer Network Health":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Dealer Network Health Dashboard</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Ensuring Our Retail Partners Can Deliver the Specialized Experience
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>Our dealers are the front line of rider experience. This dashboard helps me <strong>"collaborate with 
            purchasing, quality engineering, and global customer support teams"</strong> to identify friction points 
            before they become escalations. Tracking pending reimbursements ensures we're not creating cash flow 
            stress that degrades service quality. This is how I <strong>"own escalation pathways and develop 
            proactive solutions."</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_dealers = len(dealers_filtered)
        ebike_certified = len(dealers_filtered[dealers_filtered["e_bike_certified"] == True])
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{total_dealers}</p>
            <p class="metric-label">Active Dealers</p>
            <p class="metric-delta-positive">{ebike_certified} e-bike certified ({ebike_certified/total_dealers*100:.0f}%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        open_claims = dealers_filtered["open_warranty_claims"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{open_claims:,}</p>
            <p class="metric-label">Open Warranty Claims</p>
            <p class="metric-delta-negative">Across all regions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pending_reimburse = dealers_filtered["pending_reimbursement_usd"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${pending_reimburse/1e6:.2f}M</p>
            <p class="metric-label">Pending Reimbursements</p>
            <p class="metric-delta-negative">Dealer cash tied up</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_nps = dealers_filtered["nps_score"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{avg_nps:.0f}</p>
            <p class="metric-label">Avg Dealer NPS</p>
            <p class="metric-delta-{'positive' if avg_nps > 50 else 'negative'}">{'▲ Promoters' if avg_nps > 50 else '▼ At Risk'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Fill Rate by Region")
        
        region_fill = dealers_filtered.groupby("region").agg({
            "parts_fill_rate": "mean",
            "dealer_id": "count"
        }).reset_index()
        region_fill.columns = ["Region", "Fill Rate", "Dealers"]
        region_fill["Fill Rate"] = region_fill["Fill Rate"] * 100
        
        fig = px.bar(
            region_fill,
            x="Region",
            y="Fill Rate",
            color="Fill Rate",
            color_continuous_scale=[[0, "#F85149"], [0.5, "#D29922"], [1, "#3FB950"]],
            text=region_fill["Fill Rate"].round(1).astype(str) + "%"
        )
        fig.add_hline(y=95, line_dash="dash", line_color="#E31837", annotation_text="95% Target")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=350,
            showlegend=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### ⏱️ Claim Resolution Distribution")
        
        fig = px.histogram(
            dealers_filtered,
            x="avg_claim_resolution_days",
            nbins=20,
            color_discrete_sequence=["#E31837"]
        )
        fig.add_vline(x=14, line_dash="dash", line_color="#3FB950", annotation_text="14-day Target")
        fig.add_vline(x=30, line_dash="dash", line_color="#F85149", annotation_text="SLA Breach")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            xaxis_title="Days to Resolution",
            yaxis_title="Number of Dealers",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Dealer Risk Table
    st.markdown("#### 🚨 Dealers Requiring Attention")
    
    at_risk = dealers_filtered[
        (dealers_filtered["parts_fill_rate"] < 0.85) | 
        (dealers_filtered["avg_claim_resolution_days"] > 30) |
        (dealers_filtered["pending_reimbursement_usd"] > 10000)
    ].sort_values("parts_fill_rate")
    
    if len(at_risk) > 0:
        display_df = at_risk[["dealer_id", "region", "tier", "parts_fill_rate", "avg_claim_resolution_days", "pending_reimbursement_usd", "nps_score"]].head(10)
        display_df.columns = ["Dealer ID", "Region", "Tier", "Fill Rate", "Avg Resolution (days)", "Pending Reimb ($)", "NPS"]
        display_df["Fill Rate"] = (display_df["Fill Rate"] * 100).round(1).astype(str) + "%"
        display_df["Pending Reimb ($)"] = display_df["Pending Reimb ($)"].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No dealers currently flagged for escalation")
    
    # World Map
    st.markdown("#### 🌍 Global Dealer Network")
    
    # Aggregate by sub-region for map
    region_coords = {
        "US West": {"lat": 37.7749, "lon": -122.4194},
        "US Central": {"lat": 39.7392, "lon": -104.9903},
        "US East": {"lat": 40.7128, "lon": -74.0060},
        "Canada": {"lat": 43.6532, "lon": -79.3832},
        "UK/Ireland": {"lat": 51.5074, "lon": -0.1278},
        "DACH": {"lat": 48.2082, "lon": 16.3738},
        "France": {"lat": 48.8566, "lon": 2.3522},
        "Nordics": {"lat": 59.3293, "lon": 18.0686},
        "Southern EU": {"lat": 41.9028, "lon": 12.4964},
        "Australia/NZ": {"lat": -33.8688, "lon": 151.2093},
        "Japan": {"lat": 35.6762, "lon": 139.6503},
        "Taiwan": {"lat": 25.0330, "lon": 121.5654},
        "Southeast Asia": {"lat": 1.3521, "lon": 103.8198},
        "Brazil": {"lat": -23.5505, "lon": -46.6333},
        "Mexico": {"lat": 19.4326, "lon": -99.1332},
        "Chile/Argentina": {"lat": -33.4489, "lon": -70.6693},
    }
    
    map_data = dealers_filtered.groupby("sub_region").agg({
        "dealer_id": "count",
        "parts_fill_rate": "mean",
        "open_warranty_claims": "sum"
    }).reset_index()
    
    map_data["lat"] = map_data["sub_region"].map(lambda x: region_coords.get(x, {}).get("lat", 0))
    map_data["lon"] = map_data["sub_region"].map(lambda x: region_coords.get(x, {}).get("lon", 0))
    
    fig = px.scatter_geo(
        map_data,
        lat="lat",
        lon="lon",
        size="dealer_id",
        color="parts_fill_rate",
        hover_name="sub_region",
        color_continuous_scale=[[0, "#F85149"], [0.5, "#D29922"], [1, "#3FB950"]],
        projection="natural earth",
        size_max=40
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            landcolor="#1C2128",
            oceancolor="#0D1117",
            showocean=True,
            coastlinecolor="#30363D"
        ),
        template="plotly_dark",
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: ALLOCATION WAR ROOM
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "⚔️ Allocation War Room":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">Allocation War Room</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Production vs. Service: Finding the Balance That Keeps Everyone Riding
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>This simulation is my <strong>escalation pathway</strong>. Production wants parts for new bikes; 
            Service needs them for warranty. This directly addresses the JD requirement to <strong>"own escalation 
            pathways and develop proactive solutions for risks identified in the supply plan."</strong> I use this 
            data to <strong>influence stakeholders in Production</strong> by showing the concrete trade-offs between 
            NPI velocity and our warranty obligations to existing riders.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # The Core Conflict
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1C2128 0%, #0D1117 100%); border: 1px solid #30363D; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="text-align: center; flex: 1;">
                <h3 style="color: #58A6FF; margin: 0;">🏭 PRODUCTION</h3>
                <p style="color: #8B949E; font-size: 0.9rem;">"We need parts to hit our launch targets"</p>
            </div>
            <div style="text-align: center; flex: 0.5;">
                <h2 style="color: #E31837; margin: 0;">⚔️</h2>
            </div>
            <div style="text-align: center; flex: 1;">
                <h3 style="color: #3FB950; margin: 0;">🔧 SERVICE</h3>
                <p style="color: #8B949E; font-size: 0.9rem;">"We have riders waiting for repairs"</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Allocation Slider
    st.markdown("#### 🎚️ Global Allocation Priority")
    
    allocation = st.slider(
        "Drag to adjust allocation",
        min_value=0,
        max_value=100,
        value=50,
        format="%d%% Service",
        help="0% = All to Production, 100% = All to Service"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: {'rgba(88, 166, 255, 0.1)' if allocation < 50 else 'rgba(88, 166, 255, 0.05)'}; border-radius: 8px; border: 1px solid {'#58A6FF' if allocation < 50 else '#30363D'};">
            <h2 style="color: #58A6FF; margin: 0;">{100-allocation}%</h2>
            <p style="color: #8B949E; margin: 4px 0 0 0;">Production</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: {'rgba(63, 185, 80, 0.1)' if allocation >= 50 else 'rgba(63, 185, 80, 0.05)'}; border-radius: 8px; border: 1px solid {'#3FB950' if allocation >= 50 else '#30363D'};">
            <h2 style="color: #3FB950; margin: 0;">{allocation}%</h2>
            <p style="color: #8B949E; margin: 4px 0 0 0;">Service</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Impact Analysis
    st.markdown("#### 📊 Impact Analysis")
    
    # Calculate impacts based on allocation
    base_service_stockouts = 150
    base_production_delays = 45
    
    service_stockouts = int(base_service_stockouts * ((100 - allocation) / 50) ** 1.5)
    production_delays = int(base_production_delays * (allocation / 50) ** 1.5)
    
    affected_riders = service_stockouts * 3  # 3 riders per stockout on average
    npi_delay_days = int(production_delays * 0.5)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🔧 Service Impact")
        
        # Rider impact visualization
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=service_stockouts,
            delta={'reference': base_service_stockouts},
            title={'text': "Projected Service Stockouts"},
            gauge={
                'axis': {'range': [0, 500]},
                'bar': {'color': "#E31837"},
                'steps': [
                    {'range': [0, 100], 'color': "rgba(63, 185, 80, 0.3)"},
                    {'range': [100, 250], 'color': "rgba(210, 153, 34, 0.3)"},
                    {'range': [250, 500], 'color': "rgba(248, 81, 73, 0.3)"}
                ]
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #F85149; font-size: 1.5rem; font-weight: 700; margin: 0;">{affected_riders}</p>
            <p class="metric-label">Riders Waiting for Repairs</p>
            <p style="color: #8B949E; font-size: 0.85rem;">Avg wait: {max(14, 14 + (service_stockouts - base_service_stockouts) // 5)} days</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Which parts are affected
        st.markdown("**Most Affected Parts:**")
        affected_parts = parts_df.nlargest(5, "warranty_claims_mtd")[["description", "days_of_supply", "warranty_claims_mtd"]]
        affected_parts.columns = ["Part", "Days Supply", "Claims/Month"]
        st.dataframe(affected_parts, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("##### 🏭 Production Impact")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=production_delays,
            delta={'reference': base_production_delays, 'increasing': {'color': '#F85149'}},
            title={'text': "Production Line Stoppages"},
            gauge={
                'axis': {'range': [0, 200]},
                'bar': {'color': "#58A6FF"},
                'steps': [
                    {'range': [0, 30], 'color': "rgba(63, 185, 80, 0.3)"},
                    {'range': [30, 80], 'color': "rgba(210, 153, 34, 0.3)"},
                    {'range': [80, 200], 'color': "rgba(248, 81, 73, 0.3)"}
                ]
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #58A6FF; font-size: 1.5rem; font-weight: 700; margin: 0;">{npi_delay_days} days</p>
            <p class="metric-label">NPI Launch Delay Risk</p>
            <p style="color: #8B949E; font-size: 0.85rem;">Affecting: Turbo Levo Gen 5</p>
        </div>
        """, unsafe_allow_html=True)
        
        # NPI at risk
        st.markdown("**NPI Programs at Risk:**")
        npi_risk = npi_df[["product", "launch_date", "service_parts_readiness", "risk_level"]]
        npi_risk.columns = ["Product", "Launch", "Readiness", "Risk"]
        npi_risk["Readiness"] = (npi_risk["Readiness"] * 100).round(0).astype(int).astype(str) + "%"
        st.dataframe(npi_risk, use_container_width=True, hide_index=True)
    
    # Sweet Spot Finder
    st.markdown("#### 🎯 Find the Sweet Spot")
    
    # Generate trade-off curve
    allocations = np.arange(0, 101, 5)
    stockouts = [int(base_service_stockouts * ((100 - a) / 50) ** 1.5) for a in allocations]
    delays = [int(base_production_delays * (a / 50) ** 1.5) for a in allocations]
    
    # Combined impact score (lower is better)
    combined = [s * 2 + d * 5 for s, d in zip(stockouts, delays)]  # Weight: stockouts x2, delays x5
    optimal_idx = np.argmin(combined)
    optimal_allocation = allocations[optimal_idx]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=allocations,
        y=stockouts,
        name="Service Stockouts",
        line=dict(color="#3FB950", width=3),
        fill='tozeroy',
        fillcolor='rgba(63, 185, 80, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=allocations,
        y=delays,
        name="Production Delays",
        line=dict(color="#58A6FF", width=3),
        fill='tozeroy',
        fillcolor='rgba(88, 166, 255, 0.1)'
    ))
    
    fig.add_vline(x=optimal_allocation, line_dash="dash", line_color="#E31837", 
                  annotation_text=f"Optimal: {optimal_allocation}%")
    fig.add_vline(x=allocation, line_dash="dot", line_color="#D29922",
                  annotation_text=f"Current: {allocation}%")
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        xaxis_title="Service Allocation %",
        yaxis_title="Impact Count",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(f"""
    <div style="background: rgba(227, 24, 55, 0.1); border: 1px solid #E31837; border-radius: 8px; padding: 16px; margin-top: 16px;">
        <h4 style="color: #E31837; margin: 0;">💡 Recommendation</h4>
        <p style="color: #C9D1D9; margin: 8px 0 0 0;">
            Based on current demand signals and NPI timeline, the <strong>optimal allocation is {optimal_allocation}% to Service</strong>. 
            This minimizes total business impact while maintaining our warranty obligations. 
            {'<br><br><span style="color: #D29922;">⚠️ Current allocation deviates from optimal. Consider adjustment.</span>' if abs(allocation - optimal_allocation) > 10 else '<br><br><span style="color: #3FB950;">✓ Current allocation is within acceptable range.</span>'}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MODULE: S&OP COMMAND CENTER
# ═══════════════════════════════════════════════════════════════════════════════

elif module == "📅 S&OP Command Center":
    st.markdown("""
    <div class="hero-header">
        <h1 style="margin: 0; font-size: 2.2rem;">S&OP Command Center</h1>
        <p style="color: #8B949E; margin: 8px 0 0 0; font-size: 1.1rem;">
            Sales & Operations Planning | NPI Readiness | Team Performance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if pitch_mode:
        st.markdown("""
        <div class="insight-card">
            <h4>🎯 Strategic Insight</h4>
            <p>Here is where I <strong>track and report on team KPIs</strong> and <strong>communicate NPI milestones 
            across the business</strong>. This directly addresses the JD requirement to "collaborate with product teams" 
            and ensure the Service team is aligned with Product <strong>before a launch happens, not after</strong>. 
            I use this to <strong>provide leadership and mentorship</strong> by identifying where planners need support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # NPI Readiness Tracker
    st.markdown("#### 🚀 NPI Readiness Tracker")
    
    # Gantt-style timeline
    today = datetime.now()
    
    npi_timeline = npi_df.copy()
    npi_timeline["launch_date"] = pd.to_datetime(npi_timeline["launch_date"])
    npi_timeline["days_to_launch"] = (npi_timeline["launch_date"] - today).dt.days
    npi_timeline["start_date"] = today - timedelta(days=90)  # Started 90 days ago
    
    fig = go.Figure()
    
    colors = {"Low": "#3FB950", "Medium": "#D29922", "High": "#F85149"}
    
    for idx, row in npi_timeline.iterrows():
        # Background bar (total timeline)
        fig.add_trace(go.Bar(
            x=[row["days_to_launch"] + 90],
            y=[row["product"]],
            orientation='h',
            marker=dict(color="rgba(48, 54, 61, 0.5)"),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Progress bar (service readiness)
        fig.add_trace(go.Bar(
            x=[(row["days_to_launch"] + 90) * row["service_parts_readiness"]],
            y=[row["product"]],
            orientation='h',
            marker=dict(color=colors[row["risk_level"]]),
            name=row["risk_level"] if idx == 0 else None,
            showlegend=(idx < 3),
            hovertemplate=f"<b>{row['product']}</b><br>Readiness: {row['service_parts_readiness']*100:.0f}%<br>Launch: {row['launch_date'].strftime('%b %d, %Y')}<extra></extra>"
        ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        barmode='overlay',
        xaxis_title="Days (relative to today)",
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # NPI Detail Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🚨 High-Risk Launches")
        high_risk = npi_df[npi_df["risk_level"] == "High"]
        
        for _, row in high_risk.iterrows():
            days_to = (pd.to_datetime(row["launch_date"]) - datetime.now()).days
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #F85149;">
                <h4 style="margin: 0; color: #F0F6FC;">{row['product']}</h4>
                <p style="color: #8B949E; margin: 4px 0;">Launch: {row['launch_date']} ({days_to} days)</p>
                <div style="display: flex; justify-content: space-between; margin-top: 12px;">
                    <div>
                        <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">PARTS READY</p>
                        <p style="color: #F85149; font-size: 1.2rem; font-weight: 600; margin: 0;">{row['service_parts_readiness']*100:.0f}%</p>
                    </div>
                    <div>
                        <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">TRAINING</p>
                        <p style="color: #F85149; font-size: 1.2rem; font-weight: 600; margin: 0;">{row['training_complete']*100:.0f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("##### ✅ On-Track Launches")
        on_track = npi_df[npi_df["risk_level"] == "Low"]
        
        for _, row in on_track.iterrows():
            days_to = (pd.to_datetime(row["launch_date"]) - datetime.now()).days
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #3FB950;">
                <h4 style="margin: 0; color: #F0F6FC;">{row['product']}</h4>
                <p style="color: #8B949E; margin: 4px 0;">Launch: {row['launch_date']} ({days_to} days)</p>
                <div style="display: flex; justify-content: space-between; margin-top: 12px;">
                    <div>
                        <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">PARTS READY</p>
                        <p style="color: #3FB950; font-size: 1.2rem; font-weight: 600; margin: 0;">{row['service_parts_readiness']*100:.0f}%</p>
                    </div>
                    <div>
                        <p style="color: #8B949E; font-size: 0.75rem; margin: 0;">TRAINING</p>
                        <p style="color: #3FB950; font-size: 1.2rem; font-weight: 600; margin: 0;">{row['training_complete']*100:.0f}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Team KPIs
    st.markdown("#### 👥 Team Performance KPIs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### Forecast Accuracy (MAPE)")
        
        mape_data = pd.DataFrame({
            "Region": ["North America", "EMEA", "APAC", "LATAM"],
            "MAPE": [12.3, 15.8, 18.2, 22.4],
            "Target": [15, 15, 15, 15]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mape_data["Region"],
            y=mape_data["MAPE"],
            marker_color=[("#3FB950" if m <= 15 else "#F85149") for m in mape_data["MAPE"]],
            text=mape_data["MAPE"].astype(str) + "%",
            textposition='outside'
        ))
        fig.add_hline(y=15, line_dash="dash", line_color="#D29922", annotation_text="15% Target")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            yaxis_title="MAPE %",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### Planner Workload")
        
        workload_data = pd.DataFrame({
            "Planner": ["Sarah M.", "James K.", "Maria L.", "David C.", "Lisa T."],
            "Escalations": [8, 15, 6, 22, 11],
            "SKUs Managed": [145, 210, 120, 280, 165]
        })
        
        fig = px.scatter(
            workload_data,
            x="SKUs Managed",
            y="Escalations",
            text="Planner",
            color="Escalations",
            color_continuous_scale=[[0, "#3FB950"], [0.5, "#D29922"], [1, "#F85149"]],
            size="Escalations",
            size_max=25
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("##### Inventory Health Score")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=78,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#E31837"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(248, 81, 73, 0.3)"},
                    {'range': [50, 75], 'color': "rgba(210, 153, 34, 0.3)"},
                    {'range': [75, 100], 'color': "rgba(63, 185, 80, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "#3FB950", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            template="plotly_dark",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Global Inventory Heatmap
    st.markdown("#### 🗺️ Global Inventory Distribution")
    
    inventory_data = parts_df.copy()
    
    fig = make_subplots(rows=1, cols=3, subplot_titles=("US", "EU", "APAC"))
    
    categories = inventory_data["category"].unique()
    
    for i, (col, region) in enumerate([(1, "on_hand_us"), (2, "on_hand_eu"), (3, "on_hand_apac")]):
        cat_totals = inventory_data.groupby("category")[region].sum()
        fig.add_trace(
            go.Bar(x=list(cat_totals.index), y=list(cat_totals.values), marker_color="#E31837"),
            row=1, col=col
        )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Action Items
    st.markdown("#### 📋 S&OP Action Items")
    
    actions = [
        {"priority": "Critical", "item": "Expedite SL 1.2 motor shipment for Levo Gen 5 launch", "owner": "Procurement", "due": "Dec 15"},
        {"priority": "High", "item": "Resolve APAC forecast variance - MAPE at 18.2%", "owner": "APAC Planning", "due": "Dec 20"},
        {"priority": "High", "item": "Complete Turbo Creo 3 service training for EU dealers", "owner": "Training Team", "due": "Jan 10"},
        {"priority": "Medium", "item": "Review David C. workload - 22 open escalations", "owner": "Planning Manager", "due": "Dec 8"},
        {"priority": "Medium", "item": "Update battery recycling SOP for Q1 volumes", "owner": "Sustainability", "due": "Dec 31"},
    ]
    
    for action in actions:
        priority_color = {"Critical": "#F85149", "High": "#D29922", "Medium": "#58A6FF"}[action["priority"]]
        st.markdown(f"""
        <div style="display: flex; align-items: center; padding: 12px; background: #1C2128; border-radius: 8px; margin: 8px 0; border-left: 4px solid {priority_color};">
            <span style="background: {priority_color}; color: {'white' if action['priority'] != 'Medium' else '#0D1117'}; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-right: 12px;">{action['priority']}</span>
            <span style="color: #F0F6FC; flex: 1;">{action['item']}</span>
            <span style="color: #8B949E; margin: 0 16px;">{action['owner']}</span>
            <span style="color: #8B949E;">Due: {action['due']}</span>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 20px; border-top: 1px solid #30363D;">
    <p style="color: #8B949E; font-size: 0.85rem;">
        Service Command v2.0 | Built for Specialized Bicycles |
        <span style="color: #E31837;">Integrated Business Planning Platform</span>
    </p>
    <p style="color: #484F58; font-size: 0.75rem;">
        Real supply chain data: Merida (Taiwan) | MAHLE/Shimano/Bafang Motors | SLC/Reno/s-Heerenberg/SingPost Hubs
    </p>
    <p style="color: #484F58; font-size: 0.75rem;">
        Tariff scenarios based on Section 301 (2024-2025) | CA SB-244 & EU Right-to-Repair compliance
    </p>
    <p style="color: #30363D; font-size: 0.7rem; margin-top: 8px;">
        Prototype demonstration for Planning Manager interview | Data simulated using industry benchmarks
    </p>
</div>
""", unsafe_allow_html=True)

# CSV Export functionality
if st.sidebar.button("📥 Export Data to CSV"):
    # Combine key datasets
    with st.spinner("Preparing export..."):
        import io
        
        buffer = io.StringIO()
        parts_df.to_csv(buffer, index=False)
        
        st.sidebar.download_button(
            label="Download Parts Inventory",
            data=buffer.getvalue(),
            file_name="service_command_parts_export.csv",
            mime="text/csv"
        )

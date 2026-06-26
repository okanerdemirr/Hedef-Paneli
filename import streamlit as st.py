import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Premium ve Gösterişli Renk Dolu CSS Kodları Kesilmeyi Önleyecek Şekilde Yapılandırıldı
st.markdown("""
    <style>
        .main-title { 
            font-size: 38px !important; 
            font-weight: 800 !important; 
            color: #ffeb3b; 
            margin-bottom: 2px; 
            text-shadow: 0 0 10px rgba(255, 235, 59, 0.5); 
        }
        .subtitle { 
            font-size: 16px !important; 
            color: #94a3b8; 
            margin-bottom: 25px; 
        }
        .section-title { 
            font-size: 24px !important; 
            font-weight: 700 !important; 
            color: #38bdf8; 
            margin-top: 30px; 
            margin-bottom: 18px; 
            border-left: 5px solid #ff4081; 
            padding-left: 12px; 
        }
        div[data-testid="column"] {
            background-color: #1e293b !important;
            border: 2px solid #334155 !important;
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        .card-title { 
            font-size: 14px !important; 
            font-weight: 700 !important; 
            color: #38bdf8; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            margin-bottom: 10px; 
        }
        div[data-testid="stMetricLabel"] { 
            display: none !important; 
        }
        div[data-testid="stMetricValue"] { 
            font-size: 28px !important; 
            font-weight: 700 !important; 
            color: #ffffff !important; 
        }
        div[data-testid="stMetricDelta"] > div {
            background-color: rgba(16, 185, 129, 0.15) !important;
            color: #10b981 !important;
            padding: 4px 10px !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"] {
            font-size: 18px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ff4081 !important;
            border-bottom-color: #ff4081 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Temsilci Performans Kontrol Pan

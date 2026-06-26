import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Premium ve Gösterişli Renk Dolu CSS Kodları Kesilmeyi Önleyecek Şekilde Yapılandırıldı
st.markdown("""
    <style>
        .main-title { 
            font-size: 40px !important; 
            font-weight: 900 !important; 
            background: linear-gradient(45deg, #ff007f, #ffeb3b, #00e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2px; 
            text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);
        }
        .subtitle { 
            font-size: 16px !important; 
            color: #a1a1aa; 
            margin-bottom: 30px; 
            font-weight: 500;
        }
        .section-title { 
            font-size: 26px !important; 
            font-weight: 800 !important; 
            color: #00e5ff; 
            margin-top: 35px; 
            margin-bottom: 20px; 
            border-left: 6px solid #ff007f; 
            padding-left: 15px; 
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
        }
        div[data-testid="column"] {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            border: 2px solid #334155 !important;
            padding: 22px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease;
        }
        div[data-testid="column"]:hover {
            border-color: #00e5ff !important;
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.2) !important;
            transform: translateY(-2px);
        }
        .card-title { 
            font-size: 15px !important; 
            font-weight: 800 !important; 
            color: #00e5ff; 
            text-transform: uppercase; 
            letter-spacing: 1.5px; 
            margin-bottom: 12px; 
        }
        div[data-testid="stMetricLabel"] { 
            display: none !important; 
        }
        div[data-testid="stMetricValue"] { 
            font-size: 32px !important; 
            font-weight: 800 !important; 
            color: #ffffff !important; 
        }
        div[data-testid="stMetricDelta"] > div {
            background-color: rgba(16, 185, 129, 0.2) !important;
            color: #10b981 !important;
            padding: 5px 12px !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
        }
        button[data-baseweb="tab"] {
            font-size: 18px !important;

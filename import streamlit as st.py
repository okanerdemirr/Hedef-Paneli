import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(
    page_title="Temsilci Performans Paneli", 
    layout="wide"
)

# Premium modern tema CSS kodları ve PERFORMANS RENKLERİ entegrasyonu
st.markdown("""
    <style>
        .main-title { font-size: 34px !important; font-weight: 800 !important; color: #ffffff; margin-bottom: 2px; letter-spacing: -0.5px; }
        .subtitle { font-size: 14px !important; color: #94a3b8; margin-bottom: 25px; }
        .section-title { font-size: 22px !important; font-weight: 700 !important; color: #38bdf8; margin-top: 30px; margin-bottom: 18px; border-left: 5px solid #38bdf8; padding-left: 12px; }
        div[data-testid="column"] {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            padding: 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        .card-title { font-size: 14px !important; font-weight: 700 !important; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        div[data-testid="stMetricLabel"] { display: none !important; }
        div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #ffffff !important; }
        div[data-testid="stMetricDelta"] > div {
            background-color: rgba(16, 185, 129, 0.15) !important;
            color: #10b981 !important;
            padding: 4px 10px !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"] {
            font-size: 16px !important;
            font-weight: 600 !important;
            color: #94a3b8 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #38bdf8 !important;
            border-bottom-color: #38bdf8 !important;
        }
        /* PERFORMANS RENKLENDİRME CSS SINIFLARI */
        .color-green { color: #10b981 !important; font-weight: 700 !important; } /* >= %100 */
        .color-yellow { color: #fbbf24 !important; font-weight: 700 !important; } /* %80-%99 */
        .color-red { color: #ef4444 !important; font-weight: 700 !important; } /* <= %79 */
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Temsilci Performans Kontrol Paneli</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Şirket genel hedefleri ve dinamik temsilci performans matrisi</div>', unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.markdown("### ⚙️ Veri Kontrol Paneli")
arama_filtresi = st.sidebar.text_input("👤 Temsilci Ara (Dinamik)", "").strip().lower()

if st.sidebar.button("🔄 Verileri Yenile / Sıfırla"):
    st.cache_data.clear()
    st.rerun()

def clean_val(val):
    if pd.isna(val): 
        return 0
    v_str = str(val).strip()
    if v_str in ['None', 'nan', '-', '']: 
        return 0
    if '%' in v_str:
        try: 
            return float(v_str.replace('%', '').replace(',', '.')) / 100

import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Premium modern tema CSS kodları
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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Temsilci Performans Kontrol Paneli</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Şirket genel hedefleri ve dinamik temsilci performans matrisi</div>', unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Veri Kontrol Paneli")
arama_filtresi = st.sidebar.text_input("👤 Temsilci Ara (Dinamik)", "").strip().lower()

if st.sidebar.button("🔄 Verileri Yenile / Sıfırla"):
    st.cache_data.clear()
    st.rerun()

def clean_val(val):
    if pd.isna(val): return 0
    v_str = str(val).strip()
    if v_str in ['None', 'nan', '-', '']: return 0
    if '%' in v_str:
        v_str = v_str.replace('%', '').replace(',', '.')
        try: return float(v_str) / 100
        except: return 0
    try:
        if '.' in v_str or ',' in v_str: return float(v_str.replace(',', '.'))
        return int(v_str)
    except: return 0

# Kırpılmayı önlemek adına string formatlama satırları kısaltıldı ve bölündü
def format_val(val, col_name, is_gelme_orani=False):
    c_lower = str(col_name).lower()
    is_percent_col = (
        'oran' in c_lower or 
        '%' in c_lower or 
        'başarı' in c_lower or 
        'verimlilik' in c_lower or 
        'ortalama' in c_lower
    )
    if is_percent_col:
        v_show = val if is_gelme_orani else (val if val <= 5.0 else val / 100.0)
        if is_gelme_orani and v_show <= 5.0:
            v_show = v_show * 100.0
        return f"{v_show:.1%}" if not is_gelme_orani else f"{v_show:.1f}%"
        
    if isinstance(val, (int, float)):
        if val == int(val): 
            return f"{int(val):,}"
        return f"{val:,.2f}"
    return str(val)

def tr_lower(text):
    if not text: return ""
    text = str(text).strip()
    text = text.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ç", "ç")
    return text.lower()

def dinamik_renk_kurali_hibrit(val, page_type="standart"):
    try:
        if isinstance(val, str) and '%'

import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Kırpılmayı önlemek amacıyla parıltılı neon CSS blokları güvenli satırlara bölündü
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
            font-weight: 700 !important;
            color: #94a3b8 !important;
            padding: 12px 24px !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #ff007f !important;
            border-bottom-color: #ff007f !important;
            background-color: rgba(255, 0, 127, 0.05) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Başlık metinleri güvenli biçimde güncellendi
st.markdown('<h1 class="main-title">📊 Temsilci Performans Kontrol Paneli</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Şirket genel hedefleri ve dinamik temsilci performans matrisi</p>', unsafe_allow_html=True)

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

def format_val(val, col_name, is_gelme_orani=False):
    c_lower = str(col_name).lower()
    is_oran_col = (
        'oran' in c_lower or 
        '%' in c_lower or 
        'başarı' in c_lower or 
        'verimlilik' in c_lower or 
        'ortalama' in c_lower
    )
    if is_oran_col:
        if is_gelme_orani:
            v_show = val if val > 5.0 else val * 100.0
            return "{:.1f}%".format(v_show)
        v_show = val if val <= 5.0 else val / 100.0
        return "{:.1%}".format(v_show)
    if isinstance(val, (int, float)):
        if val == int(val): return "{:,}".format(int(val))
        return "{:,.2f}".format(val)
    return str(val)

def tr_lower(text):
    if not text: return ""
    text = str(text).strip()
    text = text.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ç", "ç")
    return text.lower()

def dinamik_renk_kurali_hibrit(val, page_type="standart"):
    try:
        if isinstance(val, str) and '%' in val:
            v = float(val.replace('%', '').replace(',', '.')) / 100
        else:
            v = float(val)
            if v > 5.0: v = v / 100.0
        
        if page_type == "verimlilik":
            if v >= 0.80

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

def clean_val(val, is_ozel_sayfa=False):
    if pd.isna(val): return 0
    v_str = str(val).strip()
    if v_str in ['None', 'nan', '-', '']: return 0
    
    if '%' in v_str:
        v_str = v_str.replace('%', '').replace(',', '.')
        try: return float(v_str) / 100.0
        except: return 0
        
    try:
        if ',' in v_str:
            v_str = v_str.replace(',', '.')
            
        res = float(v_str)
        
        # Excel'den metin formatında "85" veya "91.2" gibi gelmişse orana (0.85) çevirir
        if is_ozel_sayfa and res > 1.0:
            return res / 100.0
            
        return res
    except:
        return 0

def format_val(val, col_name):
    c_lower = str(col_name).lower()
    # Sütun adı sadece "Verimlilik" olsa bile algılaması için "verimlilik" kontrolü eklendi
    if 'oran' in c_lower or '%' in c_lower or 'başarı' in c_lower or 'verimlilik' in c_lower:
        return "{:.1%}".format(val)
    if isinstance(val, (int, float)):
        if val == int(val): return "{:,}".format(int(val))
        return "{:,.2f}".format(val)
    return str(val)

def tr_lower(text):
    if not text: return ""
    text = str(text).strip()
    text = text.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ç", "ç")
    return text.lower()

# Dinamik Renklendirme Motoru
def dinamik_renk_kurali_hibrit(val, page_type="std"):
    try:
        if isinstance(val, str) and '%' in val:
            v = float(val.replace('%', '').replace(',', '.')) / 100.0
        else:
            v = float(val)
            if v > 1.0: v = v / 100.0
        
        # Verimlilik sayfası kuralı: %80 ve üzeri Yeşil, altı Kırmızı
        if page_type == "verimlilik":
            if v >= 0.80: return 'color: #10b981; font-weight: bold;'
            return 'color: #ef4444; font-weight: bold;'
            
        # Kriter dışı sayfası kuralı: %20 ve altı Yeşil, üzeri Kırmızı
        elif page_type == "kriter":
            if v <= 0.20: return 'color: #10b981; font-weight: bold;'
            return 'color: #ef4444; font-weight: bold;'
            
        # Gelme oranı sayfası kuralı: %40 ve üzeri Yeşil, altı Kırmızı
        elif page_type == "gelme":
            if v >= 0.40: return 'color: #10b981; font-weight: bold;'
            return 'color: #ef4444; font-weight: bold;'
            
        # Standart/Diğer sayfalar kuralı
        else:
            if v >= 0.80: return 'color: #10b981; font-weight: bold;'
            return 'color: #ef4444; font-weight: bold;'
    except: 
        return ''

uploaded_file = None
kaynak_baglantilar = [
    "https://raw.githubusercontent.com/okanerdemirr/Hedef-Paneli/main/veri.xlsx.xlsx",
    "https://raw.githubusercontent.com/okanerdemirr/Hedef-Paneli/main/veri.xlsx",
    "https://raw.githubusercontent.com/okanerdemirr/Hedef-Paneli/main/veri"
]

for url in kaynak_baglantilar:
    try:
        f_excel = pd.ExcelFile(url)
        if f_excel is not None:
            uploaded_file = f_excel
            break
    except: continue

if uploaded_file is not None:
    all_sheets = uploaded_file.sheet_names

    kpi_toplamlar = {
        "Lead": {"hedef": 0, "gerceklesen": 0, "oran_val": 0},
        "Gelen Rezervasyon": {"hedef": 0, "gerceklesen": 0, "oran_val": 0},
        "Satış": {"hedef": 0, "gerceklesen": 0, "oran_val": 0},
        "Kriter Dışı": {"hedef": 0, "gerceklesen": 0, "oran_val": 0},
        "Gelme Oranı": {"hedef": 0, "gerceklesen": 0, "oran_val": 0}
    }
    
    if "Genel Hedef" in all_sheets:
        df_g = pd.read_excel(uploaded_file, sheet_name="Genel Hedef", header=None)
        for r in range(len(df_g)):
            h_adi = tr_lower(df_g.iloc[r, 0]).replace('\n', ' ')
            if not h_adi or h_adi == 'nan': continue
            
            v1 = clean_val(df_g.iloc[r, 1], False)
            v2 = clean_val(df_g.iloc[r, 2], False)
            v3 = clean_val(df_g.iloc[r, 3], False) if df_g.shape[1] > 3 else 0
            
            oran_val = v3 if v3 > 0 else (v2 / v1 if v1 > 0 else 0)
            is_kpi = any(x in h_adi for x in ["lead", "rezervasyon", "hedef"])
            
            if oran_val > 1 and not is_kpi: oran_val = oran

import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(
    page_title="Pano",
    layout="wide"
)

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
        box-shadow: 0 4px 6px -1px rgba(0,0,0, 0.1) !important;
    }
    .card-title { font-size: 14px !important; font-weight: 700 !important; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    div[data-testid="stMetricLabel"] { display: none !important; }
    div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Temsilci Performans Kontrol Paneli</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Şirket genel hedefleri ve dinamik temsilci performans matrisi</div>', unsafe_allow_html=True)

# GitHub'a yüklediğin olası iki dosya ismini de kontrol ediyoruz:
urls = [
    "https://raw.githubusercontent.com/okanerdemirr/Hedef-Paneli/main/veri.xlsx.xlsx",
    "https://raw.githubusercontent.com/okanerdemirr/Hedef-Paneli/main/veri"
]

df = None
for url in urls:
    try:
        df = pd.read_excel(url)
        break
    except:
        continue

if df is not None:
    st.markdown('<div class="section-title">👤 Temsilci Filtreleme ve Durum</div>', unsafe_allow_html=True)
    
    sutunlar = df.columns.tolist()
    temsilci_sutunu = None
    for col in sutunlar:
        if 'temsilci' in str(col).lower() or 'ad' in str(col).lower():
            temsilci_sutunu = col
            break
            
    if temsilci_sutunu:
        temsilciler = ["Hepsi"] + sorted(df[temsilci_sutunu].unique().tolist())
        secilen_temsilci = st.selectbox("İncelemek İstediğiniz Temsilciyi Seçin:", temsilciler)
        
        # Hatalı satır düzeltildi:
        if secilen_temsilci != "Hepsi":
            df_filtrelenmis = df[df[temsilci_sutunu] == secilen_temsilci]
        else:
            df_filtrelenmis = df
    else:
        df_filtrelenmis = df
        st.info("Filtreleme sütunu otomatik algılanamadı, tüm veriler listeleniyor.")

    st.markdown('<div class="section-title">📈 Performans Grafikleri ve Veri Tablosu</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card-title">Genel Dağılım Grafiği</div>', unsafe_allow_html=True)
        if len(df_filtrelenmis.columns) >= 2:
            fig = px.bar(df_filtrelenmis, x=df_filtrelenmis.columns[0], y=df_filtrelenmis.columns[1], template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.markdown('<div class="card-title">Detaylı Veri Listesi</div>', unsafe_allow_html=True)
        st.dataframe(df_filtrelenmis, use_container_width=True)
else:
    st.error("GitHub üzerinde 'veri' veya 'veri.xlsx.xlsx' dosyası bulunamadı.")

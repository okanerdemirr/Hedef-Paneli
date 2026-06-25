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
        except: 
            return 0
    try:
        if '.' in v_str or ',' in v_str:
            return float(v_str.replace(',', '.'))
        else:
            return int(v_str)
    except: 
        return 0

def format_val(val, col_name):
    c_lower = str(col_name).lower()
    if 'oran' in c_lower or '%' in c_lower or 'başarı' in c_lower:
        if val <= 1:
            return "{:.1%}".format(val)
        else:
            return "{:.1f}%".format(val)
    if isinstance(val, (int, float)):
        if val == int(val):
            return "{:,}".format(int(val))
        return "{:,.2f}".format(val)
    return str(val)

def tr_lower(text):
    if not text:
        return ""
    text = str(text).strip()
    text = text.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ").replace("Ü", "ü").replace("Ç", "ç")
    return text.lower()

# Tablo hücrelerini kurallara göre (Yeşil, Sarı, Kırmızı) renklendiren kararlı fonksiyon
def renk_kurali(val):
    try:
        if isinstance(val, str) and '%' in val:
            v = float(val.replace('%', '').replace(',', '.')) / 100
        else:
            v = float(val)
        
        if v >= 1.0:
            return 'color: #10b981; font-weight: bold;' # >= %100 Yeşil
        elif v >= 0.8:
            return 'color: #fbbf24; font-weight: bold;' # %80 - %99 Sarı
        else:
            return 'color: #ef4444; font-weight: bold;' # <= %79 Kırmızı
    except:
        return ''

# --- OTOMATİK ARKA PLAN DOSYA MOTORU ---
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
    except:
        continue

# --- MAIN ENGINE ---
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
            if not h_adi or h_adi == 'nan': 
                continue
            
            v1 = clean_val(df_g.iloc[r, 1])
            v2 = clean_val(df_g.iloc[r, 2])
            v3 = clean_val(df_g.iloc[r, 3]) if df_g.shape[1] > 3 else 0
            
            oran_val = v3 if v3 > 0 else (v2 / v1 if v1 > 0 else 0)
            is_kpi = any(x in h_adi for x in ["lead", "rezervasyon", "hedef"])
            
            if oran_val > 1 and not is_kpi:
                oran_val = oran_val / 100

            if "lead" in h_adi:
                kpi_toplamlar["Lead"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "gelen" in h_adi and "rezerv" in h_adi:
                kpi_toplamlar["Gelen Rezervasyon"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "sat" in h_adi:
                kpi_toplamlar["Satış"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "kriter" in h_adi:
                kpi_toplamlar["Kriter Dışı"] = {"hedef": v1 if v1 <= 1 else v1/100, "gerceklesen": v2 / 100 if v2 > 1 else v2, "oran_val": v2/100 if v2 > 1 else v2}
            elif "gelme" in h_adi:
                kpi_toplamlar["Gelme Oranı"] = {"hedef": v1 if v1 <= 1 else v1/100, "gerceklesen": v2 / 100 if v2 > 1 else v2, "oran_val": v2/100 if v2 > 1 else v2}

    st.markdown('<div class="section-title">⚡ Şirket Genel Performans Matrisi</div>', unsafe_allow_html=True)
    ana_kpi_sirasi = ["Lead", "Gelen Rezervasyon", "Satış", "Kriter Dışı", "Gelme Oranı"]
    cols = st.columns(len(ana_kpi_sirasi))
    
    for idx, name in enumerate(ana_kpi_sirasi):
        with cols[idx]:
            st.markdown('<div class="card-title">💎 {}</div>'.format(name), unsafe_allow_html=True)
            h_data = kpi_toplamlar[name]["hedef"]
            g_data = kpi_toplamlar[name]["gerceklesen"]
            o_data = kpi_toplamlar[name]["oran_val"]
            
            if name in ["Gelme Oranı", "Kriter Dışı"]:
                h_str = "Hedef: {:.1%}".format(h_data) if h_data <= 1 else "Hedef: {:.1f}%".format(h_data)
                g_str = "{:.1%}".format(g_data) if g_data <= 1 else "{:.1f}%".format(g_data)
                st.markdown('<div style="color:#94a3b8; font-size:13px; margin-bottom:5px;">{}</div>'.format(h_str), unsafe_allow_html=True)
                st.metric(label="", value=g_str, delta="Gerçekleşen", delta_color="normal")
            else:
                h_str = "Hedef: {:,}".format(int(h_data))
                g_str = "{:,}".format(int(g_data))
                st.markdown('<div style="color:#94a3b8; font-size:13px; margin-bottom:5px;">{}</div>'.format(h_str), unsafe_allow_html=True)
                st.metric(label="", value=g_str, delta="Başarı: {:.1%}".format(o_data), delta_color="normal")

    st.markdown('<hr style="border-top: 1px solid #334155; margin-top:30px; margin-bottom:20px;">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Temsilci Performans Kırılımları</div>', unsafe_allow_html=True)

    hedef_sayfalari = [s for s in all_sheets if ("hedef" in s.lower() or "analiz" in s.lower() or "ulasim" in s.lower() or "ulaşım" in s.lower()) and "genel" not in s.lower()]
    
    if hedef_sayfalari:
        sekme_isimleri = [sheet.replace("Hedef", "").replace("hedef", "").strip() for sheet in hedef_sayfalari]
        sekmeler = st.tabs(sekme_isimleri)
        
        for idx, sheet in enumerate(hedef_sayfalari):
            with sekmeler[idx]:
                df_sheet = pd.read_excel(uploaded_file, sheet_name=sheet, header=None)
                if len(df_sheet) == 0:
                    continue
                    
                tablo_basligi = sekme_isimleri[idx]
                sutun_isimleri = [str(df_sheet.iloc[0, col_idx]).strip() for col_idx in range(df_sheet.shape[1])]
                sutun_isimleri = [name if (name and name != 'nan') else "Sütun {}".format(i) for i, name in enumerate(sutun_isimleri)]
                
                kpi_tablo_rows = []
                toplam_satir_data = None
                
                for r in range(1, len(df_sheet)):
                    t_isim = str(df_sheet.iloc[r, 0]).strip()
                    t_isim_lower = tr_lower(t_isim)
                    
                    if not t_isim or t_isim == '' or t_isim_lower == 'nan':
                        continue
                        
                    row_data = {}
                    row_data[sutun_isimleri[0]] = t_isim
                    
                    for col_idx in range(1, df_sheet.shape[1]):
                        raw_val = df_sheet.iloc[r, col_idx]
                        cleaned = clean_val(raw_val)
                        row_data[sutun_isimleri[col_idx]] = cleaned
                    
                    if 'toplam' in t_isim_lower or 'genel' in t_isim_lower:
                        row_data[sutun_isimleri[0]] = '🔴 Genel Toplam'
                        formatted_toplam = {}
                        for k, v in row_data.items():
                            if k == sutun_isimleri[0]:
                                formatted_toplam[k] = v
                            else:
                                formatted_toplam[k] = format_val(v, k)
                        toplam_satir_data = formatted_toplam
                        continue
                    
                    if arama_filtresi == "" or arama_filtresi in t_isim_lower:
                        kpi_tablo_rows.append(row_data)
                
                grafik_df = pd.DataFrame(kpi_tablo_rows).copy()
                
                formatted_rows = []
                for row in kpi_tablo_rows:
                    f_row = {}
                    for k, v in row.items():
                        if k == sutun_isimleri[0]:
                            f_row[k] = v
                        else:
                            f_row[k] = format_val(v, k)
                    formatted_rows.append(f_row)
                    
                if toplam_satir_data and arama_filtresi == "":
                    formatted_rows.append(toplam_satir_data)
                    
                if len(formatted_rows) > 0 and not (len(formatted_rows) == 1 and formatted_rows[0][sutun_isimleri[0]] == '🔴 Genel Toplam'):
                    st.markdown("#### 📁 {} Veri Seti".format(tablo_basligi))
                    kpi_tablo_df = pd.DataFrame(formatted_rows)
                    
                    # 🔴 GÜVENLİ PANDAS STYLER RENKLENDİRME MOTORU
                    oran_sutunu = sutun_isimleri[-1] 
                    try:
                        styled_df = kpi_tablo_df.style.map(renk_kurali, subset=[oran_sutunu])
                        st.dataframe(styled_df, width="stretch", hide_index=True)
                    except:
                        st.dataframe(kpi_tablo_df, width="stretch", hide_index=True)
                    
                    y_ekseni = sutun_isimleri[1:-1] if ('oran' in sutun_isimleri[-1].lower() or '%' in sutun_isimleri[-1].lower()) else sutun_isimleri[1:]
                    
                    if not grafik_df.empty and len(y_ekseni) > 0:
                        # Grafik barlarının rengini temsilcinin başarı oranına göre grupluyoruz
                        grafik_df['Grafik_Renk'] = grafik_df[sutun_isimleri[-1]].apply(
                            lambda x: 'Yüksek (>=%100)' if x >= 1.0 else ('Orta (%80-%99)' if x >= 0.8 else 'Düşük (<%80)')
                        )
                        
                        fig = px.bar(
                            grafik_df, 
                            x=sutun_isimleri[0], 
                            y=y_ekseni, 
                            barmode='group', 
                            template="plotly_dark", 
                            height=300,
                            color='Grafik_Renk',
                            color_discrete_map={
                                'Yüksek (>=%100)': '#10b981', # Canlı Yeşil
                                'Orta (%80-%99)': '#fbbf24',  # Canlı Sarı
                                'Düşük (<%80)': '#ef4444'     # Canlı Kırmızı
                            }
                        )
                        
                        fig.update_layout(
                            margin=dict(l=20, r=20, t=20, b=20),
                            legend_title_text='Performans Durumu',
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        
                        st.plotly_chart(fig, width="stretch", use_container_width=True)
    else:
        st.info("ℹ️ Temsilci hedeflerine ait detaylı alt sayfalar bulunamadı.")
else:
    st.markdown("---")
    st.warning("⚠️ **GitHub Deponuzdaki Excel Dosyası Okunamadı!**")
    st.info("💡 **Çözüm:** Bilgisayarınızdaki güncel Excel dosyasının adını küçük harflerle tamamen **`veri.xlsx`** yapın ve GitHub'a yükleyin. Sistem dosyayı algıladığı an paneliniz anında açılacaktır.")

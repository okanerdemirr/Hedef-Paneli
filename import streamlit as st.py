import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Orijinal metrik stilini koruyarak her kutuya farklı renk çerçeve veren CSS yapısı
css = '<style>'
css += '.main-title {'
css += ' font-size: 40px !important;'
css += ' font-weight: 900 !important;'
css += ' background: linear-gradient(45deg, #ff007f, #ffeb3b, #00e5ff);'
css += ' -webkit-background-clip: text;'
css += ' -webkit-text-fill-color: transparent;'
css += ' margin-bottom: 2px;'
css += ' text-shadow: 0 0 20px rgba(0, 229, 255, 0.3);'
css += '}'
css += '.subtitle { font-size: 16px !important; color: #a1a1aa; margin-bottom: 30px; font-weight: 500; }'
css += '.section-title { font-size: 26px !important; font-weight: 800 !important; color: #00e5ff; margin-top: 35px; margin-bottom: 20px; border-left: 6px solid #ff007f; padding-left: 15px; text-shadow: 0 0 10px rgba(0, 229, 255, 0.2); }'
# Orijinal metrik sütunlarını yakalayıp renkli çerçeve ekleyen bloklar
css += 'div[data-testid="column"]:nth-of-type(1) {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;'
css += ' border: 2px solid #ff007f !important; padding: 20px !important; border-radius: 14px !important;'
css += ' box-shadow: 0 0 15px rgba(255, 0, 127, 0.2) !important; transition: all 0.3s ease;'
css += '}'
css += 'div[data-testid="column"]:nth-of-type(2) {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;'
css += ' border: 2px solid #00e5ff !important; padding: 20px !important; border-radius: 14px !important;'
css += ' box-shadow: 0 0 15px rgba(0, 229, 255, 0.2) !important; transition: all 0.3s ease;'
css += '}'
css += 'div[data-testid="column"]:nth-of-type(3) {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;'
css += ' border: 2px solid #ffeb3b !important; padding: 20px !important; border-radius: 14px !important;'
css += ' box-shadow: 0 0 15px rgba(255, 235, 59, 0.2) !important; transition: all 0.3s ease;'
css += '}'
css += 'div[data-testid="column"]:nth-of-type(4) {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;'
css += ' border: 2px solid #9c27b0 !important; padding: 20px !important; border-radius: 14px !important;'
css += ' box-shadow: 0 0 15px rgba(156, 39, 176, 0.2) !important; transition: all 0.3s ease;'
css += '}'
css += 'div[data-testid="column"]:nth-of-type(5) {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;'
css += ' border: 2px solid #ff5722 !important; padding: 20px !important; border-radius: 14px !important;'
css += ' box-shadow: 0 0 15px rgba(255, 87, 34, 0.2) !important; transition: all 0.3s ease;'
css += '}'
css += 'div[data-testid="column"]:hover { transform: translateY(-2px) !important; }'
css += '.card-title { font-size: 14px !important; font-weight: 700 !important; color: #38bdf8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }'
css += 'div[data-testid="stMetricLabel"] { display: none !important; }'
css += 'div[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; color: #ffffff !important; }'
css += 'div[data-testid="stMetricDelta"] > div { background-color: rgba(16, 185, 129, 0.15) !important; color: #10b981 !important; padding: 4px 10px !important; border-radius: 6px !important; font-weight: 600 !important; }'
# Alt sekmelerin (Tabs) her birinin farklı renk çerçeve alması için CSS sınıfları
css += 'button[data-baseweb="tab"] { font-size: 16px !important; font-weight: 700 !important; color: #94a3b8 !important; padding: 12px 20px !important; background: #1e293b !important; border-radius: 10px !important; margin-right: 8px !important; transition: all 0.3s ease !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(1) { border: 2px solid #ff007f !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(2) { border: 2px solid #00e5ff !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(3) { border: 2px solid #ffeb3b !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(4) { border: 2px solid #10b981 !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(5) { border: 2px solid #ff5722 !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(6) { border: 2px solid #9c27b0 !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(7) { border: 2px solid #2196f3 !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(8) { border: 2px solid #e91e63 !important; }'
css += 'button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff !important; background: rgba(255, 255, 255, 0.08) !important; box-shadow: 0 0 15px rgba(255, 255, 255, 0.15) !important; }'
css += 'div[data-testid="stTab"] { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important; border: 2px solid #334155 !important; padding: 25px !important; border-radius: 16px !important; margin-top: 15px !important; }'
# Her sekmedeki tabloyu altın sarısı parıltılı çerçeveye alan sınıf
css += 'div[data-testid="stDataFrame"] { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important; border: 3px solid #FFD700 !important; border-radius: 16px !important; padding: 15px !important; box-shadow: 0 0 25px rgba(255, 215, 0, 0.3) !important; margin-top: 10px !important; margin-bottom: 20px !important; }'
css += '</style>'
st.markdown(css, unsafe_allow_html=True)

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
        # Lokman Tan'ın Excel'deki 1 ile 5 arasındaki ham düz sayı format hatasını çözen akıllı filtre
        if 1.0 < val <= 5.0 and not is_gelme_orani:
            val = val / 100.0
            
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
            # Lokman Tan'ın tablodaki renklendirme motorunu düzelten filtre
            if 1.0 < v <= 5.0:
                v = v / 100.0
            elif v > 5.0:
                v = v / 100.0
        
        if page_type == "verimlilik":
            if v >= 0.80: return 'color: #10b981; font-weight: bold;'
            return 'color: #ff007f; font-weight: bold;'
        elif page_type == "kriter":
            if v <= 0.20: return 'color: #10b981; font-weight: bold;'
            return 'color: #ff007f; font-weight: bold;'
        elif page_type == "gelme":
            if v >= 0.40: return 'color: #10b981; font-weight: bold;'
            return 'color: #ff007f; font-weight: bold;'
        else:
            if v >= 1.0: return 'color: #10b981; font-weight: bold;'
            if v >= 0.8: return 'color: #ffeb3b; font-weight: bold;'
            return 'color: #ff007f; font-weight: bold;'
    except: return ''

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
            
            v1 = clean_val(df_g.iloc[r, 1])
            v2 = clean_val(df_g.iloc[r, 2])
            v3 = clean_val(df_g.iloc[r, 3]) if df_g.shape[1] > 3 else 0
            
            oran_val = v3 if v3 > 0 else (v2 / v1 if v1 > 0 else 0)
            is_kpi = any(x in h_adi for x in ["lead", "rezervasyon", "hedef"])
            
            if oran_val > 1 and not is_kpi: oran_val = oran_val / 100

            if "lead" in h_adi: 
                kpi_toplamlar["Lead"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "gelen" in h_adi and "rezerv" in h_adi: 
                kpi_toplamlar["Gelen Rezervasyon"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "sat" in h_adi: 
                kpi_toplamlar["Satış"] = {"hedef": v1, "gerceklesen": v2, "oran_val": oran_val}
            elif "kriter" in h_adi: 
                h_v = v1 if v1 <= 1 else v1/100
                g_v = v2 / 100 if v2 > 1 else v2
                o_v = v2/100 if v2 > 1 else v2
                kpi_toplamlar["Kriter Dışı"] = {"hedef": h_v, "gerceklesen": g_v, "oran_val": o_v}
            elif "gelme" in h_adi: 
                h_v = v1 if v1 <= 1 else v1/100
                g_v = v2 / 100 if v2 > 1 else v2
                o_v = v2/100 if v2 > 1 else v2
                kpi_toplamlar["Gelme Oranı"] = {"hedef": h_v, "gerceklesen": g_v, "oran_val": o_v}

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

    hedef_sayfalari = [s for s in all_sheets if ("hedef" in s.lower() or "analiz" in s.lower() or "ulasim" in s.lower() or "ulaşım" in s.lower() or "verimlilik" in s.lower()) and "genel" not in s.lower()]
    
    if hedef_sayfalari:
        sekme_isimleri = [sheet.replace("Hedef", "").replace("hedef", "").strip() for sheet in hedef_sayfalari]
        sekmeler = st.tabs(sekme_isimleri)
        
        for idx, sheet in enumerate(hedef_sayfalari):
            with sekmeler[idx]:
                df_sheet = pd.read_excel(uploaded_file, sheet_name=sheet, header=None)
                if len(df_sheet) == 0: continue
                    
                tablo_basligi = sekme_isimleri[idx]
                is_gelme_orani_page = "gelme" in sheet.lower()
                is_kriter_disi_page = "kriter" in sheet.lower()
                is_verimlilik_page = "verimlilik" in sheet.lower()
                
                current_page_type = "standart"
                if is_kriter_disi_page: current_page_type = "kriter"
                elif is_gelme_orani_page: current_page_type = "gelme"
                elif is_verimlilik_page: current_page_type = "verimlilik"
                
                sutun_isimleri = [str(df_sheet.iloc[0, col_idx]).strip() for col_idx in range(df_sheet.shape[1])]
                sutun_isimleri = [name if (name and name != 'nan') else "Sütun {}".format(i) for i, name in enumerate(sutun_isimleri)]
                
                kpi_tablo_rows = []
                toplam_satir_data = None
                
                for r in range(1, len(df_sheet)):
                    t_isim = str(df_sheet.iloc[r, 0]).strip()
                    t_isim_lower = tr_lower(t_isim)
                    
                    if not t_isim or t_isim == '' or t_isim_lower == 'nan': continue
                        
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
                            if k == sutun_isimleri[0]: formatted_toplam[k] = v
                            else: formatted_toplam[k] = format_val(v, k, is_gelme_orani_page)
                        toplam_satir_data = formatted_toplam
                        continue
                    
                    if arama_filtresi == "" or arama_filtresi in t_isim_lower: kpi_tablo_rows.append(row_data)
                
                grafik_df = pd.DataFrame(kpi_tablo_rows).copy()
                
                formatted_rows = []
                for row in kpi_tablo_rows:
                    f_row = {}
                    for k, v in row.items():
                        if k == sutun_isimleri[0]: f_row[k] = v
                        else: 
                            # Lokman Tan'ın tablodaki hücre verisini düzelten filtre
                            if k == oran_sutunu and 1.0 < v <= 5.0:
                                v = v / 100.0
                            f_row[k] = format_val(v, k, is_gelme_orani_page)
                    formatted_rows.append(f_row)
                    
                if toplam_satir_data and arama_filtresi == "": formatted_rows.append(toplam_satir_data)
                    
                if len(formatted_rows) > 0 and not (len(formatted_rows) == 1 and formatted_rows[0][sutun_isimleri[0]] == '🔴 Genel Toplam'):
                    st.markdown("#### 📁 {} Veri Seti".format(tablo_basligi))
                    kpi_tablo_df = pd.DataFrame(formatted_rows)
                    
                    oran_sutunu = sutun_isimleri[-1] 
                    try:
                        styled_df = kpi_tablo_df.style.map(lambda x: dinamik_renk_kurali_hibrit(x, current_page_type), subset=[oran_sutunu])
                        st.dataframe(styled_df, width="stretch", hide_index=True)
                    except:
                        st.dataframe(kpi_tablo_df, width="stretch", hide_index=True)
                    
                    if is_verimlilik_page:
                        y_ekseni = [oran_sutunu]
                    else:
                        y_ekseni = sutun_isimleri[1:-1] if ('oran' in sutun_isimleri[-1].lower() or '%' in sutun_isimleri[-1].lower() or 'verimlilik' in sutun_isimleri[-1].lower() or 'ortalama' in sutun_isimleri[-1].lower()) else sutun_isimleri[1:]
                    
                    if not grafik_df.empty and len(y_ekseni) > 0:
                        def get_bar_label(x, p_type):
                            # Grafik verisi düzeltmesi
                            if x > 5.0: x = x / 100.0
                            if p_type == "kriter":
                                return 'Başarılı (<=%20)' if (x <= 0.20) else 'Yetersiz (>%20)'
                            elif p_type == "gelme":
                                return 'Başarılı (>=%40)' if (x >= 0.40) else 'Yetersiz (<%40)'
                            elif p_type == "verimlilik":
                                return 'Başarılı (>=%80)' if (x >= 0.80) else 'Yetersiz (<%80)'
                            else:
                                if x >= 1.0: return 'Yüksek (>=%100)'
                                if x >= 0.8: return 'Orta (%80-%99)'
                                return 'Düşük (<%80)'

                        grafik_df['Grafik_Renk'] = grafik_df[oran_sutunu].apply(lambda x: get_bar_label(x, current_page_type))
                        
                        if current_page_type == "kriter":
                            color_map = {'Başarılı (<=%20)': '#10b981', 'Yetersiz (>%20)': '#ff007f'}
                        elif current_page_type == "gelme":
                            color_map = {'Başarılı (>=%40)': '#10b981', 'Yetersiz (<%40)': '#ff007f'}
                        elif current_page_type == "verimlilik":
                            color_map = {'Başarılı (>=%80)': '#10b981', 'Yetersiz (<%80)': '#ff007f'}
                        else:
                            color_map = {'Yüksek (>=%100)': '#10b981', 'Orta (%80-%99)': '#ffeb3b', 'Düşük (<%80)': '#ff007f'}
                        
                        fig = px.bar(
                            grafik_df, 
                            x=sutun_isimleri[0], 
                            y=y_ekseni, 
                            barmode='group', 
                            template="plotly_dark", 
                            height=300,
                            color='Grafik_Renk',
                            color_discrete_map=color_map
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

import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Tüm CSS blokları kırpılmayı önlemek amacıyla alt alta küçük parçalara bölündü
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
css += '.subtitle {'
css += ' font-size: 16px !important;'
css += ' color: #a1a1aa;'
css += ' margin-bottom: 30px;'
css += ' font-weight: 500;'
css += '}'
css += '.section-title {'
css += ' font-size: 26px !important;'
css += ' font-weight: 800 !important;'
css += ' color: #00e5ff;'
css += ' margin-top: 35px;'
css += ' margin-bottom: 20px;'
css += ' border-left: 6px solid #ff007f;'
css += ' padding-left: 15px;'
css += ' text-shadow: 0 0 10px rgba(0, 229, 255, 0.2);'
css += '}'
# Üst matris el yapımı neon kutuların CSS sınıfları
css += '.neon-box {'
css += ' background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);'
css += ' padding: 20px; border-radius: 16px; margin-bottom: 15px;'
css += ' transition: all 0.3s ease; text-align: left;'
css += '}'
css += '.neon-box:hover { transform: translateY(-3px); }'
css += '.box-title { font-size: 13px; font-weight: 800; letter-spacing: 1.5px; margin-bottom: 12px; }'
css += 'div[data-testid="stMetricLabel"] { display: none !important; }'
css += 'div[data-testid="stMetricValue"] { font-size: 32px !important; font-weight: 800 !important; color: #ffffff !important; }'
css += 'div[data-testid="stMetricDelta"] > div { background-color: rgba(16, 185, 129, 0.2) !important; color: #10b981 !important; padding: 4px 10px !important; border-radius: 6px !important; font-weight: 700 !important; font-size: 15px !important; }'
# Alt sekmelerin (Tabs) her birinin farklı renk çerçeve alması için CSS sınıfları
css += 'button[data-baseweb="tab"] {'
css += ' font-size: 16px !important; font-weight: 700 !important;'
css += ' color: #94a3b8 !important; padding: 12px 20px !important;'
css += ' background: #1e293b !important;'
css += ' border-radius: 10px !important; margin-right: 8px !important;'
css += ' transition: all 0.3s ease !important;'
css += '}'
css += 'button[data-baseweb="tab"]:nth-of-type(1) { border: 2px solid #ff007f !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(2) { border: 2px solid #00e5ff !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(3) { border: 2px solid #ffeb3b !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(4) { border: 2px solid #10b981 !important; }'
css += 'button[data-baseweb="tab"]:nth-of-type(5) { border: 2px solid #ff5722 !important; }'
css += 'button

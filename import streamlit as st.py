import streamlit as st
import pandas as pd
import plotly.express as px

# requirements: streamlit, pandas, plotly, openpyxl

st.set_page_config(page_title="Pano", layout="wide")

# Kırpılmayı önlemek amacıyla üç tırnak kaldırıldı ve güvenli kısa satırlarla birleştirildi
css = '<style>'
css += '.main-title { font-size: 40px !important; font-weight: 900 !important; background: linear-gradient(45deg, #ff007f, #ffeb3b, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 2px; text-shadow: 0 0 20px rgba(0, 229, 255, 0.3); }'
css += '.subtitle { font-size: 16px !important; color: #a1a1aa; margin-bottom: 30px; font-weight: 500; }'
css += '.section-title { font-size: 26px !important; font-weight: 800 !important; color: #00e5ff; margin-top: 35px; margin-bottom: 20px; border-left: 6px solid #ff007f; padding-left: 15px; text-shadow: 0 0 10px rgba(0, 229, 255, 0.2); }'
css += 'div[data-testid="column"] { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important; border: 2px solid #334155 !important; padding: 22px !important; border

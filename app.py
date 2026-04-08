import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="V4.0 全自動選股雷達", layout="wide")
st.title("🚀 V4.0 全自動黑馬雷達")

# 檢查檔案是否存在
if os.path.exists('result.json'):
    with open('result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    st.write("### 📅 今日法人認養清單 (由雲端機器人自動更新)")
    st.table(pd.DataFrame(data))
    st.info("💡 每日 16:30 自動更新，避開高位階倒貨風險。")
else:
    st.warning("⏳ 掃描機器人正在努力運算中，請稍後再試...")
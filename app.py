import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf
import plotly.graph_objects as go
import time

st.set_page_config(page_title="V4.6 終極黑馬雷達", layout="wide")
st.title("🚀 V4.6 自動選股 + 即時 K 線雷達")

# --- 1. 讀取機器人掃描結果 ---
if os.path.exists('result.json'):
    try:
        df_list = pd.read_json('result.json')
        st.write("### 📅 今日法人認養清單 (點選下方下拉選單查看 K 線)")
        
        # 讓表格變得可以點選
        options = df_list['代號'].astype(str) + " " + df_list['名稱']
        selected_stock = st.selectbox("請選擇要查看的股票：", options)
        
        # 顯示完整清單
        st.dataframe(df_list, use_container_width=True)
        
        # --- 2. 即時畫出 K 線與 MA20 (加上錯誤處理機制) ---
        if selected_stock:
            stock_id = str(selected_stock.split(" ")[0]) + ".TW"
            with st.spinner(f"正在連線 Yahoo 獲取 {selected_stock} 資料..."):
                try:
                    # 💡 技巧：稍微停個 0.5 秒，不要太暴力
                    time.sleep(0.5) 
                    ticker = yf.Ticker(stock_id)
                    df_k = ticker.history(period="6mo")
                    
                    if not df_k.empty:
                        df_k['MA20'] = df_k['Close'].rolling(window=20).mean()
                        fig = go.Figure(data=[
                            go.Candlestick(x=df_k.index, open=df_k['Open'], high=df_k['High'], low=df_k['Low'], close=df_k['Close'], name="K線"),
                            go.Scatter(x=df_k.index, y=df_k['MA20'], line=dict(color='orange', width=2), name="20日均線 (月線)")
                        ])
                        fig.update_layout(title=f"{selected_stock} 歷史走勢", xaxis_rangeslider_visible=False, height=500)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("⚠️ 該股票代號暫無 K 線資料（可能是新股或資料庫更新中）。")
                        
                except Exception as e:
                    if "RateLimit" in str(e):
                        st.error("🚫 【流量限制】Yahoo 股市暫時拒絕連線。請等 1 分鐘後再點選，或換一檔試試看。")
                    else:
                        st.error(f"❌ 發生預期外的錯誤：{e}")

    except Exception as e:
        st.error(f"讀取選股名單失敗：{e}")
else:
    st.warning("⏳ 掃描機器人正在努力運算中，請稍後再試...")

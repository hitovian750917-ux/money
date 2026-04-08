import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="V4.6 終極黑馬雷達", layout="wide")
st.title("🚀 V4.6 自動選股 + 即時 K 線雷達")

# --- 1. 讀取機器人掃描結果 ---
if os.path.exists('result.json'):
    with open('result.json', 'r', encoding='utf-8') as f:
        df_list = pd.read_json('result.json')
    
    st.write("### 📅 今日法人認養清單 (點選下方代號查看 K 線)")
    
    # 讓表格變得可以點選
    selected_stock = st.selectbox("請選擇要查看的股票：", df_list['代號'].astype(str) + " " + df_list['名稱'])
    
    # 顯示完整清單
    st.dataframe(df_list, use_container_width=True)
    
    # --- 2. 即時畫出 K 線與 MA20 ---
    if selected_stock:
        stock_id = selected_stock.split(" ")[0] + ".TW"
        with st.spinner(f"正在繪製 {selected_stock} 的技術線圖..."):
            # 抓取近 6 個月的資料
            df_k = yf.Ticker(stock_id).history(period="6mo")
            
            if not df_k.empty:
                # 計算 20 日均線 (MA20)
                df_k['MA20'] = df_k['Close'].rolling(window=20).mean()
                
                # 使用 Plotly 畫出專業 K 線圖
                fig = go.Figure(data=[
                    # K 線圖本體
                    go.Candlestick(
                        x=df_k.index,
                        open=df_k['Open'],
                        high=df_k['High'],
                        low=df_k['Low'],
                        close=df_k['Close'],
                        name="K線"
                    ),
                    # MA20 均線
                    go.Scatter(
                        x=df_k.index, 
                        y=df_k['MA20'], 
                        line=dict(color='orange', width=2), 
                        name="20日均線 (月線)"
                    )
                ])
                
                fig.update_layout(
                    title=f"{selected_stock} 歷史走勢 (含20日均線)",
                    yaxis_title="股價",
                    xaxis_rangeslider_visible=False,
                    template="plotly_white",
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("暫時抓不到 K 線資料，請稍後再試。")

else:
    st.warning("⏳ 掃描機器人正在努力運算中，請稍後再試...")

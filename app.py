import streamlit as st
import pandas as pd
import json
import os
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="V4.7 終極黑馬雷達", layout="wide")
st.title("🚀 V4.7 黑馬雷達 (證交所實戰版)")

if os.path.exists('result.json'):
    try:
        df_list = pd.read_json('result.json')
        
        # --- 表格顯示 ---
        st.write("### 📅 今日熱門成交精選 (資料來源：台灣證券交易所)")
        
        # 💡 關鍵修正：這裡的欄位名稱，完全對齊我們剛剛換上的證交所 JSON
        cols = ['代號', '名稱', '收盤價', '今日漲幅', '成交量', '狀態']
        st.dataframe(df_list[cols], use_container_width=True)
        
        # --- 下拉選單 ---
        options = df_list['代號'].astype(str) + " " + df_list['名稱']
        selected_stock = st.selectbox("🎯 點選查看 K 線與均線位階：", options, index=None, placeholder="請選擇股票...")
        
        if selected_stock:
            stock_id = str(selected_stock.split(" ")[0]) + ".TW"
            current_row = df_list[df_list['代號'].astype(str) == selected_stock.split(" ")[0]].iloc[0]
            
            c1, c2 = st.columns(2)
            # 顯示現價與漲跌
            c1.metric("當前股價", f"${current_row['收盤價']}", f"{current_row['今日漲幅']}")
            
            with st.spinner(f"正在繪製 {selected_stock} 的技術線圖..."):
                @st.cache_data(ttl=3600)
                def get_data(sid):
                    return yf.Ticker(sid).history(period="6mo")
                
                df_k = get_data(stock_id)
                if not df_k.empty:
                    df_k['MA20'] = df_k['Close'].rolling(window=20).mean()
                    fig = go.Figure(data=[
                        go.Candlestick(x=df_k.index, open=df_k['Open'], high=df_k['High'], low=df_k['Low'], close=df_k['Close'], name="K線"),
                        go.Scatter(x=df_k.index, y=df_k['MA20'], line=dict(color='orange', width=2), name="20日月線")
                    ])
                    fig.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"資料讀取錯誤：請確認 scanner.py 已經成功跑完最新版本。詳細錯誤：{e}")
else:
    st.warning("⏳ 機器人正在掃描 1700 檔股票，請稍後...")

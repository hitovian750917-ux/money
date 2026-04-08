import pandas as pd
import requests
import streamlit as st
import google.generativeai as genai

# 1. 這裡導入你的 API Key 
# 👇 替換成你剛剛複製的 Key，記得保留前後的雙引號 👇
genai.configure(api_key="AIzaSyBq57te_gMaMBJr7pZEFreF5QYOeB7ww5w") 

# 2. 定義 AI 幫你讀新聞的功能
def get_ai_summary(news_content):
    # 設定我們使用的 AI 模型
    model = genai.GenerativeModel('gemini-pro')
    
    # 給 AI 的指令 (Prompt)
    prompt = f"""
    你是一位專業的台股分析師。請針對以下新聞內容，精煉出 3 個影響股價的關鍵重點。
    請包含：1.營收與展望 2.獲利或毛利率 3.資本支出或重大計畫。
    請用繁體中文條列，語氣專業且簡短。
    
    新聞內容：
    {news_content}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI 罷工了，發生錯誤：{e}"

# 3. 網頁的外觀與按鈕設計
st.title("投資助理：AI 法說會重點摘要")

import yfinance as yf
import datetime

st.write("---")
st.write("### 📈 個股走勢 X 光機")
st.write("資料來源：Yahoo Finance (全球股市皆可查！)")

# 讓使用者輸入股票代號
stock_id = st.text_input("請輸入股票代號 (台股請加 .TW，例如 2330.TW，美股直接輸入例如 AAPL)", "2330.TW")

if st.button("📊 畫出近一個月走勢圖"):
    with st.spinner(f"正在前往 Yahoo 股市撈取 {stock_id} 的資料..."):
        try:
            # 設定抓取的時間範圍 (設定為近 30 天)
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=30)
            
            # 呼叫 yfinance 神器幫我們抓資料
            data = yf.download(stock_id, start=start_date, end=end_date)
            
            if data.empty:
                st.warning("找不到這檔股票的資料，請檢查代號是否輸入正確喔！")
            else:
                # 只取出「收盤價 (Close)」來畫圖，並把圖表漂亮地顯示出來
                st.line_chart(data['Close'])
                st.success(f"✅ 成功繪製 {stock_id} 近一個月的走勢圖！")
                
        except Exception as e:
            st.error(f"哎呀，撈取資料失敗了：{e}")
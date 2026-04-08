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

st.write("歡迎來到你的專屬 AI 投資網頁！請在下方貼上一段新聞內容，讓 AI 幫你畫重點。")

# 給你貼上新聞內容的框框
news_input = st.text_area("🗞️ 請在此貼上新聞內容：", height=200)

# 點擊按鈕後執行的動作
if st.button("✨ 開始 AI 摘要"):
    if news_input: # 如果框框裡有文字
        with st.spinner("AI 正在閱讀並整理重點，請稍候..."):
            # 呼叫 AI 幫忙
            result = get_ai_summary(news_input)
            
            # 顯示結果
            st.success("整理完成！")
            st.write("### 🤖 你的重點摘要：")
            st.info(result)
    else:
        st.warning("老闆，你要先貼上新聞內容啦！")
import pandas as pd
import requests

st.write("---") # 畫一條分隔線
st.write("### 📅 法說會搶先看雷達")
st.write("資料來源：公開資訊觀測站 (即將舉辦的法說會)")

# 只要按下按鈕，就去官方網站抓資料
if st.button("📡 啟動雷達，抓取最新行事曆"):
    with st.spinner("正在潛入公開資訊觀測站抓取資料..."):
        try:
            # 公開資訊觀測站的隱藏 API 網址
            url = "https://mops.twse.com.tw/mops/web/ajax_t100sb07_1"
            
            # 給伺服器的通關密語 (設定抓取最新的資料)
            payload = {
                "encodeURIComponent": "1",
                "step": "1",
                "firstin": "1",
                "off": "1",
                "TYPEK": "all",
                "isnew": "true" 
            }
            
            # 發送請求
            res = requests.post(url, data=payload)
            res.encoding = 'utf8' # 確保中文不會變成亂碼
            
            # 🔮 魔法發生在這裡：直接把網頁裡的 HTML 轉換成表格
            dfs = pd.read_html(res.text)
            
            # 取出第一個表格
            df = dfs[0]
            
            # 我們只挑選我們在乎的欄位
            df = df[['公司代號', '公司名稱', '法說會日期', '法說會時間', '法說會地點']]
            
            # 把表格漂亮地顯示在 Streamlit 網頁上
            st.dataframe(df, use_container_width=True)
            st.success("抓取成功！快看看有沒有你關注的股票！")
            
        except Exception as e:
            st.error(f"哎呀，雷達訊號中斷了：{e}")
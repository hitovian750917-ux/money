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

# 只要按下按鈕，就去官方網站抓資料
# 只要按下按鈕，就去官方網站抓資料
if st.button("📡 啟動雷達，抓取最新行事曆"):
    with st.spinner("正在透過工程師 VIP 通道抓取資料..."):
        try:
            # 台灣證交所 Open API
            url = "https://openapi.twse.com.tw/v1/company/investorConference"
            
            # 戴上人類瀏覽器的面具，以免被當成粗魯的機器人
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
            
            # 發送請求 (戴上面具 + 免除憑證檢查的通關密語)
            res = requests.get(url, headers=headers, verify=False)
            
            # 把拿到的 JSON 資料轉換成表格
            import pandas as pd
            df = pd.DataFrame(res.json())
            
            # 挑選我們在乎的欄位，並把英文標題換成中文
            df = df[['Code', 'Name', 'Date', 'Time', 'Location']]
            df.columns = ['公司代號', '公司名稱', '法說會日期', '法說會時間', '法說會地點']
            
            # 把表格漂亮地顯示在網頁上
            st.dataframe(df, use_container_width=True)
            st.success("✅ 突破封鎖！成功取得最新法說會日程！")
            
        except Exception as e:
            st.error(f"哎呀，雷達訊號中斷了：{e}")
            # 如果還是失敗，我們把警衛塞給我們的紙條內容印出來看看
            if 'res' in locals():
                st.info(f"保鑣塞給我們的紙條內容：{res.text[:200]}")
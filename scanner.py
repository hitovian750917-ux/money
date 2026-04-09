import pandas as pd
import requests
import json

def run_scan():
    print("📡 正在連線【台灣證券交易所】官方資料庫抓取真實行情...")
    
    # 💡 證交所官方的每日收盤行情 API (免費、免 Key、超穩定)
    url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # 轉成 DataFrame 方便篩選
        df = pd.DataFrame(data)
        
        # 整理資料：把字串轉成數字
        df['TradeVolume'] = pd.to_numeric(df['TradeVolume'], errors='coerce')
        df['ClosingPrice'] = pd.to_numeric(df['ClosingPrice'], errors='coerce')
        
        # 排除資料有缺的股票
        df = df.dropna(subset=['TradeVolume', 'ClosingPrice'])
        
        # --- 真實過濾邏輯 ---
        # 1. 成交量 > 5000 張 (代表市場熱門、有人氣)
        # 2. 股價 > 10 元 (避開全額交割或雞蛋股)
        mask = (df['TradeVolume'] > 5000) & (df['ClosingPrice'] > 10)
        
        # 取成交量最大的前 30 檔熱門股
        filtered = df[mask].sort_values(by='TradeVolume', ascending=False).head(30)
        
        result_list = []
        for _, row in filtered.iterrows():
            result_list.append({
                "代號": str(row['Code']),
                "名稱": str(row['Name']),        # 這裡絕對是真正的台股中文名
                "收盤價": float(row['ClosingPrice']),
                "今日漲幅": row['Change'],       # 證交所提供的是漲跌金額 (例如 +2.5 或 -1.0)
                "狀態": "熱門成交股",
                "成交量": int(row['TradeVolume'])
            })
            
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
            
        print(f"✅ 證交所資料抓取成功！已存入 {len(result_list)} 檔真實台股！")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    run_scan()

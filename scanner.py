import pandas as pd
import requests
import json
import os

def run_scan():
    api_key = os.environ.get('FUGLE_API_KEY')
    print("📡 啟動真．台股掃描器...")
    
    # 抓取上市股票快照 (這才是真貨！)
    url = "https://api.fugle.tw/marketdata/v1.0/stock/snapshot/market/TSE"
    headers = {"X-API-KEY": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'data' not in data:
            print("❌ 抓取失敗，請檢查 API Key 是否正確")
            return

        stocks = data['data']
        df = pd.DataFrame(stocks)
        
        # 換算漲跌幅
        df['漲跌幅'] = (df['changePercent'] * 100).round(2)
        
        # --- 實戰過濾邏輯 ---
        # 1. 有漲但沒漲停 (0.5% ~ 8%)
        # 2. 有人在玩 (成交量 > 3000 張)
        # 3. 股價大於 10 元 (避開全額交割或雞蛋股)
        mask = (df['漲跌幅'] > 0.5) & (df['漲跌幅'] < 8) & (df['tradeVolume'] > 3000) & (df['lastPrice'] > 10)
        filtered = df[mask].sort_values(by='tradeVolume', ascending=False).head(30)
        
        result_list = []
        for _, row in filtered.iterrows():
            result_list.append({
                "代號": row['symbol'],
                "名稱": row['name'], # 這裡會顯示真正的「鴻海」、「瑞軒」
                "收盤價": row['lastPrice'],
                "今日漲幅": row['漲跌幅'],
                "外資買超": "授權確認中", # 基本用戶權限可能看不了籌碼，先抓價格
                "成交量": int(row['tradeVolume'])
            })
            
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
        print(f"✅ 實戰掃描完成！找到 {len(result_list)} 檔真實台股黑馬！")

    except Exception as e:
        print(f"❌ 錯誤：{e}")

if __name__ == "__main__":
    run_scan()

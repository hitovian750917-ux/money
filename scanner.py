import pandas as pd
import requests
import json
import os

def run_scan():
    # 1. 檢查鑰匙
    api_key = os.environ.get('FUGLE_API_KEY')
    if not api_key or api_key == "YOUR_FUGLE_API_KEY":
        print("❌ 錯誤：找不到 API Key，請檢查 GitHub Secrets 設定。")
        return

    print("📡 正在連線富果 API 抓取『純台股』真實行情...")
    
    # 2. 抓取上市 (TSE) 股票快照
    url = "https://api.fugle.tw/marketdata/v1.0/stock/snapshot/market/TSE"
    headers = {"X-API-KEY": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'data' not in data:
            print(f"❌ API 回傳異常：{data.get('message', '未知錯誤')}")
            return

        stocks = data['data']
        df = pd.DataFrame(stocks)
        
        # 3. 過濾邏輯 (確保抓出來的是真貨)
        df['漲跌幅'] = (df['changePercent'] * 100).round(2)
        
        # 篩選：成交量 > 2000 張 且 漲幅在 1% ~ 8% 之間
        mask = (df['tradeVolume'] > 2000) & (df['漲跌幅'] > 1.0) & (df['漲跌幅'] < 8.0)
        filtered = df[mask].sort_values(by='tradeVolume', ascending=False).head(30)
        
        result_list = []
        for _, row in filtered.iterrows():
            result_list.append({
                "代號": str(row['symbol']),
                "名稱": row['name'],       # 這才是真正的「鴻海」、「茂聯」
                "收盤價": row['lastPrice'],
                "今日漲幅": row['漲跌幅'],
                "成交量": int(row['tradeVolume']),
                "狀態": "真實行情"
            })
            
        # 4. 覆蓋舊的 JSON
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
        print(f"✅ 實戰更新成功！已存入 {len(result_list)} 檔真實台股資料。")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    run_scan()

import pandas as pd
import requests
import json
import os

def run_scan():
    api_key = os.environ.get('FUGLE_API_KEY')
    print("📡 執行『純台股』籌碼過濾器...")
    
    # 💡 鎖定 TSE (上市) 與 OTC (上櫃)
    urls = [
        "https://api.fugle.tw/marketdata/v1.0/stock/snapshot/market/TSE",
        "https://api.fugle.tw/marketdata/v1.0/stock/snapshot/market/OTC"
    ]
    headers = {"X-API-KEY": api_key}
    
    all_stocks = []
    
    try:
        for url in urls:
            response = requests.get(url, headers=headers)
            data = response.json()
            if 'data' in data:
                all_stocks.extend(data['data'])
        
        df = pd.DataFrame(all_stocks)
        
        # 換算漲跌幅
        df['漲跌幅'] = (df['changePercent'] * 100).round(2)
        
        # --- 篩選條件：避開殭屍股、避開追高 ---
        mask = (df['漲跌幅'] > 1.0) & (df['漲跌幅'] < 8.0) & (df['tradeVolume'] > 3000)
        filtered = df[mask].sort_values(by='tradeVolume', ascending=False).head(30)
        
        result_list = []
        for _, row in filtered.iterrows():
            result_list.append({
                "代號": str(row['symbol']),
                "名稱": row['name'],  # 這邊抓出來一定是中文
                "收盤價": row['lastPrice'],
                "今日漲幅": row['漲跌幅'],
                "狀態": "籌碼強勁",
                "成交量": int(row['tradeVolume'])
            })
            
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result_list, f, ensure_ascii=False, indent=4)
        print(f"✅ 掃描完畢！已抓取 {len(result_list)} 檔純台股資料。")

    except Exception as e:
        print(f"❌ 錯誤：{e}")

if __name__ == "__main__":
    run_scan()

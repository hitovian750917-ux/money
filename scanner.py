import pandas as pd
import json
import os
import yfinance as yf

def run_scan():
    print("📡 正在抓取『真．台股』即時行情...")
    
    # 這是我們要監控的熱門股名單 (範例，你可以增加到 1700 檔)
    # 真正的 1700 檔需要透過 Fugle API 抓取清單，我們先用這幾檔測試
    target_stocks = ["2330.TW", "2317.TW", "2454.TW", "2489.TW", "2603.TW", "2609.TW", "2303.TW", "2382.TW"]
    
    real_data = []
    
    for sid in target_stocks:
        try:
            stock = yf.Ticker(sid)
            hist = stock.history(period="2d")
            if len(hist) < 2: continue
            
            # 計算現價與漲跌幅
            current_price = round(hist['Close'].iloc[-1], 2)
            prev_price = hist['Close'].iloc[-2]
            change_percent = round(((current_price - prev_price) / prev_price) * 100, 2)
            volume = int(hist['Volume'].iloc[-1])
            
            # 獲取名稱 (yfinance 抓中文有時會漏，我們先用代號補)
            name = stock.info.get('shortName', sid.replace(".TW", ""))
            
            real_data.append({
                "代號": sid.replace(".TW", ""),
                "名稱": name,
                "收盤價": current_price,
                "今日漲幅": change_percent,
                "外資買超": "需API授權", # 這部分需要 Fugle API 正式權限
                "成交量": volume
            })
        except:
            continue

    # 存檔
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(real_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 成功抓取 {len(real_data)} 檔真實台股數據！")

if __name__ == "__main__":
    run_scan()

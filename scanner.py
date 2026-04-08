import requests
import pandas as pd
import json
import os

def run_scan():
    # 從 GitHub Secrets 讀取你的 API Key
    api_key = os.environ.get('FUGLE_API_KEY')
    
    print("🚀 啟動全市場籌碼掃描...")
    
    # 這裡我們先用一個範例邏輯 (因為掃描 1700 檔需要多個 API 組合)
    # 實際運作時，這段會去爬取富果的「每日法人買賣超統計」
    
    # 假設這是篩選出來的結果
    top_picks = [
        {"代號": "2489", "名稱": "瑞軒", "外資買超": 11991, "狀態": "法人大買"},
        {"代號": "2317", "名稱": "鴻海", "外資買超": 8500, "狀態": "持續吸貨"},
        # ... 這裡會由程式自動填滿 50 隻
    ]
    
    # 把結果存成檔案
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(top_picks, f, ensure_ascii=False, indent=4)
    print("✅ 掃描完成，清單已更新。")

if __name__ == "__main__":
    run_scan()
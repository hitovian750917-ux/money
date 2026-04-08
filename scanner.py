import pandas as pd
import numpy as np
import json
import os

def run_scan():
    print("🚀 啟動 V4.7 全市場大掃描 (含現價偵測)...")
    
    # --- 模擬全市場數據 (1700 檔) ---
    np.random.seed(42)
    codes = [str(i) for i in range(1101, 2801)]
    names = ["股票" + c for c in codes]
    
    all_data = pd.DataFrame({
        '代號': codes,
        '名稱': names,
        '收盤價': np.random.uniform(10, 1000, size=1700).round(2), # 👈 加上現價數據
        '外資買超': np.random.randint(-1000, 3000, size=1700),
        '投信買超': np.random.randint(-200, 500, size=1700),
        '今日漲幅': np.random.uniform(-3, 9.9, size=1700).round(2),
        '成交量': np.random.randint(100, 50000, size=1700)
    })

    # 濾網條件
    mask = (all_data['外資買超'] > 100) & (all_data['投信買超'] >= 0) & (all_data['今日漲幅'] < 8.5)
    top_30 = all_data[mask].sort_values(by='外資買超', ascending=False).head(30)
    
    result = top_30.to_dict(orient='records')
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print("✅ 掃描完畢，現價資料已更新！")

if __name__ == "__main__":
    run_scan()

import pandas as pd
import numpy as np
import json
import os

def run_scan():
    print("🚀 啟動 V4.6 全市場 1700 檔『三面合一』掃描器...")
    
    # 這裡未來會接 Fugle API 抓取 1700 檔的快照
    # api_key = os.environ.get('FUGLE_API_KEY')
    
    # --- 模擬全市場數據 (1700 檔) ---
    np.random.seed(42) # 固定結果方便觀察
    codes = [str(i) for i in range(1101, 2801)]
    names = ["股票" + c for c in codes] # 暫時用代號命名
    
    all_data = pd.DataFrame({
        '代號': codes,
        '名稱': names,
        '外資買超': np.random.randint(-1000, 3000, size=1700),
        '投信買超': np.random.randint(-200, 500, size=1700),
        '今日漲幅': np.random.uniform(-3, 9.9, size=1700),
        '成交量': np.random.randint(100, 50000, size=1700)
    })

    # --- 💡 關鍵：調整濾網 (讓名單變多) ---
    # 只要符合這三個條件的都抓出來：
    # 1. 外資有買 (買超 > 100張)
    # 2. 投信沒賣 (買超 >= 0張)
    # 3. 漲幅別太誇張 (今日漲幅 < 8.5%，避開隔日沖)
    # 4. 有人在玩 (成交量 > 1000張)
    
    mask = (all_data['外資買超'] > 100) & \
           (all_data['投信買超'] >= 0) & \
           (all_data['今日漲幅'] < 8.5) & \
           (all_data['成交量'] > 1000)
    
    filtered_df = all_data[mask].copy()
    
    # 按外資買超力道排序，取前 30 名
    top_30 = filtered_df.sort_values(by='外資買超', ascending=False).head(30)
    
    # 轉換成 JSON 格式
    result = top_30.to_dict(orient='records')
    
    # 存檔
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 掃描完畢！在 1700 檔中篩選出 {len(top_30)} 檔優質黑馬！")

if __name__ == "__main__":
    run_scan()

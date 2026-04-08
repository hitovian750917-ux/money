# 💡 調整後的濾網邏輯：
# 1. 外資買超 > 200 張 (不用到 500 這麼多，讓中小型績優股進來)
# 2. 漲幅放寬到 < 9% (只要還沒漲停都算)
# 3. 投信買超只要 > 0 就及格 (只要有認養跡象就抓)

filtered = all_data[
    (all_data['foreign_buy'] > 200) & 
    (all_data['growth'] < 9) & 
    (all_data['trust_buy'] >= 0)
]

# 這次我們取前 30 名
result = filtered.head(30).to_dict(orient='records')

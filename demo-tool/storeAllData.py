import requests
import json


response = requests.get("https://www.cninfo.com.cn/new/data/szse_stock.json")
with open("szse_stock.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, ensure_ascii=False)


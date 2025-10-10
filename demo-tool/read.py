import json


def read_stock_data(query: str) -> str:
    with open("szse_stock.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # 在数据中搜索zwjc字段等于query的项目
    found_items = []

    for item in data.get("stockList"):
        if item.get("zwjc") == query:
            found_items.append(item)
            break
    print(found_items)
    print(found_items[0])
    print(found_items[0].get("code"))
    print(f"公司的股票代码为{found_items[0].get('code')}")
    return f"公司的股票代码为{found_items[0].get('code')}"


read_stock_data("金发科技")
import requests


def get_balance_sheet(stock_code: str) -> dict:
    url = f"http://webapi.cninfo.com.cn/api/stock/p_stock2300"
    params = {
        "scode": stock_code,
    }
    response = requests.post(url, data=params)
    return response.json()
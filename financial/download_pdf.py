import requests


cookie_string = "gdp_user_id=gioenc-c928289g%2C91db%2C5gea%2Ca297%2C46cga34e8dc1; ba17301551dcbaf9_gdp_session_id=5dc308e0-857c-4db8-92bc-c8f1cc7c167c; ba17301551dcbaf9_gdp_session_id_sent=5dc308e0-857c-4db8-92bc-c8f1cc7c167c; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:90%2C%22VISIT%22:6%2C%22PAGE%22:12%2C%22VIEW_CLICK%22:56%2C%22CUSTOM%22:14%2C%22VIEW_CHANGE%22:6}; acw_tc=df6d3fab17616578018691111e356b958d23906e2a97ac689840462b96; cdn_sec_tc=df6d3fab17616578018691111e356b958d23906e2a97ac689840462b96; acw_sc__v2=6900c3c97841398cb5ecfa8b519600d097d0e83c"

# 将字符串拆分成键值对
parsed_cookies = {}
for cookie_pair in cookie_string.split(';'):
    if '=' in cookie_pair:
        name, value = cookie_pair.strip().split('=', 1)
        parsed_cookies[name] = value

# 1. 定义请求头
custom_headers = {
    # 模拟浏览器访问，很多网站会检查这个头
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
    # 模拟认证，例如使用 Bearer Token
    'Authorization': 'Bearer your_secret_token_here',
    
    # 你可以添加其他任何需要的头，比如接受的语言等
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
def download_pdf(url, filename):
    """
    从指定 URL 下载 PDF 文件并保存为本地文件。
    
    参数:
    url (str): PDF 文件的网络地址
    filename (str): 保存到本地的文件名（例如 'document.pdf'）
    """
    try:
        # 发送 GET 请求
        response = requests.get(url, headers=custom_headers, cookies=parsed_cookies)
        
        # 检查请求是否成功
        response.raise_for_status()
        
        print(response.content)
        # 以二进制写模式打开文件
        with open(f"./pdf/{filename}", 'wb') as file:
            # 分块写入，避免大文件占用过多内存
            # for chunk in response.iter_content(chunk_size=8192):
            file.write(response.content)
        
        print(f"PDF 文件已成功下载并保存为: {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")

# 使用示例
# pdf_url = "https://example.com/path/to/document.pdf"  # 替换为实际的 PDF 链接
# save_filename = "downloaded_document.pdf"             # 本地保存的文件名

# download_pdf('https://static.sse.com.cn/disclosure/listedinfo/announcement/c/new/2025-10-29/600281_20251029_4ZJS.pdf', 'info.pdf')

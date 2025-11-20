from crawler_website.run_browser import run_browser
from download_pdf.auth_download import auth_download
from ai.analyse_pdf import analyse_pdf
from db.save_campany_info import save_campany_info
from db.search_SQL import search_SQL
from datetime import datetime


def main(exchange_code, stock_code, fiscal_year, period_type):
    # 1. 股票信息 exchange_code, stock_code, fiscal_year, period_type
    fiscal_year = datetime.now().year
    period_type = (datetime.now().month - 1) // 3 + 1
    # 2. 从数据库中查看是否有内容  返回  fileUrl
    fileUrl = search_SQL()
    # 2.1 如果没有内容 需要打开浏览器去爬取对应内容
    if not fileUrl:
        file = run_browser(exchange_code, stock_code, fiscal_year, period_type)
        save_campany_info(file['url'], exchange_code, stock_code, fiscal_year, period_type)
    # 3. 前端下载内容 blob
    auth_download(file['url'], file['name'])

    # 4. 把 blob 给ai 去分析
    analyse_pdf(f'../pdf/{file['name']}')


if __name__ == "__main__":
    main()
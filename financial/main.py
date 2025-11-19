

def main():
    # 1. 股票信息 exchange_code, stock_code, fiscal_year, period_type

    # 2. 从数据库中查看是否有内容  返回  fileUrl
    fileUrl = search_SQL()
    # 2.1 如果没有内容 需要打开浏览器去爬取对应内容
    if not fileUrl:
        fileUrl = get_company_pdf(exchange_code, stock_code, fiscal_year, period_type)
        save_campany_info(fileUrl)
    # 3. 前端下载内容 blob
    filepath = download_pdf(fileUrl)

    # 4. 把 blob 给ai 去分析
    analyse_pdf(filepath)



if __name__ == "__main__":
    main()
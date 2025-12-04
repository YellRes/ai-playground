from typing import Any, Generator


from crawler_website.run_browser import run_browser
from download_pdf.auth_download import auth_download
from ai.analyse_pdf import analyse_pdf
from ai.index import main_with_pdf
from db.save_company_info import save_company_info
from db.search_SQL import search_SQL
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main(exchange_code, stock_code, fiscal_year, company_name = '', period_type = 3) -> Generator:
    """
    主函数 - 返回生成器用于流式处理
    """
    try:
        # 1. 股票信息
        logging.info(f"开始处理: exchange_code={exchange_code}, stock_code={stock_code}, fiscal_year={fiscal_year}")
        yield {
            "status": "progress",
            "step": "init",
            "message": f"开始处理: {exchange_code}-{stock_code}"
        }
        
        fiscal_year = datetime.now().year
        period_type = (datetime.now().month - 1) // 3 + 1
        logging.info(f"当前财年: {fiscal_year}, 季度: {period_type}")
        
        # 2. 查询数据库
        logging.info("正在查询数据库...")
        yield {
            "status": "progress",
            "step": "search_db",
            "message": "正在查询数据库..."
        }
        
        file = search_SQL(exchange_code, stock_code, fiscal_year, period_type)
        logging.info(f'file: {file}')
        
        # 2.1 如果没有内容，爬取数据
        if not file:
            logging.info("数据库中无内容，启动浏览器爬取...")
            yield {
                "status": "progress",
                "step": "crawl",
                "message": "数据库中无内容，启动浏览器爬取..."
            }
            
            file = run_browser(exchange_code, stock_code, fiscal_year, period_type)
            logging.info(f"爬取完成，保存数据: {file}")
            
            yield {
                "status": "progress",
                "step": "save",
                "message": "保存爬取数据到数据库..."
            }
            
            save_company_info(file[0]['file_url'], exchange_code, stock_code, fiscal_year, period_type, file[0]['company_name'])
        else:
            logging.info(f"从数据库获取文件: {file}")
            yield {
                "status": "progress",
                "step": "search_db_success",
                "message": f"从数据库获取文件: {file[0]['company_name']}"
            }
        
        # 3. 下载文件
        logging.info(f"开始下载文件: {file[0]['company_name']}")
        yield {
            "status": "progress",
            "step": "download",
            "message": f"开始下载文件: {file[0]['company_name']}"
        }
        
        auth_download(file[0]['file_url'], file[0]['company_name'])
        logging.info("文件下载完成")
        
        yield {
            "status": "progress",
            "step": "download_complete",
            "message": "文件下载完成"
        }

        # 4. AI分析
        logging.info(f"开始分析PDF: {file[0]['company_name']}")
        yield {
            "status": "progress",
            "step": "analyze",
            "message": f"开始分析PDF: {file[0]['company_name']}"
        }
        
        pdf_path = f'../pdf/{file[0]["company_name"]}.pdf'
        
        # 使用 main_with_pdf 进行流式分析
        for analysis_chunk in main_with_pdf(pdf_path):
            yield {
                "status": "progress",
                "step": "analysis",
                "data": analysis_chunk
            }
        
        logging.info("PDF分析完成")
        yield {
            "status": "complete",
            "message": "财务报表分析完成",
            "data": {
                "company_name": file[0]['company_name'],
                "exchange_code": exchange_code,
                "stock_code": stock_code,
                "fiscal_year": fiscal_year
            }
        }
        
    except Exception as e:
        logging.error(f"执行出错: {str(e)}", exc_info=True)
        yield {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info("开始执行财务报表分析系统")
    logging.info("=" * 50)
    try:
        main('SH', '601127', 2025)
        logging.info("=" * 50)
        logging.info("执行完成")
        logging.info("=" * 50)
    except Exception as e:
        logging.error(f"执行出错: {str(e)}", exc_info=True)
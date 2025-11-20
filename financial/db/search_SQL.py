from index import supabase
def search_SQL(exchange_code, stock_code, fiscal_year, period_type):
    query = supabase.table('company_info').select('*').eq('exchange_code', exchange_code).eq('stock_code', stock_code).eq('fiscal_year', fiscal_year).eq('period_type', period_type)
    response = query.execute()
    return response.data

# if __name__ == "__main__":
    # search_SQL('SH', '600000', 2023, 1)
import tushare as ts

pro = ts.pro_api()

stock_list_L = pro.stock_basic(list_status='L',
                               fields='ts_code, symbol, name, area, '
                                      'industry, fullname, enname, '
                                      'cnspell, market, exchange, '
                                      'curr_type, list_status, '
                                      'list_date, delist_date, is_hs')

#print(type(stock_list_L))

stock_list_D = pro.stock_basic(list_status='D',
                               fields='ts_code, symbol, name, area, '
                                      'industry, fullname, enname, '
                                      'cnspell, market, exchange, '
                                      'curr_type, list_status, '
                                      'list_date, delist_date, is_hs')
stock_list_P = pro.stock_basic(list_status='P',
                               fields='ts_code, symbol, name, area, '
                                      'industry, fullname, enname, '
                                      'cnspell, market, exchange, '
                                      'curr_type, list_status, '
                                      'list_date, delist_date, is_hs')

stock_list_L.to_csv('stock_list_L.csv')
stock_list_D.to_csv('stock_list_D.csv')
stock_list_P.to_csv('stock_list_P.csv')
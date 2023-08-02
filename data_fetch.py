import tushare as ts
#import pandas as pd
import os
import time

cwd_path = os.getcwd()
data_path = cwd_path+"/Data/"

'''
stock_list_L = pd.read_csv(data_path+"stock_list_L.csv")
stock_list_D = pd.read_csv(data_path+"stock_list_D.csv")
stock_list_P = pd.read_csv(data_path+"stock_list_P.csv")

ts_code_L = list(stock_list_L.ts_code)
ts_code_D = list(stock_list_D.ts_code)
ts_code_P = list(stock_list_P.ts_code)
ts_code_full = ts_code_L + ts_code_D + ts_code_P
'''
s_date = '19990101'
e_date = '20161231'
#获取区间交易日历
pro=ts.pro_api()
trade_calendar = pro.trade_cal(exchange='', start_date=s_date, end_date=e_date)
trade_calendar.to_csv(data_path+'trade_cal.csv')
#print(trade_calendar)
tr_cal = list(trade_calendar.loc[date].cal_date for date in trade_calendar.index if trade_calendar.loc[date].is_open==1)
#print(tr_cal[-1])
#print(len(tr_cal))

#获取行情数据，注意每分钟只能请求200次
i=0
for date in tr_cal:
    if os.path.exists(data_path+date+'.csv'):
        continue
    bar = pro.daily(trade_date=date)
    bar.to_csv(data_path+date+'.csv')
    i += 1
    print(i)
    print(date)
    if i>=200:
        time.sleep(60)
        i = 0


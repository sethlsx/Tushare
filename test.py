import time

import pandas as pd
import os
import tushare as ts

pro = ts.pro_api()
cwd_path = os.getcwd()
data_path = cwd_path+"/Data/"

trade_calendar = pd.read_csv(data_path+'trade_cal_processed.csv')
tr_cal = list(str(trade_calendar.loc[date].cal_date) for date in trade_calendar.index if trade_calendar.loc[date].is_open==1)
first_day_in_year = list(str(trade_calendar.loc[row].cal_date) for row in trade_calendar.index if trade_calendar.loc[row].first_day_in_year == 1)
#print(first_day_in_year)
#print(type(first_day_in_year[0]))
first_day_in_year.reverse()
i = 0
day = '20060925'
mkt_value = pro.daily_basic(ts_code='', trade_date=day, fields='ts_code, total_mv, total_share, close')
print(mkt_value.loc[mkt_value['ts_code']=='600018.SH'])
print('600018.SH' in mkt_value['ts_code'])
print('000949.SZ' in list(mkt_value['ts_code']))
#mkt_value.to_csv(data_path+day+'_test.csv')
'''
for day in tr_cal:
    
    if os.path.exists(data_path+day+'_processed.csv'):
        continue
    bar = pd.read_csv(data_path+day+'.csv')
    #print(bar)
    
    i += 1
    print(i)
    print(day)
    print('Inquiry successful!')
    if i >= 200:
        i = 0

        print("Too many inquiries, hold for 1 minute...")
        time.sleep(60)
        #print(mkt_value)
    bar['mkt_value'] = 0

    for row in bar.index:
        stock = bar.loc[row].ts_code
        print(stock)
        print(mkt_value.loc[mkt_value['ts_code'] == stock, 'total_mv'])
        bar.loc[row, 'mkt_value'] = mkt_value.loc[mkt_value['ts_code']==stock,'total_mv'].values[0]
            #print(bar.head())
    bar.to_csv(data_path+day+'_processed.csv')
    print(day)
    print('Csv saved!')

'''

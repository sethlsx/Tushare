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

for day in tr_cal:
    if os.path.exists(data_path+day+'_processed.csv'):
        continue
    bar = pd.read_csv(data_path+day+'.csv')
    #print(bar)
    mkt_value = pro.daily_basic(ts_code='', trade_date=day, fields='ts_code, total_mv')
    i += 1
    print(i)
    print(day)
    print('Inquiry successful!')
    if i >= 200:
        i = 0

        print("Too many inquiries, hold for 1 minute...")
        time.sleep(60)
        #print(mkt_value)
    bar['mkt_value'] = pd.Series()


    for row in bar.index:
        stock = bar.loc[row].ts_code
        #print(stock)
        #print(mkt_value.loc[mkt_value['ts_code'] == stock, 'total_mv'])
        if stock in list(mkt_value['ts_code']): #对于接过壳的股票，会出现借壳前的同代码股票有交易记录数据却没有市值数据的情况，为避免出错增加判断语句
            bar.loc[row, 'mkt_value'] = mkt_value.loc[mkt_value['ts_code']==stock,'total_mv'].values[0]
            #print(bar.head())
    bar.to_csv(data_path+day+'_processed.csv')
    print(day)
    print('Csv saved!')



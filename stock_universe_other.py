import time
import pandas as pd
import os
import tushare as ts
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm

pro = ts.pro_api()
cwd_path = os.getcwd()
data_path = cwd_path + "/Data/"

stock_list_L = pd.read_csv(data_path + "stock_list_L.csv")
stock_list_D = pd.read_csv(data_path + "stock_list_D.csv")
stock_list_P = pd.read_csv(data_path + "stock_list_P.csv")
stock_list_full = pd.concat([stock_list_P, stock_list_D, stock_list_L])
stock_list_full = stock_list_full.drop(columns='Unnamed: 0')

'''
ts_code_L = list(stock_list_L.ts_code)
ts_code_D = list(stock_list_D.ts_code)
ts_code_P = list(stock_list_P.ts_code)
ts_code_full = ts_code_L + ts_code_D + ts_code_P
'''

trade_calendar = pd.read_csv(data_path + 'trade_cal_processed.csv')
tr_cal = list(
    str(trade_calendar.loc[date].cal_date) for date in trade_calendar.index if trade_calendar.loc[date].is_open == 1)
# print(tr_cal)
s_date = '19990101'
e_date = '20161231'
record_calendar = pro.trade_cal(exchange='', start_date=s_date, end_date=e_date)
r_cal = list(
    str(record_calendar.loc[date].cal_date) for date in record_calendar.index if record_calendar.loc[date].is_open == 1)
trading_records = dict()
print('Start loading records...')
for r_date in tqdm(r_cal):
    records = pd.read_csv(data_path + r_date + '.csv')
    trading_records[r_date] = records
print('Records loaded.')
# print(trading_records)
time.sleep(1)
effective_cal = list(date for date in tr_cal if not os.path.exists(data_path + date + '_final.csv'))
p_bar = tqdm(effective_cal)
#为了避免重复请求数据，提高效率，增加一些缓存变量，当判断与上个交易日的前一个交易年或者前一个交易月底是同一年或者同一月的情况，不再重复请求数据，而是直接调用缓存的数据，大幅减少运行时间
last_previous_year = 0
last_previous_month = 0
last_records_year = dict()
last_records_month = dict()
i = 0 #用于计数，避免超出单分钟请求次数
for day in p_bar:
    '''
    if os.path.exists(data_path+day+'_final.csv'):
        continue
    '''
    p_bar.set_description(day)
    bar = pd.read_csv(data_path + day + '_processed.csv')
    bar['list_day'] = pd.Series(str)
    bar['Month_from_list'] = pd.Series(int)
    bar['records_last_month'] = pd.Series(int)
    bar['records_last_year'] = pd.Series(int)
    current_date = datetime.strptime(day, '%Y%m%d')
    # print(current_date)
    previous_year = current_date.year - 1
    # print(previous_year)
    # print(type(previous_year))
    # print(previous_year)
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    # print(previous_year)
    # print(previous_month.strftime("%Y%m"))
    # stock_for_the_day = list(bar.loc[s].ts_code for s in bar.index)
    # last_stock_y = list(last_records_year.keys())
    # last_stock_m = list(last_records_month.keys())
    # stock_year_diff = len(set(stock_for_the_day).difference(set(last_stock_y)))
    # stock_month_diff = len(set(stock_for_the_day).difference(set(last_stock_m)))
    previous_year_s_date = str(previous_year) + '0101'
    previous_year_e_date = str(previous_year) + '1231'
    previous_year_cal = pro.trade_cal(exchange='', start_date=previous_year_s_date,
                                      end_date=previous_year_e_date)
    i += 1
    if i >= 290:
        time.sleep(60)
        i = 0
    p_y_cal = list(str(previous_year_cal.loc[date].cal_date) for date in previous_year_cal.index if
                   previous_year_cal.loc[date].is_open == 1)
    previous_month_s_date = previous_month.strftime("%Y%m") + '01'
    previous_month_e_date = previous_month.strftime("%Y%m%d")
    previous_month_cal = pro.trade_cal(exchange='', start_date=previous_month_s_date,
                                       end_date=previous_month_e_date)
    i += 1
    if i >= 290:
        time.sleep(60)
        i = 0
    p_m_cal = list(str(previous_month_cal.loc[date].cal_date) for date in previous_month_cal.index if
                   previous_month_cal.loc[date].is_open == 1)
    for row in bar.index:
        stock = bar.loc[row].ts_code
        if stock in list(stock_list_full['ts_code']):   #先标记上市了多少个月
            bar.loc[row, 'list_day'] = str(
                stock_list_full.loc[stock_list_full['ts_code'] == stock, 'list_date'].values[0])
            list_day = datetime.strptime(bar.loc[row, 'list_day'], '%Y%m%d')
            diff_month = (current_date.year - list_day.year) * 12 + current_date.month - list_day.month
            bar.loc[row, 'Month_from_list'] = diff_month
        if previous_year == last_previous_year: #如果与上个交易日是同一年，直接调用之前的数据，不用再循环统计一次
            if stock in last_records_year: #这个判断很重要，因为有的股票上个交易日可能还没上市或没交易，不判断会出错
                bar.loc[row, 'records_last_year'] = last_records_year[stock]
            else: #如果出现了上个交易日没有交易的股票，开始统计
                records_year = 0
                for d in p_y_cal:
                    df = trading_records[d]
                    if stock not in list(df['ts_code']):
                        continue
                    if df.loc[df['ts_code'] == stock, 'vol'].values[0] > 0:
                        records_year += 1
                bar.loc[row, 'records_last_year'] = records_year
                last_records_year[stock] = records_year
        else: #如果与上个交易日不是一年，开始统计
            last_previous_year = previous_year
            records_year = 0
            for d in p_y_cal:
                df = trading_records[d]
                if stock not in list(df['ts_code']):
                    continue
                if df.loc[df['ts_code'] == stock, 'vol'].values[0] > 0:
                    records_year += 1

            bar.loc[row, 'records_last_year'] = records_year
            last_records_year[stock] = records_year
        if previous_month == last_previous_month: #月度统计与年度统计一样的逻辑与处理方式，不再重复注释
            if stock in last_records_month:
                bar.loc[row, 'records_last_month'] = last_records_month[stock]
            else:

                records_month = 0
                for dm in p_m_cal:
                    df = trading_records[dm]
                    if stock not in list(df['ts_code']):
                        continue
                    if df.loc[df['ts_code'] == stock, 'vol'].values[0] > 0:
                        records_month += 1
                bar.loc[row, 'records_last_month'] = records_month
                last_records_month[stock] = records_month
        else:
            last_previous_month = previous_month
            records_month = 0
            for dm in p_m_cal:
                df = trading_records[dm]
                if stock not in list(df['ts_code']):
                    continue
                if df.loc[df['ts_code'] == stock, 'vol'].values[0] > 0:
                    records_month += 1
            bar.loc[row, 'records_last_month'] = records_month
            last_records_month[stock] = records_month
    bar = bar.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'])
    bar.to_csv(data_path + day + '_final.csv')

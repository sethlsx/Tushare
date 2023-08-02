
import pandas as pd
import os


cwd_path = os.getcwd()
data_path = cwd_path+"/Data/"

trade_calendar = pd.read_csv(data_path+'trade_cal.csv')
print(trade_calendar.head())
trade_calendar['first_day_in_year'] = 0
trade_calendar['first_day_in_month'] = 0

#判断是否是年首日或者月首日，并标记
for row in trade_calendar.index:
    cal_date = str(trade_calendar.loc[row].cal_date)
    pretrade_date = str(trade_calendar.loc[row].pretrade_date)
    year = int(cal_date[:4])
    month = int(cal_date[4:6])
    pre_year = int(pretrade_date[:4])
    pre_month = int(pretrade_date[4:6])
    is_open = trade_calendar.loc[row].is_open
    #print(year)
    #print(month)
    if year > pre_year and is_open == 1:
        trade_calendar.loc[row, 'first_day_in_year'] = 1
        trade_calendar.loc[row, 'first_day_in_month'] = 1 #年首日必定是月首日
    if month > pre_month and is_open == 1:
        trade_calendar.loc[row, 'first_day_in_month'] = 1

print(trade_calendar.head())
trade_calendar.to_csv(data_path+'trade_cal_processed.csv')
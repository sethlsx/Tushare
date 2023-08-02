from datetime import datetime

str_date_1 = '20071207'
str_date_2 = '20161230'

date_1 = datetime.strptime(str_date_1, '%Y%m%d')
date_2 = datetime.strptime(str_date_2, '%Y%m%d')

diff = date_2 - date_1
diff_month = (date_2.year - date_1.year)*12+date_2.month-date_1.month
print(date_1)
print(date_2)
print(diff)
print(diff_month)
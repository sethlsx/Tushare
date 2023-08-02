# Tushare
Try to replicate the result from Size and Value in China

## .gitignore
主要忽略了：

1. 设置Token的Token.py，不设置token，tushare的接口是无法调用的
2. 数据文件夹Data

## 关于其他代码的说明

### 代码的运行顺序

*1. data_fetch.py*  
根据tushare的官方文档，[如何优雅高效的撸数据](https://tushare.pro/document/1?doc_id=230),首先获取相应时间区段的交易日历，然后按日历请求交易数据  
*2. cal_process.py*  
处理交易日历，标记出全年或者全月首个交易日  
*3. stock_universe_mkt_value.py*  
处理获得的交易数据，标记每只股票在对应交易日的市值数据  
*4. stock_universe_other.py*  
继续处理交易数据，标记每个交易日的每只股票的挂牌日期，交易日之时距离挂牌日期的月份差异，以及前一个月和前一年的有多少天有交易记录  
*5. 其他*  
*Liu et al. 2019 - Size and value in China.pdf*  
原论文  
*main.py*  
pycharm自动生成，没有用到  
*stock_list.py*  
一开始打算按照股票请求数据，后来按照官方稳定的解释用了按日期请求的方法，该代码只用于获得完整的股票列表，包括已上市，已退市和已暂停交易的全部股票  
*test.py test_date.py*  
用于测试一些不方便在终端里测试的东西


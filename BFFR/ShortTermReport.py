import yfinance as yf
import statistics as stats
from dataclasses import dataclass

@dataclass
class StockInfo:
    Ticker:str
    last_four_growth:float
    last_four_convexity:float
    last_month_growth:float
    last_month_convexity:float
    curr_val:float
    max_val_month:float
    hist_by_year_day:list
    hist_by_month_day:list


def ShortTermReport(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d", interval = "1h")
    val_array=list(hist["Close"][-32:])
    growth_array = list()
    for i in range(-1*len(val_array), -1):
        growth_array.append((hist["Close"].iloc[i+1]/hist["Close"].iloc[i])-1)
    last_four_growth = stats.linear_regression(list(range(1, len(val_array)+1)), val_array).slope
    last_four_convexity =  stats.linear_regression(list(range(1,len(val_array))), growth_array).slope
    hist = stock.history(period="1mo", interval = "1d")
    val_array=list(hist["Close"][-22:])
    growth_array = list()
    max_val = 0
    for i in range(-1*len(val_array), -1):
        growth_array.append((hist["Close"].iloc[i+1]/hist["Close"].iloc[i])-1)
        if (hist["Close"].iloc[i] > max_val):
            max_val = hist["Close"].iloc[i] 
    last_month_growth = stats.linear_regression(list(range(1, len(val_array)+1)), val_array).slope
    last_month_convexity = stats.linear_regression(list(range(1, len(val_array))), growth_array).slope
    curr_val = hist["Close"].iloc[-1]
    hist_by_year_day = stock.history(period="1y", interval = "1d")["Close"]
    hist_by_month_day = stock.history(period="1mo", interval = "1d")["Close"]
    return StockInfo(ticker, last_four_growth, last_four_convexity*100, last_month_growth, last_month_convexity*100, curr_val, max_val, list(hist_by_year_day), list(hist_by_month_day))
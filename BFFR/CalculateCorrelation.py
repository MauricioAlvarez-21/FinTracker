import numpy as np
import yfinance as yf
def CalculateCorrelation(ticker1, ticker2):
    stock1 = yf.Ticker(ticker1)
    stock2 = yf.Ticker(ticker2)
    hist1 = stock1.history(period="1mo", interval = "1d")
    hist2 = stock2.history(period="1mo", interval = "1d")
    data_array1 = np.array(hist1["Close"][-22:])
    data_array2 = np.array(hist2["Close"][-22:])
    r = np.corrcoef(data_array1, data_array2)
    return r[0,1]

ticker1 = input('Enter First Ticker: ')
ticker2 = input('Enter Second Ticker: ')
print(CalculateCorrelation(ticker1, ticker2))

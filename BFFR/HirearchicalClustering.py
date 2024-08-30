import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist
import scipy.cluster.hierarchy as sch
import yfinance as yf
import util_lists
import time 

def build_clusters(tickers):
    LastMonthDataList = list()
    iterations = 0
    for ticker in tickers:
        hist = yf.Ticker(ticker).history(period="1mo", interval = "1d")
        iterations +=1 
        if (iterations %100==0):
            print("Preventing API overload")
            time.sleep(30)
        growth_array = list()
        for i in range(-1*len(hist["Close"][-22:]), -1):
            growth_array.append(((hist["Close"].iloc[i+1]/hist["Close"].iloc[i])-1))
        LastMonthDataList.append(growth_array)
    LastMonthDataArray = np.array(LastMonthDataList)
    linkage_matrix = sch.linkage(LastMonthDataArray, method='single')
    return linkage_matrix

def get_associated_clusters(linkage_matrix, tickers, threshold, ticker = "AAPL"):
    ticker_index = tickers.index(ticker)
    cluster_id = sch.cut_tree(linkage_matrix,  height=threshold)[ticker_index]
    associated_clusters = [tickers[i] for i in range(len(tickers)) if sch.cut_tree(linkage_matrix, height=threshold)[i] == cluster_id]
    return associated_clusters
def main(tickers):
    linkage_matrix = build_clusters(util_lists.SPY_list)
    associated_clusters = get_associated_clusters(linkage_matrix, util_lists.SPY_list, 1)
    similar_tickers = dict()
    for i in range(len(associated_clusters)):
        if associated_clusters[i] in tickers:
            if (i-3 >0 and i+3 < len(associated_clusters)):
                similar_tickers[associated_clusters[i]] = associated_clusters[i-3:i+3]
            elif (i-3>0):
                similar_tickers[associated_clusters[i]] = associated_clusters[i-3:i]
            elif (i+3<len(associated_clusters)):
                similar_tickers[associated_clusters[i]] = associated_clusters[i:i+3]
    return similar_tickers
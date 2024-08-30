import util_lists
import ShortTermReport
import BasicMarkovChain
import time
import HirearchicalClustering
import GeminiSentimentScore
import UI
from dataclasses import dataclass
import yfinance as yf
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

@dataclass
class ProspectiveInvestment:
    Ticker:str
    last_four_growth:float
    last_four_convexity:float
    last_month_growth:float
    last_month_convexity:float
    curr_val:float
    max_val_month:float
    hist_by_month_day:list
    success_rate:float
    failure_rate:float
    gemini_rating:int
    related_tickers:list
    related_tickers_hist:list
    gemini_suggestion:str

qualified_tickers = list()
iterations = 0
for ticker in util_lists.SPY_list:
    # First triage finding only viable candidates.
  iterations +=1 
  if iterations % 100 == 0:
      print("Preventing API Overload")
      time.sleep(30)
  short_term_info = ShortTermReport.ShortTermReport(ticker)
  if(short_term_info.last_four_growth>0 and short_term_info.last_four_convexity>0 
     and short_term_info.last_month_growth>0 and short_term_info.last_month_convexity>0 
     and short_term_info.curr_val < short_term_info.max_val_month):
      qualified_tickers.append([short_term_info])
# Apply Markov Chain
start_time = time.time()
for stock_info in qualified_tickers:
    print(stock_info[0].Ticker)
    Markov_results = BasicMarkovChain.ComputeMarkovProbability(stock_info[0].hist_by_year_day)
    success_rate = Markov_results[0]
    failure_rate = Markov_results[1]
    stock_info.append(success_rate)
    stock_info.append(failure_rate)
end_time = time.time()
print(end_time-start_time)
sorted_by_risk = sorted(qualified_tickers, key = lambda x:x[2])[0:3]
triaged_investments = sorted(sorted_by_risk, key = lambda x:x[1], reverse=True)
# Apply Hirearchical Clustering
relations_dict = HirearchicalClustering.main([(triaged_investments[0])[0].Ticker,(triaged_investments[1])[0].Ticker, 
                                              (triaged_investments[2])[0].Ticker])
#Transfer Data
prospective_investments = list()
for triaged_investment in triaged_investments:
    prospective_investments.append(ProspectiveInvestment(triaged_investment[0].Ticker, triaged_investment[0].last_four_growth, 
                                                         triaged_investment[0].last_four_convexity, triaged_investment[0].last_month_growth,
                                                         triaged_investment[0].last_month_convexity, triaged_investment[0].curr_val,
                                                         triaged_investment[0].max_val_month, triaged_investment[0].hist_by_month_day,
                                                         triaged_investment[1], triaged_investment[2], 
                                                         GeminiSentimentScore.CalculateSentimentScore(triaged_investment[0].Ticker),
                                                         relations_dict[triaged_investment[0].Ticker],[],""))
# Extract related ticker info
for investment in prospective_investments:
    for ticker in investment.related_tickers:
        investment.related_tickers_hist.append([ticker, yf.Ticker(ticker).history(period="1y", interval = "1d")["Close"]])
# Get Gemini Suggestion
for investment in prospective_investments:
    prompt = "Hello Gemini! I would like to you to give me thoughts on buying " + investment.Ticker + "(ticker for company) shares to be held for the next 2-3 days. According to my basic Markov Analysis, the stock from this company has a " + str(investment.success_rate*100) + "% probability of growing above 2% in the next 3 business days. Per the same analysis it also has a " +  str(investment.failure_rate*100) + "% chance of decreasing in value, generating a loss. In the scale of 1 to 10 it has a sentiment score of " + str(investment.gemini_rating) + ". The stock is currently priced at " + str(investment.curr_val) + "$ per share, and in the last month. it had a maximun value of " + str(investment.max_val_month) + "$ In particular, this ticker has behaved similar to the following companies:"
    for val in investment.related_tickers_hist:
        markov_analysis = BasicMarkovChain.ComputeMarkovProbability(val[1])
        prompt += ". " + val[0] + "(ticker for company) with a " + str(markov_analysis[0]*100) + "% probability of growing over 2% in the next 2-3 days.     "
    prompt += "Please provide a 150 word analysis on why purchasing shares of" + investment.Ticker + " (ticker for company) is or not a potentially successful investment in the next 2-3 days"
    investment.gemini_suggestion = GeminiSentimentScore.Generic(prompt)

root1 = tk.Tk()
root1.title("Tkinter Window")
section1 = UI.create_section(root1, prospective_investments[0])
section1.pack(pady=20)
root1.mainloop()

root2 = tk.Tk()
root2.title("Tkinter Window")
section2 = UI.create_section(root2, prospective_investments[1])
section2.pack(pady=20)
root2.mainloop()

root3 = tk.Tk()
root3.title("Tkinter Window")
section3 = UI.create_section(root3, prospective_investments[2])
section3.pack(pady=20)
root3.mainloop()
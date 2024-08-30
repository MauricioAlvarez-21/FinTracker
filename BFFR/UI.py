import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import BasicMarkovChain

def create_section(root, prospective_investment):
    section_frame = tk.Frame(root)

    title_Label = tk.Label(section_frame, text=(prospective_investment.Ticker + " @  $" + str(prospective_investment.curr_val)), font=("Arial", 14, "bold"), fg="green")
    title_Label.pack(pady=10)

    table_frame = tk.Frame(section_frame)
    cell_1 = tk.Label(table_frame, text=f"4-growth", bg="blue", width=15, height=2)
    cell_1.grid(row =0, column =0, padx=5, pady=5)
    color_2 = "green" if (prospective_investment.last_four_growth)*100 > 2 else "red"
    cell_2 = tk.Label(table_frame, text=str((prospective_investment.last_four_growth)*100) + " %", bg=color_2, width=25, height=2)
    cell_2.grid(row=0, column=1, padx=5, pady=5)

    cell_3 = tk.Label(table_frame, text=f"Month growth", bg="blue", width=15, height=2)
    cell_3.grid(row =0, column =2, padx=5, pady=5)
    color_4 = "green" if (prospective_investment.last_month_growth)*100 > 4 else "red"
    cell_4 = tk.Label(table_frame, text=str((prospective_investment.last_month_growth)*100) + " %", bg=color_4, width=25, height=2)
    cell_4.grid(row=0, column=3, padx=5, pady=5)

    cell_5 = tk.Label(table_frame, text=f"Success Rate", bg="blue", width=15, height=2)
    cell_5.grid(row =0, column =4, padx=5, pady=5)
    color_6 = "green" if (prospective_investment.success_rate)*100 > 50 else "red"
    cell_6 = tk.Label(table_frame, text=str((prospective_investment.success_rate)*100) + " %", bg=color_6, width=25, height=2)
    cell_6.grid(row=0, column=5, padx=5, pady=5)

    cell_7 = tk.Label(table_frame, text=f"4-concavity", bg="blue", width=15, height=2)
    cell_7.grid(row =1, column =0, padx=5, pady=5)
    color_8 = "green" if (prospective_investment.last_four_convexity)*100 > 0.5 else "red"
    cell_8 = tk.Label(table_frame, text=str((prospective_investment.last_four_convexity)*100) + " %", bg=color_8, width=25, height=2)
    cell_8.grid(row=1, column=1, padx=5, pady=5)

    cell_9 = tk.Label(table_frame, text=f"Month concavity", bg="blue", width=15, height=2)
    cell_9.grid(row =1, column =2, padx=5, pady=5)
    color_10 = "green" if (prospective_investment.last_month_convexity)*100 > 0.5 else "red"
    cell_10 = tk.Label(table_frame, text=str((prospective_investment.last_month_convexity)*100) + " %", bg=color_10, width=25, height=2)
    cell_10.grid(row=1, column=3, padx=5, pady=5)

    cell_11 = tk.Label(table_frame, text=f"Failure Rate", bg="blue", width=15, height=2)
    cell_11.grid(row =1, column =4, padx=5, pady=5)
    color_12 = "green" if (prospective_investment.failure_rate)*100 < 25 else "red"
    cell_12 = tk.Label(table_frame, text=str((prospective_investment.failure_rate)*100) + " %", bg=color_12, width=25, height=2)
    cell_12.grid(row=1, column=5, padx=5, pady=5)

    cell_13 = tk.Label(table_frame, text=f"MaxVal Month", bg="blue", width=15, height=2)
    cell_13.grid(row =0, column =6, padx=5, pady=5)
    cell_14 = tk.Label(table_frame, text="$" + str(prospective_investment.max_val_month) + " %", bg="blue", width=25, height=2)
    cell_14.grid(row=0, column=7, padx=5, pady=5)

    cell_15 = tk.Label(table_frame, text=f"Gemini Rating", bg="blue", width=15, height=2)
    cell_15.grid(row =1, column =6, padx=5, pady=5)
    color_16 = "green" if prospective_investment.gemini_rating > 5 else "red"
    cell_16 = tk.Label(table_frame, text=str(prospective_investment.gemini_rating), bg=color_12, width=25, height=2)
    cell_16.grid(row=1, column=7, padx=5, pady=5)


    table_frame.pack(pady=10)
    graph_frame = tk.Frame(section_frame)
    figure = Figure(figsize=(5, 3))
    ax = figure.add_subplot(111)
    ax.plot(prospective_investment.hist_by_month_day)
    canvas = FigureCanvasTkAgg(figure, graph_frame)
    canvas.get_tk_widget().pack()
    graph_frame.pack(pady=10)

    table_frame = tk.Frame(section_frame)
    
    cell_1 = tk.Label(table_frame, text=f"Ticker", bg="blue", width=25, height=2)
    cell_1.grid(row =0, column =0, padx=5, pady=5)
    cell_2 = tk.Label(table_frame, text=f"Success Rate", bg="blue", width=25, height=2)
    cell_2.grid(row =0, column =1, padx=5, pady=5)
    cell_3 = tk.Label(table_frame, text=f"Failure Rate", bg="blue", width=25, height=2)
    cell_3.grid(row =0, column =2, padx=5, pady=5)
    for i in range(len(prospective_investment.related_tickers_hist)):
        cell_ticker = tk.Label(table_frame, text=prospective_investment.related_tickers_hist[i][0], bg="blue", width=25, height=2)
        cell_ticker.grid(row =i+1, column =0, padx=5, pady=5)
        markov_result = BasicMarkovChain.ComputeMarkovProbability(prospective_investment.related_tickers_hist[i][1])
        color_success = "green" if (markov_result[0])*100 > 50 else "red"
        cell_success = tk.Label(table_frame, text=str((markov_result[0])*100) + " %", bg=color_success, width=25, height=2)
        cell_success.grid(row=i+1, column=1, padx=5, pady=5)
        color_failure = "green" if (markov_result[1])*100 < 25 else "red"
        cell_failure = tk.Label(table_frame, text=str((markov_result[1])*100) + " %", bg=color_failure, width=25, height=2)
        cell_failure.grid(row=i+1, column=2, padx=5, pady=5)
    table_frame.pack(pady=10)

    return section_frame
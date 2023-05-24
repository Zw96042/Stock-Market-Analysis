import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import messagebox, OptionMenu
from tkcalendar import DateEntry
import pprint
import datetime

canvas = None  # Global variable for the canvas
keywords = [
    'symbol', 'name', 'price', 'marketCap', 'dividendYield', 'trailingPE', 'forwardPE', 
    'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 
    'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 
    'beta', 'volume', 'regularMarketVolume', 'averageVolume', 'averageVolume10days', 'bid', 
    'ask', 'bidSize', 'askSize', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'trailingAnnualDividendRate', 
    'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins', 'floatShares', 
    'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth', 'heldPercentInsiders', 
    'heldPercentInstitutions', 'shortRatio', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth', 
    'netIncomeToCommon', 'trailingEps', 'forwardEps', 'pegRatio', 'enterpriseToRevenue', 
    'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange', 'exchange', 'currentPrice', 
    'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 
    'recommendationMean', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash', 
    'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 
    'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'grossProfits', 
    'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 
    'ebitdaMargins', 'operatingMargins', 'trailingPegRatio'
]


def generate_graph():
    global canvas  # Access the global canvas variable
    if not stock_var.get():
        return messagebox.showerror("No Stock Symbols", "Please enter at least one stock symbol.")
    
    stock_symbols = stock_var.get().split(',')
    
    
    try:
        window_size = int(window_size_entry.get())
    except ValueError:
        return messagebox.showerror("Invalid Input", "Please enter a valid window size.")

    start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
    end_date = end_date_entry.get_date().strftime('%Y-%m-%d')

    if start_date == end_date:
        return messagebox.showerror("Invalid Dates", "Start and end dates cannot be the same.")
    

    # Create a figure and subplot for the graph
    fig, ax = plt.subplots(figsize=(8, 6))

    global stock_info  # Dictionary to store stock information
    stock_info = {}

    for symbol in stock_symbols:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            return messagebox.showerror("Invalid Stock Symbol", f"The stock symbol '{symbol}' is invalid.")
            
        # Retrieve stock information
        stock = yf.Ticker(symbol)
        info = stock.info

        # Calculate the SMA for the specified window size
        stock_data['SMA'] = stock_data['Close'].rolling(window=window_size).mean() 

        # Plot the closing price and SMA
        ax.plot(stock_data.index, stock_data['Close'], label=f"{info.get('longName', '')} Closing Price")
        ax.plot(stock_data.index, stock_data['SMA'], label=f"{info.get('longName', '')} SMA {window_size}")

        stock_data.reset_index(inplace=True)

        # Store stock information in the dictionary
        stock_info[symbol] = info

    # Set the x-axis label and title
    ax.set_xlabel('Date')
    ax.set_title(f'Stock Prices with SMA {window_size} Trend')
    ax.legend()

    date_format = mdates.DateFormatter('%b %d')  # Specify the desired date format
    ax.xaxis.set_major_formatter(date_format)



    # Clear the previous graph from the canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    # Create a new canvas to display the graph
    canvas = FigureCanvasTkAgg(fig, master=display_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, columnspan=2)

    # Update the dropdown menu with the stock information
    info_dropdown['menu'].delete(0, 'end')  # Clear previous options

    for symbol, info in stock_info.items():
        # Create a label for each stock with relevant information
        label = f"{symbol}: {info.get('longName', '')}"
        info_dropdown['menu'].add_command(label=label, command=tk._setit(info_var, symbol))

    # Update the selected option in the dropdown menu
    info_var.set('')  # Reset the selected option


def show_stock_info(*args):
    selected_option = info_var.get()
    print(info_var.get())
    selected_option = stock_info.get(selected_option)
    if selected_option:
        selected_keywords = [selected_option]
        selected_keywords = selected_keywords[0]  # Assuming selected_keywords is a list with a single dictionary
        filtered_data = {key: value for key, value in selected_keywords.items() if key in keywords or key.lower() in keywords}
        formatted_data = pprint.pformat(filtered_data)
        print(formatted_data)
        messagebox.showinfo("Stock Info", formatted_data)
            

    else:
        selected_keywords = []
    # if selected_option:
        

window = tk.Tk()
window.title("Stock Info")

# Create a frame for the input section
input_frame = tk.Frame(window)
input_frame.pack(pady=10)

# Stock Symbol Label and Entry
symbol_label = tk.Label(input_frame, text="Stock Symbols (separated by comma):")
symbol_label.grid(row=0, column=0)
stock_var = tk.StringVar()
symbol_entry = tk.Entry(input_frame, textvariable=stock_var)
symbol_entry.grid(row=0, column=1)

# Window Size Label and Entry
window_size_label = tk.Label(input_frame, text="Window Size:")
window_size_label.grid(row=1, column=0)
window_size_entry = tk.Entry(input_frame)
window_size_entry.grid(row=1, column=1)

# Start Date Label and DateEntry
start_date_label = tk.Label(input_frame, text="Start Date:")
start_date_label.grid(row=0, column=2)
start_date_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
start_date_entry.grid(row=0, column=3)

# End Date Label and DateEntry
end_date_label = tk.Label(input_frame, text="End Date:")
end_date_label.grid(row=1, column=2)
end_date_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
end_date_entry.grid(row=1, column=3)

# Generate Graph Button
generate_button = tk.Button(window, text="Generate Graph", command=generate_graph)
generate_button.pack(pady=10)

# Create a frame for the stock info and graph display
display_frame = tk.Frame(window)
display_frame.pack()

# Stock Info Dropdown
info_label = tk.Label(display_frame, text="Stock Information:")
info_label.grid(row=0, column=0)
info_var = tk.StringVar()
info_var.trace('w', show_stock_info)  # Call show_stock_info when the dropdown selection changes
info_dropdown = OptionMenu(display_frame, info_var, "")
info_dropdown.grid(row=0, column=1)

# Run the Tkinter event loop
window.mainloop()
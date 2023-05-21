import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import sys

window = tk.Tk()
window.title("Stock Info")

fig = plt.Figure(figsize=(8, 6))
ax = fig.add_subplot(111)
stock_symbol = input("Please provide the ticker symbol for the stock: ")  # Example stock symbol
# Check if the stock symbol is valid
try:
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    print(f"Stock symbol '{stock_symbol}' is valid.")
    
    # Retrieve stock data from Yahoo Finance
    stock_data = yf.download(stock_symbol, start="2023-01-01", end="2023-05-31")

    window_size = float(input("Enter the window size for the SMA: "))

    # Calculate the SMA for the specified window size
    stock_data['SMA'] = stock_data['Close'].rolling(window=window_size).mean()

    # Reset the index to make the date column accessible
    stock_data.reset_index(inplace=True)

    print(info.get('longName') or info.get('shortName'))
except:
    print(f"Ticker symbol '{stock_symbol}' is not valid.")
    sys.exit(1)


# Graph
# Plot the closing price and SMA
ax.plot(stock_data['Date'], stock_data['Close'], label='Closing Price')
ax.plot(stock_data['Date'], stock_data['SMA'], label=f'SMA {window_size}')

# Determine the trend based on the SMA relationship
for i in range(window_size, len(stock_data)):
    if stock_data['SMA'].iloc[i] > stock_data['SMA'].iloc[i - 1]:
        ax.scatter(stock_data['Date'].iloc[i], stock_data['Close'].iloc[i], color='green', marker='^')
    else:
        ax.scatter(stock_data['Date'].iloc[i], stock_data['Close'].iloc[i], color='red', marker='v')

ax.set_xlabel('Date')
ax.set_ylabel('Price')
ax.set_title(f'Stock Price with SMA {window_size} Trend')
ax.legend()

# Create a FigureCanvasTkAgg widget
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()

# Place the canvas in the Tkinter window
canvas.get_tk_widget().pack()


# Info
keywords = ['symbol', 'name', 'price', 'marketCap', 'dividendYield', 'trailingPE', 'forwardPE', 'previousClose', 'open', 'dayLow', 'dayHigh', 'regularMarketPreviousClose', 'regularMarketOpen', 'regularMarketDayLow', 'regularMarketDayHigh', 'dividendRate', 'beta', 'volume', 'regularMarketVolume', 'averageVolume', 'averageVolume10days', 'bid', 'ask', 'bidSize', 'askSize', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'trailingAnnualDividendRate', 'trailingAnnualDividendYield', 'currency', 'enterpriseValue', 'profitMargins', 'floatShares', 'sharesOutstanding', 'sharesShort', 'sharesShortPriorMonth', 'heldPercentInsiders', 'heldPercentInstitutions', 'shortRatio', 'bookValue', 'priceToBook', 'earningsQuarterlyGrowth', 'netIncomeToCommon', 'trailingEps', 'forwardEps', 'pegRatio', 'enterpriseToRevenue', 'enterpriseToEbitda', '52WeekChange', 'SandP52WeekChange', 'exchange', 'currentPrice', 'targetHighPrice', 'targetLowPrice', 'targetMeanPrice', 'targetMedianPrice', 'recommendationMean', 'recommendationKey', 'numberOfAnalystOpinions', 'totalCash', 'totalCashPerShare', 'ebitda', 'totalDebt', 'quickRatio', 'currentRatio', 'totalRevenue', 'debtToEquity', 'revenuePerShare', 'returnOnAssets', 'returnOnEquity', 'grossProfits', 'freeCashflow', 'operatingCashflow', 'earningsGrowth', 'revenueGrowth', 'grossMargins', 'ebitdaMargins', 'operatingMargins', 'trailingPegRatio']

# Create labels for filtered info
for key, value in info.items():
    if any(keyword in key.lower() for keyword in keywords):
        label_text = f"{key}: {value}"
        label = tk.Label(window, text=label_text)
        label.pack()

window.mainloop()
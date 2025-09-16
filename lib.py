import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import easygui
import keyboard

def stock_view():
    yesterday = date.today() - timedelta(1)

    stock_name = easygui.enterbox("Enter stock name")

    ticker = stock_name  # Apple stock
    start_date = "2025-01-01"
    end_date = yesterday

    data = yf.download(ticker, start=start_date, end=end_date)

    print(data.head())



    short_window = 7
    long_window = 30

    data['SMA Short Win'] = data['Close'].rolling(window=short_window).mean()
    data['SMA Long Win'] = data['Close'].rolling(window=long_window).mean()


    data['Signal'] = 0
    data.loc[data['SMA Short Win'] > data['SMA Long Win'], 'Signal'] = 1
    data.loc[data['SMA Short Win'] < data['SMA Long Win'], 'Signal'] = -1


    data['Position'] = data['Signal'].shift(1)

    data['Daily Return'] = data['Close'].pct_change()

    data['Strategy Return'] = data['Position'] * data['Daily Return']

    data['Cumulative Market Return'] = (1 + data['Daily Return']).cumprod()
    data['Cumulative Strategy Return'] = (1 + data['Strategy Return']).cumprod()

    total_strategy_return = data['Cumulative Strategy Return'].iloc[-1] - 1
    total_market_return = data['Cumulative Market Return'].iloc[-1] - 1

    print(f"Total Strategy Return: {total_strategy_return:.2%}")
    print(f"Total Market Return: {total_market_return:.2%}")

    plot_choice = easygui.choicebox(msg="Choose one option", choices=("Price and Moving Averages","Cumulative Returns"))
    if (plot_choice == "Price and Moving Averages"):
        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label='Close Price', alpha=0.5)
        plt.plot(data['SMA Short Win'], label='SMA Short-Term', alpha=0.75)
        plt.plot(data['SMA Long Win'], label='SMA Long-Term', alpha=0.75)
        plt.title(f"{ticker} Price and Moving Averages")
        plt.legend()
        plt.show()
        pass
    else:
        plt.figure(figsize=(14, 7))
        plt.plot(data['Cumulative Market Return'], label='Market Return', alpha=0.75)
        plt.plot(data['Cumulative Strategy Return'], label='Strategy Return', alpha=0.75)
        plt.title("Cumulative Returns")
        plt.legend()
        plt.show()
    if(keyboard.is_pressed("q")):
        exit()

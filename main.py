import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import easygui
from lib import stock_view



while True:
    new_win = input("Do you want a new stock view? [Y/n] ")
    if new_win == "Y":
        stock_view()
    else:
        break
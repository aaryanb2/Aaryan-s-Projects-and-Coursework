import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from matplotlib.pyplot import close

import util

class Indicators:
    def __init__(self, lb = 14, symbol = "AAPL", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31)):
        # Initialize any necessary variables or data structures here
        self.lb = lb
        self.symbol = symbol
        self.sd = sd
        self.ed = ed

    def bolinger_band_ind(self, isPlot = False):
        # Public method ind1
        # Implement your logic here
        new_sd = self.sd - dt.timedelta(days=self.lb*2)
        price = util.get_data([self.symbol],dates=pd.date_range(new_sd, self.ed))
        price = price[self.symbol].to_frame()
        while self.sd not in price.index:
            self.sd = self.sd + dt.timedelta(days=1)
        new_ind = price.index.get_loc(self.sd)
        sma = price.rolling(window=self.lb, min_periods=self.lb).mean()
        rolling_std = price.rolling(window=self.lb, min_periods=self.lb).std()
        sma = sma.iloc[new_ind:]
        price = price.iloc[new_ind:]
        rolling_std = rolling_std.iloc[new_ind:]
        top_band = sma + (rolling_std * 2)
        bottom_band = sma - (rolling_std * 2)
        bolbandperc = (price- bottom_band) / (top_band - bottom_band)
        bolbandperc[bolbandperc == np.inf] = 0.5
        if isPlot:
            fig, ax = plt.subplots()
            ax.plot(price.index, price[self.symbol], color="blue", label="Price")
            ax.plot(top_band.index, top_band[self.symbol], color="green", label="Upper Bollinger Band")
            ax.plot(bottom_band.index, bottom_band[self.symbol], color="red", label="Lower Bollinger Band")
            ax.plot(sma.index, sma[self.symbol], color="orange", label="SMA")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("Price", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.legend()
            plt.title("Bollinger Bands Plot with 20 day lookback", fontsize=16)
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure1.png')

            fig, ax = plt.subplots()
            ax.plot(bolbandperc.index, bolbandperc[self.symbol], color="orange", label="BB%")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("BB%", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.title("Bollinger Bands % 20 day indicator", fontsize=16)
            plt.axhline(0, linestyle='--', color='g', label= "Lower Band")
            plt.axhline(1, linestyle='--', color='r', label= "Upper Band")
            plt.legend()
            fig = ax.get_figure()
            fig.set_size_inches(14,6)
            fig.tight_layout()
            fig.savefig('images/Figure2.png')
        return bolbandperc


    def rsi_ind(self, isPlot = False):
        new_sd = self.sd - dt.timedelta(days=self.lb*2)
        price = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed))
        price = price[self.symbol].to_frame()
        daily_returns = price.diff()
        up_gain, down_loss = daily_returns.copy(), daily_returns.copy()
        up_gain[up_gain < 0] = 0
        down_loss[down_loss > 0] = 0
        avg_gain = up_gain.rolling(window=self.lb).mean()
        avg_loss = abs(down_loss.rolling(window=self.lb).mean())
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        rsi[rsi == np.inf] = 100
        while self.sd not in price.index:
            self.sd = self.sd + dt.timedelta(days=1)
        new_ind = price.index.get_loc(self.sd)
        rsi = rsi.iloc[new_ind:]
        if isPlot:
            fig, ax = plt.subplots()
            ax.plot(rsi.index, rsi[self.symbol], color="blue", label="RSI")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("RSI Value", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.title("RSI Plot with 14 day lookback", fontsize=16)
            plt.axhline(70, linestyle='--', color='r', label= "Overbought Line")
            plt.axhline(30, linestyle='--', color='g', label= "Oversold Line")
            plt.legend()
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure3.png')
        return rsi

    def ultimate_oscillator_ind(self, short_period=7, medium_period=14, long_period=28, isPlot=False):
        # Public method ind3
        # Implement your logic here
        new_sd = self.sd - dt.timedelta(days=long_period*2)
        price = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed))
        price = price[self.symbol].to_frame()
        high = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed), colname="High")
        high = high[self.symbol].to_frame()
        low = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed), colname="Low")
        low = low[self.symbol].to_frame()
        close = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed), colname="Close")
        close = close[self.symbol].to_frame()
        high = high * (price/close)
        low = low * (price/close)
        price.rename(columns={self.symbol: 'Price'}, inplace=True)
        high.rename(columns={self.symbol: 'High'}, inplace=True)
        low.rename(columns={self.symbol: 'Low'}, inplace=True)
        a = pd.concat([low, price.shift(1)], axis=1, ignore_index=True).min(axis=1).to_frame('name')
        buy_press = (price['Price'] - a['name']).to_frame('name')
        m = pd.concat([high,price.shift(1)], axis=1, ignore_index=True).max(axis=1).to_frame('name')
        n = pd.concat([low,price.shift(1)], axis=1, ignore_index=True).min(axis=1).to_frame('name')
        true_range = (m['name'] - n["name"]).to_frame('name')
        short_period_avg = buy_press.rolling(short_period).sum() / true_range.rolling(short_period).sum()
        medium_period_avg = buy_press.rolling(medium_period).sum() / true_range.rolling(medium_period).sum()
        long_period_avg = buy_press.rolling(long_period).sum() / true_range.rolling(long_period).sum()
        ult_osc = (((4 * short_period_avg) + (2 * medium_period_avg) + long_period_avg) / 7)*100
        while self.sd not in price.index:
            self.sd = self.sd + dt.timedelta(days=1)
        new_ind = price.index.get_loc(self.sd)
        ult_osc = ult_osc.iloc[new_ind:]
        if isPlot:
            fig, ax = plt.subplots()
            ax.plot(ult_osc.index, ult_osc['name'], color="blue", label="Ultimate Oscillator")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("Ultimate Oscillator Value", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.title("Ultimate Oscillator Plot with 7, 14 and 28 day lookbacks", fontsize=16)
            plt.axhline(70, linestyle='--', color='r', label= "Overbought Line")
            plt.axhline(30, linestyle='--', color='g', label= "Oversold Line")
            plt.legend()
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure4.png')
        return ult_osc

    def ppo_indicator(self, short_period=12, long_period=26, signal_period=9, isPlot=False):
        new_sd = self.sd - dt.timedelta(days=long_period*2)
        price = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed))
        price = price[self.symbol].to_frame()
        while self.sd not in price.index:
            self.sd = self.sd + dt.timedelta(days=1)
        new_ind = price.index.get_loc(self.sd)
        short_ema = price.ewm(span=short_period, adjust=False).mean()
        long_ema = price.ewm(span=long_period, adjust=False).mean()
        ppo = ((short_ema - long_ema)/long_ema)*100
        signal_line = ppo.ewm(span=signal_period, adjust=False).mean()
        ppo_ind = ppo - signal_line
        ppo_ind = ppo_ind.iloc[new_ind:]
        ppo = ppo.iloc[new_ind:]
        signal_line = signal_line.iloc[new_ind:]
        if isPlot:
            fig, ax = plt.subplots()
            ax.plot(ppo_ind.index, ppo_ind[self.symbol], color="blue", label="PPO Indicator")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("PPO Value (%) - Signal Line(%)", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.legend()
            plt.title("PPO(%) - Signal Line(%)", fontsize=16)
            plt.axhline(0, linestyle='--', color='r')
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure6.png')

            fig, ax = plt.subplots()
            ax.plot(ppo.index, ppo[self.symbol], color="black", label="PPO (%)")
            ax.plot(signal_line.index, signal_line[self.symbol], color="red", label="Signal Line (%)")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("Percentage(%)", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.legend()
            plt.title("PPO and Signal Line Plot", fontsize=16)
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure5.png')
        return ppo_ind

    def tema_ind(self, isPlot=False):
        lookback = self.lb*2
        if self.lb < 50:
            lookback = 80
        new_sd = self.sd - dt.timedelta(days=lookback)
        price = util.get_data([self.symbol], dates=pd.date_range(new_sd, self.ed))
        price = price[self.symbol].to_frame()
        while self.sd not in price.index:
            self.sd = self.sd + dt.timedelta(days=1)
        new_ind = price.index.get_loc(self.sd)
        ema1 = price.ewm(span=self.lb, adjust=False).mean()
        ema2 = price.ewm(span=self.lb, adjust=False).mean()
        ema3 = price.ewm(span=self.lb, adjust=False).mean()
        tma_val = 3 * ema1 - 3 * ema2 + ema3
        ema1 = price.ewm(span=40, adjust=False).mean()
        ema2 = price.ewm(span=40, adjust=False).mean()
        ema3 = price.ewm(span=40, adjust=False).mean()
        tma_50 = 3 * ema1 - 3 * ema2 + ema3
        tma_ind = tma_val - tma_50
        tma_ind = tma_ind.iloc[new_ind:]
        if isPlot:
            fig, ax = plt.subplots()
            ax.plot(tma_ind.index, tma_ind[self.symbol], color="blue", label="TEMA Indicator")
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.set_xlabel("Date", fontsize=14)
            ax.set_ylabel("TEMA(14) - TEMA(50)", fontsize=14)
            ax.margins(x=0)
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=6)
            plt.grid()
            plt.legend()
            plt.title("TEMA Indicator Plot", fontsize=14)
            plt.axhline(0, linestyle='--', color='r')
            fig = ax.get_figure()
            fig.set_size_inches(14, 6)
            fig.tight_layout()
            fig.savefig('images/Figure7.png')
        return tma_ind

if __name__ == "__main__":
    # ind1 = Indicators(lb=20, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    # b_perc = ind1.bolinger_band_ind(isPlot=True)
    # ind2 = Indicators(lb=14, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    # rsi = ind2.rsi_ind(isPlot=True)
    # ind3 = Indicators(lb=14, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    # ult_osc = ind3.ultimate_oscillator_ind(short_period=7, medium_period=14, long_period=28, isPlot=True)
    # ind4 = Indicators(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    # ppo_ind = ind4.ppo_indicator(short_period=12, long_period=26, signal_period=9, isPlot=True)
    # ind5 = Indicators(lb=14, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    # tema = ind4.tema_ind(isPlot=True)
    pass

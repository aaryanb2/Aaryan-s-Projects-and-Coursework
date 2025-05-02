""""""
from contextlib import nullcontext

from fontTools.pens.basePen import NullPen
from fontTools.subset.svg import ranges
  		  	   		 	   		  		  		    	 		 		   		 		  
import math
import datetime as dt  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import numpy as np  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		  	   		 	   		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 	   		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as opt
import matplotlib.dates as mdates


def optimize_portfolio(  		  	   		 	   		  		  		    	 		 		   		 		  
    sd,  		  	   		 	   		  		  		    	 		 		   		 		  
    ed,  		  	   		 	   		  		  		    	 		 		   		 		  
    syms,  		  	   		 	   		  		  		    	 		 		   		 		  
    gen_plot=False,  		  	   		 	   		  		  		    	 		 		   		 		  
):  		  	   		 	   		  		  		    	 		 		   		 		    	   		 	   		  		  		    	 		 		   		 		  	  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		  	   		 	   		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		  	   		 	   		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY

    # clean the data
    prices_all.fillna(method="ffill", inplace=True)
    prices_all.fillna(method="bfill", inplace=True)

    # normalize values
    prices_all = (prices_all / prices_all[:1].values)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # set a guess value of equal allocations for symbols
    guess = np.ones(len(syms))
    guess = guess/len(syms)

    # find the allocations for the optimal portfolio
    bounds = ((0.0, 1.0),) * len(syms)
    cons = {'type': 'eq', 'fun': lambda x: 1-sum(abs(x))}
    result = opt.minimize(neg_sharpe_ratio, guess, args = (prices, ), method= 'SLSQP', bounds = bounds, constraints = cons)
  	   		 	   		  		  		    	 		 		   		 		  
    allocs = result.x

    # Get daily portfolio value
    ports_value = allocs * prices
    port_value = ports_value.sum(axis=1)
    port_daily_returns = port_value.copy()
    port_daily_returns[1:] = (port_value[1:] / port_value[:-1].values) - 1
    port_daily_returns = port_daily_returns[1:]
    sr = neg_sharpe_ratio(allocs, prices) * -1.0
    cr = port_value[-1]/port_value[0] -1
    adr = port_daily_returns.mean()
    sddr = port_daily_returns.std(ddof=1)
  		  	   		 	   		  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		 	   		  		  		    	 		 		   		 		  
    if gen_plot:  		  	   		 	   		  		  		    	 		 		   		 		  
        # add code to plot here  		  	   		 	   		  		  		    	 		 		   		 		  
        df_temp = pd.concat(  		  	   		 	   		  		  		    	 		 		   		 		  
            [port_value, prices_SPY], keys=["Portfolio", "SPY"], axis=1
        )  		  	   		 	   		  		  		    	 		 		   		 		  
        ax = df_temp.plot(title= "Daily Optimized Portfolio vs SPY Value", fontsize=8)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        fmt = mdates.DateFormatter('%b %Y')
        ax.xaxis.set_major_formatter(fmt)
        ax.margins(x=0)
        plt.grid()
        
        fig = ax.get_figure()
        fig.savefig('images/Optimized_Portfolio.png')
    # Return all required metrics
    return allocs, cr, adr, sddr, sr  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
def neg_sharpe_ratio(alloc, data):
    ports_value = alloc*data
    port_value = ports_value.sum(axis=1)  #sum the allocations to get daily value
    port_daily_returns = port_value.copy()
    port_daily_returns[1:] = (port_value[1:] / port_value[:-1].values) - 1 #daily returns formula
    port_daily_returns = port_daily_returns[1:]  #remove the zero value in the start
    k = math.sqrt(252)  #anualized value by day for sharpe ratio
    sharpe_ratio = k * (port_daily_returns.mean() / port_daily_returns.std(ddof=1))
    return sharpe_ratio*(-1.0) # need to minimize so multiplying by negative 1


def test_code():
  		  	   		 	   		  		  		    	 		 		   		 		  
    # Call optimize function to save chart
    syms = ['IBM', 'X', 'GLD', 'JPM']
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=dt.datetime(2008,6,1),
                                                        ed=dt.datetime(2009,6,1),
                                                        syms=['IBM','X','GLD','JPM'], gen_plot=True)
    with open("images/p3_results.txt", "w") as text_file:
        print(f"Stocks:{syms}", file=text_file)
        print(f"Allocations:{allocations}", file=text_file)
        print(f"Sharpe Ratio: {sr}", file=text_file)
        print(f"Volatility (stdev of daily returns): {sddr}", file=text_file)
        print(f"Average Daily Return: {adr}", file=text_file)
        print(f"Cumulative Return: {cr}", file=text_file)
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	   		  		  		    	 		 		   		 		    	   		 	   		  		  		    	 		 		   		 		  
    test_code()  		  	   		 	   		  		  		    	 		 		   		 		  

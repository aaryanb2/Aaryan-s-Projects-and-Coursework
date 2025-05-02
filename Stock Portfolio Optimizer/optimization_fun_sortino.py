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
    sd=dt.datetime(2008, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
    ed=dt.datetime(2009, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		 	   		  		  		    	 		 		   		 		  
    gen_plot=False,  		  	   		 	   		  		  		    	 		 		   		 		  
):  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		 	   		  		  		    	 		 		   		 		  
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		 	   		  		  		    	 		 		   		 		  
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		 	   		  		  		    	 		 		   		 		  
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		 	   		  		  		    	 		 		   		 		  
    statistics.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 	   		  		  		    	 		 		   		 		  
    :type sd: datetime  		  	   		 	   		  		  		    	 		 		   		 		  
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 	   		  		  		    	 		 		   		 		  
    :type ed: datetime  		  	   		 	   		  		  		    	 		 		   		 		  
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		 	   		  		  		    	 		 		   		 		  
        symbol in the data directory)  		  	   		 	   		  		  		    	 		 		   		 		  
    :type syms: list  		  	   		 	   		  		  		    	 		 		   		 		  
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		 	   		  		  		    	 		 		   		 		  
        code with gen_plot = False.  		  	   		 	   		  		  		    	 		 		   		 		  
    :type gen_plot: bool  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		 	   		  		  		    	 		 		   		 		  
        standard deviation of daily returns, and Sharpe ratio  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: tuple  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
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
    result = opt.minimize(neg_sortino_ratio, guess, args = (prices, ), method= 'SLSQP', bounds = bounds, constraints = cons)

    # note that the values here ARE NOT meant to be correct for a test case  		  	   		 	   		  		  		    	 		 		   		 		  
    allocs = result.x

    # Get daily portfolio value
    ports_value = allocs * prices
    port_value = ports_value.sum(axis=1)
    port_daily_returns = port_value.copy()
    port_daily_returns[1:] = (port_value[1:] / port_value[:-1].values) - 1
    port_daily_returns = port_daily_returns[1:]
    sr = neg_sortino_ratio(allocs, prices) * -1.0
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
        fig.savefig('images/Figure2.png')
  		  	   		 	   		  		  		    	 		 		   		 		  
    return allocs, cr, adr, sddr, sr  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
def neg_sortino_ratio(alloc, data):
    ports_value = alloc*data
    port_value = ports_value.sum(axis=1)  #sum the allocations to get daily value
    port_daily_returns = port_value.copy()
    port_daily_returns[1:] = (port_value[1:] / port_value[:-1].values) - 1 #daily returns formula
    port_daily_returns = port_daily_returns[1:]  #remove the zero value in the start
    k = math.sqrt(252)  #anualized value by day for sharpe ratio
    sum_neg = (port_daily_returns[port_daily_returns < 0].pow(2)).sum()
    std = sum_neg / (len(port_daily_returns)-1)
    std =math.sqrt(std)
    sortino_ratio = k * port_daily_returns.mean() / std
    return sortino_ratio*(-1.0) # need to minimize so multiplying by negative 1

def constrain(x):
    return np.sum(np.abs(x))

def test_code():
    # Call optimize function to save chart for parameters given in assignment instructions
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd=dt.datetime(2008,6,1),
                                                        ed=dt.datetime(2009,6,1),
                                                        syms=['IBM','X','GLD','JPM'], gen_plot=True)
    # Print statistics  		  	   		 	   		  		  		    	 		 		   		 		  
    #print(f"Start Date: {start_date}")
    #print(f"End Date: {end_date}")
    #print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    test_code()  		  	   		 	   		  		  		    	 		 		   		 		  

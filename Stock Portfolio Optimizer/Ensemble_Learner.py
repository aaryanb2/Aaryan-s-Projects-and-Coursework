""""""
import math

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import indicators
import BagLearner as bl
import RTLearner as rt
import scipy.optimize as opt
import datetime as dt  		  	   		 	   		  		  		    	 		 		   		 		  
import random  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		 	   		  		  		    	 		 		   		 		  
import util as ut  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  	  	   		 	   		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		 	   		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		 	   		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    # constructor  		  	   		 	   		  		  		    	 		 		   		 		  
    def __init__(self, impact=0.0, commission=0.0):
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Constructor method  		  	   		 	   		  		  		    	 		 		   		 		  
        """
        self.learner = None
        self.impact = impact  		  	   		 	   		  		  		    	 		 		   		 		  
        self.commission = commission
        self.bench_value = None
        self.portfolio_value = None
        self.num_trades = None

    # this method creates a QLearner, and train it for trading
    def add_evidence(  		  	   		 	   		  		  		    	 		 		   		 		  
        self,  		  	   		 	   		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		 	   		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		 	   		  		  		    	 		 		   		 		  
    ):	 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
        # add your code to do learning here
        new_sd = sd - dt.timedelta(days=5)
        new_ed = ed + dt.timedelta(days=100)
        sym_data = ut.get_data([symbol], dates=pd.date_range(sd, new_ed))
        indic_data = ut.get_data([symbol], dates=pd.date_range(new_sd, ed))
        while sd not in indic_data.index:
            sd = sd + dt.timedelta(days=1)
        new_ind = indic_data.index.get_loc(sd)
        while ed not in indic_data.index:
            ed = ed - dt.timedelta(days=1)
        idx_ed = sym_data.index.get_loc(ed)
        ind_sd = indic_data.index[new_ind - 1]
        sym_data = sym_data[symbol]
        sym_data = sym_data.to_numpy()
        ind1 = indicators.Indicators(lb=20, symbol=symbol, sd=ind_sd, ed=ed)
        b_perc = ind1.bolinger_band_ind()
        ind2 = indicators.Indicators(lb=14, symbol=symbol, sd=ind_sd, ed=ed)
        rsi = ind2.rsi_ind()
        ind4 = indicators.Indicators(symbol=symbol, sd=ind_sd, ed=ed)
        ppo_ind = ind4.ppo_indicator(short_period=9, long_period=17, signal_period=5)
        ind5 = indicators.Indicators(lb=4, symbol=symbol, sd=ind_sd, ed=ed)
        tema = ind5.tema_ind()
        merged_df = pd.concat([b_perc[:-1], rsi[:-1], ppo_ind[:-1], tema[:-1]], axis=1)
        x = merged_df.to_numpy()
        y = np.zeros(idx_ed+1)
        for i in range(idx_ed):
            if i + 4 < idx_ed + 1:
                if (sym_data[i]*(1+self.impact) + self.commission/1000) < sym_data[i+4]:
                    y[i] = 1
                elif (sym_data[i]*(1-self.impact) - self.commission/1000) > sym_data[i+4]:
                    y[i] = -1
            else: # cannot look ahead values outside in-sample data range
                y[i] = y[i-1]
        cutoff = round(0.6*idx_ed)
        train_x = x[:cutoff,:]
        train_y = y[:cutoff]
        test_x = x[cutoff:,:]
        test_y = y[cutoff:]
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": 18}, bags=28, boost=False,
                                     verbose=False)
        self.learner.add_evidence(x, y)


    def optimize_neg_cr(self, leaf, x, y, sv,portvals,symbol):
        self.learner = bl.BagLearner(learner=rt.RTLearner, kwargs={"leaf_size": leaf[0]}, bags=20, boost=False,
                                     verbose=False)
        self.learner.add_evidence(x, y)
        pred_y = self.learner.query(x)
        in_sample_value =np.zeros(len(pred_y))
        current_pos=0
        cash_val = sv
        for i in range(len(pred_y)):
            if pred_y[i] == 1:
                if current_pos == 0:
                    cash_val = cash_val - portvals[symbol][i] * 1000*(1+self.impact) -self.commission
                elif current_pos == -1:
                    cash_val = cash_val - portvals[symbol][i] * 2000*(1+self.impact) -self.commission
                current_pos = 1
            elif pred_y[i] == -1 :
                if current_pos == 0:
                    cash_val = cash_val - portvals[symbol][i] * (-1000)*(1-self.impact) -self.commission
                elif current_pos == 1:
                    cash_val = cash_val - portvals[symbol][i] * (-2000)*(1-self.impact) -self.commission
                current_pos = -1
            in_sample_value[i] = portvals[symbol][i] * current_pos * 1000
            in_sample_value[i] += cash_val
        cr_port = round(in_sample_value[-1] / in_sample_value[0] - 1, 6)

        return cr_port*(-1)

  		  	   		 	   		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		 	   		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		 	   		  		  		    	 		 		   		 		  
        self,  		  	   		 	   		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		 	   		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		 	   		  		  		    	 		 		   		 		  
        sv=10000,
        figa = 1
    ):  		  	   		 	   		  		  		    	 		 		   		 		  
        """  		  	   		 	   		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		 	   		  		  		    	 		 		   		 		    	   		 	   		  		  		    	 		 		   		 		  
        """
        new_sd = sd - dt.timedelta(days=5)
        indic_data = ut.get_data([symbol], dates=pd.date_range(new_sd, ed))
        while sd not in indic_data.index:
            sd = sd + dt.timedelta(days=1)
        new_ind = indic_data.index.get_loc(sd)
        ind_sd = indic_data.index[new_ind - 1]
        ind1 = indicators.Indicators(lb=20, symbol=symbol, sd=ind_sd, ed=ed)
        b_perc = ind1.bolinger_band_ind()
        ind2 = indicators.Indicators(lb=14, symbol=symbol, sd=ind_sd, ed=ed)
        rsi = ind2.rsi_ind()
        ind4 = indicators.Indicators(symbol=symbol, sd=ind_sd, ed=ed)
        ppo_ind = ind4.ppo_indicator(short_period=9, long_period=17, signal_period=5)
        ind5 = indicators.Indicators(lb=4, symbol=symbol, sd=ind_sd, ed=ed)
        tema = ind5.tema_ind()
        merged_df = pd.concat([b_perc[:-1], rsi[:-1], ppo_ind[:-1], tema[:-1]], axis=1)
        x = merged_df.to_numpy()
        pred_y = self.learner.query(x)
        portvals = ut.get_data([symbol], dates=pd.date_range(sd, ed))
        current_pos = 0  # 0 indicates hold, 1 indicates long, -1 indicates short
        in_sample_value = pd.DataFrame(index=portvals.index, data=portvals[symbol])
        cash_val = sv
        b_val = sv - portvals[symbol][0] * 1000
        bench_value = pd.DataFrame(index=portvals.index, data=portvals[symbol])
        df = pd.DataFrame(index=portvals.index, data=portvals[symbol])
        df = df.rename(columns={symbol: "Values"})
        self.num_trades = df
        self.num_trades = self.num_trades.replace(self.num_trades.values, 0)
        for ind in portvals.index:
            i = portvals.index.get_loc(ind)
            if pred_y[i] == 1:
                if current_pos == 0:
                    df.iloc[i] = 1000
                    cash_val = cash_val - portvals[symbol][i] * 1000*(1+self.impact) -self.commission
                elif current_pos == 1:
                    df.iloc[i] = 0.0
                elif current_pos == -1:
                    df.iloc[i] = 2000.0
                    cash_val = cash_val - portvals[symbol][i] * 2000*(1+self.impact) -self.commission
                current_pos = 1
                self.num_trades.iloc[i] = self.num_trades.iloc[i-1] + 1
            elif pred_y[i] == -1 :
                if current_pos == 0:
                    df.iloc[i] = -1000.0
                    cash_val = cash_val - portvals[symbol][i] * (-1000)*(1-self.impact) -self.commission
                elif current_pos == 1:
                    df.iloc[i]= -2000.0
                    cash_val = cash_val - portvals[symbol][i] * (-2000)*(1-self.impact) -self.commission
                elif current_pos == -1:
                    df.iloc[i] = 0.0
                current_pos = -1
                self.num_trades.iloc[i] = self.num_trades.iloc[i - 1] + 1
            else:
                df.iloc[i] = 0
                self.num_trades.iloc[i] = self.num_trades.iloc[i - 1]

            bench_value.iloc[i] = portvals[symbol][i] * 1000 + b_val
            in_sample_value.iloc[i] = portvals[symbol][i] * current_pos * 1000
            in_sample_value.iloc[i] += cash_val
        in_sample_value = in_sample_value / in_sample_value.iloc[0]
        bench_value = bench_value / bench_value.iloc[0]
        self.portfolio_value = in_sample_value
        self.bench_value = bench_value
        return df
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    # np.random.seed(903310070)
    # m = StrategyLearner(commission=9.95, impact=0.005)
    # a = m.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # b = m.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000, figa=0)
    # #c = m.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000, figa=1)
    pass


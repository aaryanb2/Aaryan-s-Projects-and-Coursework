import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import Ensemble_Learner as sl
import datetime as dt



def main():
    symbol = "JPM"
    low_imp = sl.StrategyLearner(commission=0, impact=0)
    low_imp.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    a = low_imp.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    med_imp = sl.StrategyLearner(commission=0, impact=0.01)
    med_imp.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    b = med_imp.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    high_imp = sl.StrategyLearner(commission=0, impact=0.02)
    high_imp.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    c = high_imp.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    v_med_imp = sl.StrategyLearner(commission=0, impact=0.015)
    v_med_imp.add_evidence(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    d = v_med_imp.testPolicy(symbol=symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)


    # Strategy Learner Chart with varying impact for daily port value
    fig, ax = plt.subplots()
    ax.plot(low_imp.portfolio_value.index, low_imp.portfolio_value[symbol], color="red",
            label="Impact=0")
    ax.plot(med_imp.portfolio_value.index, med_imp.portfolio_value[symbol], color="purple",
            label="Impact=0.01")
    ax.plot(v_med_imp.portfolio_value.index, v_med_imp.portfolio_value[symbol], color="black",
            label="Impact=0.015")
    ax.plot(high_imp.portfolio_value.index, high_imp.portfolio_value[symbol], color="green",
            label="Impact=0.02")

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Portfolio Value")
    ax.margins(x=0)
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.tick_params(axis='both', which='minor', labelsize=6)
    plt.grid()
    plt.title("Strategy Learner Daily Portfolio Value with Impact")
    plt.legend(loc="upper left")
    fig = ax.get_figure()
    fig.set_size_inches(14, 6)
    fig.tight_layout()
    fig.savefig('images/Portfolio_outlook.png')



if __name__ == "__main__":
    main()

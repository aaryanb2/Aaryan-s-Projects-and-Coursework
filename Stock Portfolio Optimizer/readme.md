📈 Stock Portfolio Optimizer
This project builds a machine learning-based trading strategy that selects optimal stock allocations based on historical performance, volatility, volume, and macroeconomic metrics. It applies custom learners including Bagging, Regression Trees, and Q-Learning to maximize risk-adjusted returns.

🧠 Key Features
Feature engineering from historical stock price, volume, and economic indicators

Custom ML algorithms:

BagLearner (ensemble)

Regression Tree Learner

Q-Learning agent for sequential portfolio decisions

Risk evaluation using Sharpe and Sortino Ratios

Benchmark comparison against traditional market portfolios

🚀 How to Run
Clone this repository

Portfolio Optimization (Multi-Stock Allocation)

Run optimization.py and input desired stock symbols

This script calculates optimal allocations based on Sharpe and Sortino Ratios

Results are saved in p3_results.txt

bash
Copy
Edit
python optimization.py
ML Strategy Performance (Single Stock)

Run prediction_model_runner.py with one stock symbol to evaluate an ML-based strategy

Uses a BagLearner + Q-Learner combination to model and simulate performance

Outputs include performance plots over test periods

bash
Copy
Edit
python prediction_model_runner.py
Dependencies

Python 3.x, NumPy, Pandas, Matplotlib (add others if needed)

📊 Results
Optimization script identifies optimal allocations across stocks that yield higher Sharpe/Sortino ratios vs. naive allocations

Prediction model shows strong generalization using custom ensemble + reinforcement learning approach

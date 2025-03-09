Mutual Fund Plan

This repository contains a Python-based mutual fund planning script that analyzes stock market data to create a portfolio with high returns and low risk. It utilizes stock price trends, volatility, return on investment (ROI), and various investment strategies to construct an optimized mutual fund plan.

Features

Stock Price Analysis: Reads and processes stock market data (Nifty50 closing prices).
Data Cleaning & Preprocessing: Handles missing values using forward-fill.
Stock Trend Visualization: Uses Plotly to generate interactive stock price trend charts.

Volatility and ROI Calculation:

Computes standard deviation as a measure of stock volatility.
Calculates ROI based on initial and final stock prices.
Mutual Fund Plan Construction:
Selects companies with high ROI and low volatility.
Assigns investment ratios based on inverse volatility.
Investment Growth Projection:
Computes future investment value over various periods.
Compares mutual fund risk and ROI against high-growth companies.

Technologies Used

Python: Core programming language
Pandas: Data manipulation and analysis
Plotly: Data visualization and interactive graphs
NumPy: Numerical computations

KEY FEATURES

1. Data Handling

pd.read_csv() – Reads stock price data.
pd.to_datetime() – Converts date column to datetime format.
fillna(method='ffill') – Handles missing values using forward fill.

2. Statistical Computations

std() – Computes standard deviation (volatility measure).
pct_change() – Calculates percentage change in stock prices.
ROI calculation: (final_price - initial_price) / initial_price * 100

3. Mutual Fund Strategy Implementation

Selecting companies based on ROI & volatility thresholds.
Assigning investment ratios using inverse volatility.

4. Data Visualization (Plotly)

go.Scatter() – Line chart for stock trends.
go.Bar() – Bar chart for comparing risk and ROI.

5. Investment Growth Calculation

Future value formula:
def future_value(P, r, n, t):
    return P * (((1 + r/n)**(n*t) - 1) / (r/n)) * (1 + r/n)

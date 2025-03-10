# -*- coding: utf-8 -*-
"""MUTUAL FUND PLAN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H6jlalpLjhC7ElOqYYpnsbE6MofkbG1m
"""

import pandas as pd
data = pd.read_csv("nifty50_closing_prices.csv")
print(data.head())

#Converting the date column into a datetime data type
data['Date'] = pd.to_datetime(data['Date'])

print(data.isnull().sum())

#Filling the missing values using forward fill
data.fillna(method='ffill', inplace=True)

# Stock price trend visualisation for the companies
import plotly.graph_objs as go
import plotly.express as px

fig = go.Figure()

for company in data.columns[1:]:
    fig.add_trace(go.Scatter(x=data['Date'], y=data[company],
                             mode='lines',
                             name=company,
                             opacity=0.5))

fig.update_layout(
    title='Stock Price Trends of All Indian Companies',
    xaxis_title='Date',
    yaxis_title='Closing Price (INR)',
    xaxis=dict(tickangle=45),
    legend=dict(
        x=1.05,
        y=1,
        traceorder="normal",
        font=dict(size=10),
        orientation="v"
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode='x',
    template='plotly_white'
)
fig.show()

#Top 10 companies with the highest risks for investing, this reflects the volatility associated with the stock
all_companies = data.columns[1:]

volatility_all_companies = data[all_companies].std()
volatility_all_companies.sort_values(ascending=False).head(10)

# Top 10 companies with the highest growth rate
growth_all_companies = data[all_companies].pct_change() * 100

average_growth_all_companies = growth_all_companies.mean()
average_growth_all_companies.sort_values(ascending=False).head(10)

#Finding ROI fro the companies
initial_prices_all = data[all_companies].iloc[0]
final_prices_all = data[all_companies].iloc[-1]

roi_all_companies = ((final_prices_all - initial_prices_all) / initial_prices_all) * 100
roi_all_companies.sort_values(ascending=False).head(10)

"""**Creating a Mutual Fund Plan Based on High ROI and Low Risk**

To create a strategy for selecting companies with high ROI and low risk, we can use a combination of ROI and volatility (standard deviation) metrics. The goal is to find companies that offer a high return on investment (ROI) but with low volatility to minimize risk.

STEPS TO CREATE A MUTUAL FUND PLAN

1) Define ROI and Volatility Thresholds: We will set thresholds for ROI and volatility to select companies that provide good returns with lower risks.

2) Rank Companies by ROI and Volatility: Rank all companies based on their ROI and volatility scores.

3) Assign Investment Ratios: Allocate more investment to companies with higher ROI and lower volatility.
"""

# Defining thresholds and selecting companies meeting the criteria
roi_threshold = roi_all_companies.median()
volatility_threshold = volatility_all_companies.median()

selected_companies = roi_all_companies[(roi_all_companies > roi_threshold) & (volatility_all_companies < volatility_threshold)]

selected_companies.sort_values(ascending=False)

selected_volatility = volatility_all_companies[selected_companies.index]
inverse_volatility = 1 / selected_volatility

investment_ratios = inverse_volatility / inverse_volatility.sum()

investment_ratios.sort_values(ascending=False)

"""ANALYSING OUR MUTUAL FUND PLAN:
Now, let’s analyze and compare our mutual fund plan by comparing it with the high-performing companies in the stock market. Let’s start by comparing the risks in our mutual fund with the risk in the high growth companies
"""

top_growth_companies = average_growth_all_companies.sort_values(ascending=False).head(10)
risk_growth_rate_companies = volatility_all_companies[top_growth_companies.index]
risk_mutual_fund_companies = volatility_all_companies[selected_companies.index]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=risk_mutual_fund_companies.index,
    x=risk_mutual_fund_companies,
    orientation='h',  # Horizontal bar
    name='Mutual Fund Companies',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=risk_growth_rate_companies.index,
    x=risk_growth_rate_companies,
    orientation='h',
    name='Growth Rate Companies',
    marker=dict(color='green'),
    opacity=0.7
))

fig.update_layout(
    title='Risk Comparison: Mutual Fund vs Growth Rate Companies',
    xaxis_title='Volatility (Standard Deviation)',
    yaxis_title='Companies',
    barmode='overlay',
    legend=dict(title='Company Type'),
    template='plotly_white'
)

fig.show()

"""Comparing the ROI of both the groups."""

expected_roi_mutual_fund = roi_all_companies[selected_companies.index]

expected_roi_growth_companies = roi_all_companies[top_growth_companies.index]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=expected_roi_mutual_fund.index,
    x=expected_roi_mutual_fund,
    orientation='h',
    name='Mutual Fund Companies',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=expected_roi_growth_companies.index,
    x=expected_roi_growth_companies,
    orientation='h',
    name='Growth Rate Companies',
    marker=dict(color='green'),
    opacity=0.7
))

fig.update_layout(
    title='Expected ROI Comparison: Mutual Fund vs Growth Rate Companies',
    xaxis_title='Expected ROI (%)',
    yaxis_title='Companies',
    barmode='overlay',
    legend=dict(title='Company Type'),
    template='plotly_white'
)

fig.show()

"""The comparison between the risk (volatility) and expected ROI for mutual fund companies (in blue) and growth rate companies (in green) shows a clear trade-off. Mutual fund companies offer lower volatility, meaning they are less risky, but also provide lower expected returns. In contrast, growth rate companies demonstrate higher volatility, indicating more risk, but they offer much higher potential returns, especially companies like Bajaj Auto and Bajaj Finserv. This highlights a common investment dilemma: lower risk comes with a lower reward, while higher risk could yield higher returns.

For long-term investments, the goal is typically to find companies that offer a balance of stable returns and manageable risk. The companies in our mutual fund exhibit low volatility, meaning they are less risky, and their moderate returns make them solid choices for long-term, stable growth. They are well-suited for conservative investors who want steady returns without significant fluctuations in value.

Now, let’s calculate the expected returns a person will get from our mutual fund if he/she invests ₹5000 every month.

To calculate the expected value a person will accumulate over 1 year, 3 years, 5 years, and 10 years through the mutual fund plan
"""

import numpy as np

monthly_investment = 5000  # Monthly investment in INR
years = [1, 3, 5, 10,20,50]  # Investment periods (in years)
n = 12  # Number of times interest is compounded per year (monthly)

avg_roi = expected_roi_mutual_fund.mean() / 100  # Convert to decimal

def future_value(P, r, n, t):
    return P * (((1 + r/n)**(n*t) - 1) / (r/n)) * (1 + r/n)

future_values = [future_value(monthly_investment, avg_roi, n, t) for t in years]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[str(year) + " year" for year in years],
    y=future_values,
    mode='lines+markers',
    line=dict(color='blue'),
    marker=dict(size=8),
    name='Future Value'
))

fig.update_layout(
    title="Expected Value of Investments of ₹ 5000 Per Month (Mutual Funds)",
    xaxis_title="Investment Period",
    yaxis_title="Future Value (INR)",
    xaxis=dict(showgrid=True, gridcolor='lightgrey'),
    yaxis=dict(showgrid=True, gridcolor='lightgrey'),
    template="plotly_white",
    hovermode='x'
)

fig.show()
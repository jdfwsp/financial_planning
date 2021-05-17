#!/usr/bin/env python
# coding: utf-8

# # Unit 5 - Financial Planning
# 

# In[1]:


# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation
import matplotlib.pyplot as plt
from datetime import date, timedelta

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Declare datetime variables
today = date.today().isoformat()
five_yrs_ago = (date.today() - timedelta(days = 5 * 365)).isoformat()

# Print datetime variables 
print(today)
print(five_yrs_ago)


# In[3]:


# Declare variable for outputting report
final_rpt = []


# In[4]:


# Load .env enviroment variables
load_dotenv()


# ## Part 1 - Personal Finance Planner

# ### Collect Crypto Prices Using the `requests` Library

# In[5]:


# Set current amount of crypto assets
my_btc = 1.2
my_eth = 5.3


# In[6]:


# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=USD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=USD"


# In[7]:


# Fetch current BTC price
btc_data = requests.get(btc_url).json()
btc_price = btc_data['data']['1']['quotes']['USD']['price']

# Fetch current ETH price
eth_data = requests.get(eth_url).json()
eth_price = eth_data['data']['1027']['quotes']['USD']['price']

# Compute current value of my crpto
my_btc_value = my_btc * btc_price
my_eth_value = my_eth * eth_price
my_crypto_total = my_btc_value + my_eth_value

# Print current crypto wallet balance

btc_val_rpt = (f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}  ")
eth_val_rpt = (f"The current value of your {my_eth} ETH is ${my_eth_value:0.2f}  ")
crypto_total_rpt = (f"The total value of your crypto portfolio is ${my_crypto_total:0.2f}  ")

crypto_rpt = [btc_val_rpt, eth_val_rpt, crypto_total_rpt]
final_rpt.append(crypto_rpt)
for i in crypto_rpt:
    print(i)


# ### Collect Investments Data Using Alpaca: `SPY` (stocks) and `AGG` (bonds)

# In[8]:


# Current amount of shares
my_agg = 200
my_spy = 50


# In[9]:


# Set Alpaca API key and secret
alpaca_key = os.getenv('ALPACA_API_KEY')
alpaca_secret = os.getenv('ALPACA_API_SECRET')

# Create the Alpaca API object
alpaca = tradeapi.REST(alpaca_key, alpaca_secret, api_version = "v2")


# In[10]:


# Format current date as ISO format

# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"

# Get current closing prices for SPY and AGG
start = pd.Timestamp('2021-05-14', tz = 'US/Pacific').isoformat()
end = pd.Timestamp('2021-05-14', tz = 'US/Pacific').isoformat()
spy_agg = alpaca.get_barset(tickers, timeframe, start = start, end = end).df

# Preview DataFrame
spy_agg


# In[11]:


# Pick AGG and SPY close prices
agg_close_price = spy_agg.iloc[0, 3]
spy_close_price = spy_agg.iloc[0, 8]

# Print AGG and SPY close prices
agg_close_rpt = (f"Current AGG closing price: ${agg_close_price:0.2f}")
spy_close_rpt = (f"Current SPY closing price: ${spy_close_price:0.2f}")

stock_price_rpt = [agg_close_rpt, spy_close_rpt]
final_rpt.append(stock_price_rpt)
for i in stock_price_rpt:
    print(i)


# In[12]:


# Compute the current value of shares
my_spy_value = my_spy * spy_close_price
my_agg_value = my_agg * agg_close_price
my_stocks_total = my_agg_value + my_spy_value

# Print current value of share
my_spy_rpt = (f"The current value of your {my_spy} SPY shares is ${my_spy_value:0.2f}")
my_agg_rpt = (f"The current value of your {my_agg} AGG shares is ${my_agg_value:0.2f}")
my_shares_rpt = (f"The total value of your stocks is ${my_stocks_total:0.2f}")

shares_rpt = [my_agg_rpt, my_spy_rpt, my_shares_rpt]
final_rpt.append(shares_rpt)
for i in shares_rpt:
    print(i)


# ### Savings Health Analysis

# In[13]:


# Set monthly household income
monthly_income = 12000
# Create savings DataFrame
savings_data = [{'Savings': my_crypto_total}, {'Savings': my_stocks_total}]
df_savings = pd.DataFrame(savings_data, index = ['Crypto', 'Stocks'])
total_savings = my_crypto_total + my_stocks_total
# Display savings DataFrame
display(df_savings)
print(total_savings)


# In[14]:


# Plot savings pie chart
df_savings.plot.pie(y = 'Savings', figsize = (8, 8))
plt.savefig('Images/pie.png')
pie_rpt = (f'You have a total of ${total_savings:0.2f} in savings')
pct_crypto_rpt = (f'{((my_crypto_total / total_savings) * 100):0.0f}% of your savings is in crypto-currency')
pct_stocks_rpt = (f'{((my_stocks_total / total_savings) * 100):0.0f}% of your savings is in stocks & bonds')
savings_rpt = [pie_rpt, pct_crypto_rpt, pct_stocks_rpt]
for i in savings_rpt:
    print(i)


# In[15]:


# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
savings_total = my_crypto_total + my_stocks_total

# Validate saving health
if savings_total >= emergency_fund:
    savings_eval = ('Congratulations, you have more than 3 months income in your savings!')
else:
    savings_eval = (f'You need to increase your savings by ${emergency_fund - savings_total} as soon as possible!')
print(savings_eval)
savings_rpt.append(savings_eval)
final_rpt.append(savings_rpt)


# ## Part 2 - Retirement Planning
# 
# ### Monte Carlo Simulation

# In[16]:


# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
start_date = pd.Timestamp(five_yrs_ago, tz='America/New_York').isoformat()
end_date = pd.Timestamp(today, tz='America/New_York').isoformat()


# In[17]:


# Get 5 years' worth of historical data for SPY and AGG
# YOUR CODE HERE!
timeframe = '1D'
df_stock_data = alpaca.get_barset(tickers, timeframe, start = start_date, end = end_date, limit = 1000).df

# Display sample data
df_stock_data.sample(5)

# Use the Alpaca API to fetch five years historical closing prices for a traditional 40/60 portfolio using the SPY and AGG tickers to represent the 60% stocks (SPY) and 40% bonds (AGG) composition of the portfolio. Make sure to convert the API output to a DataFrame and preview the output.


# Configure and execute a Monte Carlo Simulation of 500 runs and 30 years for the 40/60 portfolio.


# Plot the simulation results and the probability distribution/confidence intervals.
# In[18]:


# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns
mc_sim_30 = MCSimulation(df_stock_data, [.4, .6], 500, 252 * 30)


# In[19]:


# Printing the simulation input data
df_stock_data


# In[20]:


# Running a Monte Carlo simulation to forecast 30 years cumulative returns
mc_sim_30.calc_cumulative_return()


# In[21]:


# Plot simulation outcomes
mc_sim_30.plot_simulation()
plt.savefig('Images/sim_returns_30.png')


# In[22]:


# Plot probability distribution and confidence intervals
mc_sim_30.plot_distribution()
plt.savefig('Images/dist_returns_30.png')


# ### Retirement Analysis

# In[23]:


# Fetch summary statistics from the Monte Carlo simulation results
my_sim_summary = mc_sim_30.summarize_cumulative_return()

# Print summary statistics
print(my_sim_summary)


# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a `$20,000` initial investment.

# In[24]:


# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
ci_lower = round(my_sim_summary.loc['95% CI Lower'] * initial_investment, 2)
ci_upper = round(my_sim_summary.loc['95% CI Upper'] * initial_investment, 2)
# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within the range of"
      f" ${ci_lower} and ${ci_upper}")


# ### Calculate the expected portfolio return at the `95%` lower and upper confidence intervals based on a `50%` increase in the initial investment.

# In[25]:


# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000
ci_lower = round(my_sim_summary.loc['95% CI Lower'] * initial_investment, 2)
ci_upper = round(my_sim_summary.loc['95% CI Upper'] * initial_investment, 2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within the range of"
      f" ${ci_lower} and ${ci_upper}")


# ## Optional Challenge - Early Retirement
# 
# 
# ### Five Years Retirement Option

# In[26]:


# Configuring a Monte Carlo simulation to forecast 5 years cumulative returns
mc_sim_5 = MCSimulation(df_stock_data, [.1, .9], 500, 252 * 5)


# In[27]:


# Running a Monte Carlo simulation to forecast 5 years cumulative returns
mc_sim_5.calc_cumulative_return()


# In[28]:


# Plot simulation outcomes
mc_sim_5.plot_simulation()
plt.savefig('Images/sim_returns_5.png')


# In[29]:


# Plot probability distribution and confidence intervals
mc_sim_5.plot_distribution()
plt.savefig('Images/dist_returns_5.png')


# In[30]:


# Fetch summary statistics from the Monte Carlo simulation results
my_sim_5_summary = mc_sim_5.summarize_cumulative_return()

# Print summary statistics
print(my_sim_5_summary)


# In[31]:


# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_five = round(my_sim_5_summary.loc['95% CI Lower'] * initial_investment, 2)
ci_upper_five = round(my_sim_5_summary.loc['95% CI Upper'] * initial_investment, 2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 5 years will end within the range of"
      f" ${ci_lower_five} and ${ci_upper_five}")


# ### Ten Years Retirement Option

# In[32]:


# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
mc_sim_10 = MCSimulation(df_stock_data, [.1, .9], 500, 252 * 10)


# In[33]:


# Running a Monte Carlo simulation to forecast 10 years cumulative returns
mc_sim_10.calc_cumulative_return()


# In[34]:


# Plot simulation outcomes
mc_sim_10.plot_simulation()
plt.savefig('Images/sim_returns_10.png')


# In[35]:


# Plot probability distribution and confidence intervals
mc_sim_10.plot_distribution()
plt.savefig('Images/dist_returns_10.png')


# In[36]:


# Fetch summary statistics from the Monte Carlo simulation results
my_sim_10_summary = mc_sim_10.summarize_cumulative_return()

# Print summary statistics
print(my_sim_10_summary)


# In[37]:


# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000
ci_lower_ten = round(my_sim_10_summary.loc['95% CI Lower'] * initial_investment, 2)
ci_upper_ten = round(my_sim_10_summary.loc['95% CI Upper'] * initial_investment, 2)

# Print result
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 10 years will end within the range of"
      f" ${ci_lower_ten} and ${ci_upper_ten}")


# In[39]:


# Find initial investment needed to achieve mean return of 30 year investment

# Declare variable with value of original retire-at-30 years analysis mean
thirty_yr_mean = my_sim_summary.loc['mean'] * initial_investment

# Declare variabls for simulated 5 & 10 year means
mean_five = my_sim_5_summary.loc['mean']
mean_ten = my_sim_10_summary.loc['mean']

# Define a function that accepts simulated mean and targeted return
# Returns initial investment needed to reach target
def find_initial_investment(mean, target):
    i = 0
    while (i * mean) < target:
        i += 1000
    
    return i

# Run function on simulated 5 & 10 year means
five_investment = find_initial_investment(mean_five, thirty_yr_mean)
ten_investment = find_initial_investment(mean_ten, thirty_yr_mean)

# Explain the findings
print(f'The mean return on ${initial_investment} invested for 30 years is ${thirty_yr_mean:0.2f}.')
print(f'In order to achieve the same mean investment in 10 years, you need to invest ${ten_investment:0.2f}.')
print(f'The amount increases to ${five_investment:0.2f} if you expect that mean return in only 5 years.')


# In[ ]:





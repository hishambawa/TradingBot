import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as time

from trading_env import TradingEnvironment

pd.options.mode.chained_assignment = None

df = pd.read_csv('data.csv')

# Get the simple moving averages
def get_sma(prices, rate):
    return prices.rolling(rate).mean()

# Generate the bollinger bands
def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate)      # Get SMA for 20 days
    std = prices.rolling(rate).std() # Get rolling standard deviation for 20 days

    bollinger_up = sma + std * 2
    bollinger_down = sma - std * 2

    return bollinger_up, bollinger_down

symbols = ['A', 'AAPL', 'FB', 'GOOG']

for symbol in symbols:

    # Convert the price column of the dataframe to float values
    df[f'{symbol}_price'] = df[f'{symbol}_price'].astype(float)

    # Generate the bollinger bands
    df[f'{symbol}_upper_band'], df[f'{symbol}_lower_band'] = get_bollinger_bands(df[f'{symbol}_price'])

# Remove the missing values
df.dropna(inplace=True)

print("Running")

##############################################################################################

start_funds = 100
balance =     100
balance_unit = "LKR"

env = TradingEnvironment(balance, symbols)

for i in range(len(df)):
    if env.balance_unit == 'LKR':
        
        for symbol in symbols:
            if env.bottoms[symbol] == 'hit' and df[f'{symbol}_price'].iloc[i] > df[f'{symbol}_lower_band'].iloc[i]:
                env.bottoms[symbol] = 'released'
            if df[f'{symbol}_price'].iloc[i] < df[f'{symbol}_lower_band'].iloc[i]: #buy signal
                if env.bottoms[symbol] == 'released':
                    env.buy(symbol, df[f'{symbol}_price'].iloc[i], df['datetime'].iloc[i])
                    env.reset_bottoms()
                    print(f'Buying at {df[f"{symbol}_price"].iloc[i]}')
                    break
                else:
                    env.bottoms[symbol] = 'hit'
                
    if env.balance_unit != 'LKR':

        if env.tops[env.balance_unit] == 'hit' and (df[f'{env.balance_unit}_price'].iloc[i] < df[f'{env.balance_unit}_upper_band'].iloc[i]):
            env.tops[env.balance_unit] = 'released'
            
        if df[f'{env.balance_unit}_price'].iloc[i] > df[f'{env.balance_unit}_upper_band'].iloc[i]: #sell signal
            if env.tops[env.balance_unit] == 'released':
                env.sell(df[f'{env.balance_unit}_price'].iloc[i], df['datetime'].iloc[i])
                env.reset_tops()
                print(f'Selling at {df[f"{symbol}_price"].iloc[i]}')

            else:
                env.tops[env.balance_unit] = 'hit'

        # mimic the time taken to update the dataframe. This value is ideally the time gap between the stocks used in the dataset (5 mins in the current dataset)
        time.sleep(0.01)

if env.balance_unit != 'LKR':
    env.sell(env.stock_buys[-1][2], df['datetime'].iloc[-1])
    print(f'Selling at the end of the dataset {env.stock_buys[-1][2]}')

print("\nEnd of dataset...\n") 

print(f"Profit/Loss: {round((env.balance - start_funds), 2)}\n")
  
# print(env.stock_buys)
# print(env.stock_sells)

##############################################################################################

# Testing
def show_plot(symbol):
    plt.title(symbol + ' Bollinger Bands')
    plt.xlabel('Days')
    plt.ylabel('Closing Prices')
    plt.plot(df[f'{symbol}_price'], label='Closing Prices')
    plt.plot(df[f'{symbol}_upper_band'], label='Bollinger Up', c='g')
    plt.plot(df[f'{symbol}_lower_band'], label='Bollinger Down', c='r')

    plt.legend()
    plt.show()

# show_plot('AAPL')
# show_plot('GOOG')
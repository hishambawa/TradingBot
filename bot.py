import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


pd.options.mode.chained_assignment = None

df = pd.read_csv('data.csv')

symbol = "HNB"

# Select the rows in the dataframe that contains the selected symbol
df_selected = df.loc[df['symbol'] == symbol]

# Convert the price column of the dataframe to float values
df_selected['price'] = df_selected['price'].astype(float)


df_selected.index = np.arange(df_selected.shape[0])

# Get the simple moving averages
def get_sma(prices, rate):
    return prices.rolling(rate).mean()

def get_bollinger_bands(prices, rate=20):
    sma = get_sma(prices, rate) # <-- Get SMA for 20 days
    std = prices.rolling(rate).std() # <-- Get rolling standard deviation for 20 days

    bollinger_up = sma + std * 2
    bollinger_down = sma - std * 2

    return bollinger_up, bollinger_down

prices = df_selected['price']

df_selected['bollinger_up'], df_selected['bollinger_down'] = get_bollinger_bands(prices)

print("Running")

##############################################################################################

start_funds = 10000
balance = 10000
balance_unit = "LKR"
buys = []
sells = []

for i in range(len(df_selected)):

    if balance_unit == "LKR" and df_selected['price'].iloc[i] < df_selected['bollinger_down'].iloc[i]: #buy signal    
        balance_unit = symbol
    
        balance = balance / df_selected['price'].iloc[i]
        buys.append([df_selected['date'].iloc[i], df_selected['price'].iloc[i]])

        buy_price = df_selected['price'].iloc[i]

        print(f"Buying at {df_selected['price'].iloc[i]}. Bollinger band is at {df_selected['bollinger_down'].iloc[i]}")

    if balance_unit != "LKR" and (df_selected['price'].iloc[i] > df_selected['bollinger_up'].iloc[i]):   #sell sginal
        balance_unit = "LKR"

        balance = balance * df_selected['price'].iloc[i]
        sells.append([df_selected['date'].iloc[i], df_selected['price'].iloc[i]])

        print(f"Selling at {df_selected['price'].iloc[i]}. Bollinger band is at {df_selected['bollinger_up'].iloc[i]}")

print("End of dataset...\n") 

print(f"Profit/Loss: {math.floor(balance - start_funds)}\n")
  
print(buys)
print(sells)

##############################################################################################

# Testing
plt.title(symbol + ' Bollinger Bands')
plt.xlabel('Days')
plt.ylabel('Closing Prices')
plt.plot(prices, label='Closing Prices')
plt.plot(df_selected['bollinger_up'], label='Bollinger Up', c='g')
plt.plot(df_selected['bollinger_down'], label='Bollinger Down', c='r')
plt.legend()
plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

df = pd.read_csv('data.csv')

symbol = "ABAN"

# Select the rows in the dataframe that contains the selected symbol
df_selected = df.loc[df['symbol'] == symbol]

# Convert the price column of the dataframe to float values
df_selected['price'] = df_selected['price'].astype(float)

#
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
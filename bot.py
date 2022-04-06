import threading
import pandas as pd
import matplotlib.pyplot as plt
import time as time

from trading_env import TradingEnvironment

pd.options.mode.chained_assignment = None

class Bot:
    def __init__(self, user, balance, symbols):
        self.balance = balance
        self.symbols = symbols
        self.prices = {}
        self.env = TradingEnvironment(balance, symbols)

        self.user = user
        self.running = False
        
    # Get the simple moving averages
    def get_sma(self, prices, rate):
        return prices.rolling(rate).mean()

    # Generate the bollinger bands
    def get_bollinger_bands(self, prices, rate=20):
        sma = self.get_sma(prices, rate)      # Get SMA for 20 days
        std = prices.rolling(rate).std()      # Get the standard deviation for 20 days

        bollinger_up = sma + std * 2
        bollinger_down = sma - std * 2

        return bollinger_up, bollinger_down

    def run(self):
        self.running = True
        df = pd.read_csv('data.csv')

        for symbol in self.symbols:

            # Convert the price column of the dataframe to float values
            df[f'{symbol}_price'] = df[f'{symbol}_price'].astype(float)

            # Generate the bollinger bands
            df[f'{symbol}_upper_band'], df[f'{symbol}_lower_band'] = self.get_bollinger_bands(df[f'{symbol}_price'])

        # Remove the missing values
        df.dropna(inplace=True)

        print(f"Running {self.user}")
        ##############################################################################################

        start_funds = self.balance

        for i in range(len(df)):
            if self.env.balance_unit == 'LKR':
                
                for symbol in self.symbols:
                    if self.env.bottoms[symbol] == 'hit' and df[f'{symbol}_price'].iloc[i] > df[f'{symbol}_lower_band'].iloc[i]:
                        self.env.bottoms[symbol] = 'released'
                    if df[f'{symbol}_price'].iloc[i] < df[f'{symbol}_lower_band'].iloc[i] and self.env.balance >= df[f'{symbol}_price'].iloc[i]: #buy signal # check if the user can afford atleast 1 share
                        if self.env.bottoms[symbol] == 'released': 
                            self.env.buy(symbol, df[f'{symbol}_price'].iloc[i], df['datetime'].iloc[i])
                            self.env.reset_bottoms()
                            print(f'Buying {self.env.balance} stocks at {df[f"{symbol}_price"].iloc[i]}. Balance is {self.env.currency_balance}')
                            break
                        else:
                            self.env.bottoms[symbol] = 'hit'
                        
            if self.env.balance_unit != 'LKR':

                if self.env.tops[self.env.balance_unit] == 'hit' and (df[f'{self.env.balance_unit}_price'].iloc[i] < df[f'{self.env.balance_unit}_upper_band'].iloc[i]):
                    self.env.tops[self.env.balance_unit] = 'released'
                    
                if df[f'{self.env.balance_unit}_price'].iloc[i] > df[f'{self.env.balance_unit}_upper_band'].iloc[i]: #sell signal
                    if self.env.tops[self.env.balance_unit] == 'released':
                        print(f'Selling {self.env.balance} of {self.env.balance_unit} stocks at {df[f"{symbol}_price"].iloc[i]}')
                        self.env.sell(df[f'{self.env.balance_unit}_price'].iloc[i], df['datetime'].iloc[i])
                        self.env.reset_tops()

                    else:
                        self.env.tops[self.env.balance_unit] = 'hit'

                # mimic the time taken to update the dataframe. This value is ideally the time gap between the stocks used in the dataset (5 mins in the current dataset)
                time.sleep(0.2)

        if self.env.balance_unit != 'LKR':
            self.env.sell(self.env.stock_buys[-1][3], df['datetime'].iloc[-1])
            print(f'Selling at the end of the dataset at {self.env.stock_buys[-1][3]}')

        print("\nEnd of dataset...\n") 

        print(f"Profit/Loss: {round((self.env.balance - start_funds), 2)}\n")

        print("Finishing...")
        time.sleep(1)
        
        # print(env.stock_buys)
        # print(env.stock_sells)

        # self.show_plot(df, 'TSLA')
        # show_plot(df, 'GOOG')

        ##############################################################################################

    # Testing
    def show_plot(self, df, symbol):
        plt.title(symbol + ' Bollinger Bands')
        plt.xlabel('Days')
        plt.ylabel('Closing Prices')
        plt.plot(df[f'{symbol}_price'], label='Closing Prices')
        plt.plot(df[f'{symbol}_upper_band'], label='Bollinger Up', c='g')
        plt.plot(df[f'{symbol}_lower_band'], label='Bollinger Down', c='r')

        plt.legend()
        plt.show()

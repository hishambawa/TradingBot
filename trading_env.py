class TradingEnvironment:
    def __init__(self, balance, symbols):
        self.balance = balance
        self.balance_unit = "LKR"

        self.data = []

        self.currency_balance = balance

        self.symbols = symbols

        self.bottoms = {}
        self.reset_bottoms()
        
        self.tops = {}
        self.reset_tops()

    def buy(self, symbol, buy_price, time):
        self.balance_unit = symbol

        self.balance = int(self.balance / buy_price) # number of stocks purchased

        stock_value = self.balance * buy_price
        self.currency_balance = self.currency_balance - stock_value #  update the left over money when buying stocks
        
        data = {
            'action': 'buy',
            'symbol': symbol,
            'time': time,
            'value': stock_value,
            'price': buy_price,
            'quantity': self.balance,
            'running': True
        }

        self.data.append(data)

    def sell(self, sell_price, time):
        sell_value = self.balance * sell_price
        self.currency_balance = sell_value + self.currency_balance

        data = {
            'action': 'sell',
            'symbol': self.balance_unit,
            'time': time,
            'value': sell_value,
            'price': sell_price,
            'quantity': self.balance,
            'running': True
        }

        self.data.append(data)
        self.balance_unit = "LKR"
        self.balance = self.currency_balance

    def reset_bottoms(self):
        for symbol in self.symbols:
            self.bottoms[symbol] = 'none'
        
    def reset_tops(self):
        for symbol in self.symbols:
            self.tops[symbol] = 'none'

    def finish(self):
        self.data.append({'running': False})
class TradingEnvironment:
    def __init__(self, balance, symbols):
        self.balance = balance
        self.stock_buys = []
        self.stock_sells = []
        self.balance_unit = "LKR"

        self.currency_balance = balance

        self.symbols = symbols

        self.bottoms = {}
        self.reset_bottoms()
        
        self.tops = {}
        self.reset_tops()

    def buy(self, symbol, buy_price, time):
        self.balance_unit = symbol

        quantity = int(self.balance / buy_price)

        self.balance = quantity # number of stocks purchased

        stock_value = quantity * buy_price
        self.currency_balance = self.currency_balance - stock_value #  update the left over money when buying stocks
        
        self.stock_buys.append([symbol, time, stock_value, buy_price, quantity])

    def sell(self, sell_price, time):
        self.balance_unit = "LKR"

        sell_value = self.balance * sell_price
        quantity = self.balance

        self.balance = (self.balance * sell_price) + self.currency_balance
        self.currency_balance = self.balance

        self.stock_sells.append([self.balance_unit, time, sell_value, sell_price, quantity])

    def reset_bottoms(self):
        for symbol in self.symbols:
            self.bottoms[symbol] = 'none'
        
    def reset_tops(self):
        for symbol in self.symbols:
            self.tops[symbol] = 'none'
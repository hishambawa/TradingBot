class TradingEnvironment:
    def __init__(self, balance, symbols):
        self.balance = balance
        self.stock_buys = []
        self.stock_sells = []
        self.balance_unit = "LKR"

        self.symbols = symbols

        self.bottoms = {}
        self.reset_bottoms()
        
        self.tops = {}
        self.reset_tops()

    def buy(self, symbol, buy_price, time):
        self.balance_unit = symbol
        self.balance = self.balance / buy_price
        self.stock_buys.append([symbol, time, buy_price])

    def sell(self, sell_price, time):
        self.balance_unit = "LKR"
        self.balance = self.balance * sell_price
        self.stock_sells.append([self.balance_unit, time, sell_price])

    def reset_bottoms(self):
        for symbol in self.symbols:
            self.bottoms[symbol] = 'none'
        
    def reset_tops(self):
        for symbol in self.symbols:
            self.tops[symbol] = 'none'        
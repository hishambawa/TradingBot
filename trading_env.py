class TradingEnvironment:
    def _init_(self, balance, symbol):
        self.balance = balance
        self.symbol = symbol
        self.stock_buys = []
        self.stock_sells = []

    def buy(self, symbol, buy_price, time):
        pass

    def sell(self, sell_price, time):
        pass

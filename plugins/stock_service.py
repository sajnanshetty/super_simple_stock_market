# from modules.utility import get_gbce_data
import datetime
import json
import pickle

class SuperSimpleStock:
    """
    Super Simple Stock Market calculations
    """
    def __init__(self, stock_symbol):
        self.symbol = stock_symbol
        self.gbce_data = SuperSimpleStock.get_gbce_data()[self.symbol]
        self.type = self.gbce_data["type"]
        self.last_dividend = self.gbce_data["last_dividend"]
        self.fixed_dividend = self.gbce_data["fixed_dividend"]
        self.par_value = self.gbce_data["par_value"]

    @staticmethod
    def get_gbce_data():
        """
        load the sample data from the Global Beverage Corporation Exchange
        """
        with open('plugins/gbce_data.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data


    def calculate_dividend(self, price):
        """
        Given any price as input, calculate the dividend yield
        """
        if price == 0:
            print("Error: Price should not be zero.")
            return None

        if self.type == "Common":
            dividend = self.last_dividend / price
        else:
            dividend = self.fixed_dividend * self.par_value / price
        return dividend
       
    def calculate_pe_ratio(self, price):
        """
        Given any price as input, calculate the P/E Ratio
        """
        if price == 0:
            print("Error: Price should not be zero.")
            return None

        dividend = self.calculate_dividend(price)
        if dividend is None:
            return None
        return price / dividend
    
    @staticmethod
    def store_trade_data(trade):
         # Load pickled trade data if available, otherwise initialize an empty list
        try:
            with open("trades.pickle", "rb") as file:
                trades = pickle.load(file)
        except FileNotFoundError:
            trades = []

        # Append the new trade to self.trades
        trades.append(trade)

        # Pickle the updated trade data
        with open("trades.pickle", "wb") as file:
            pickle.dump(trades, file)

    @staticmethod
    def get_all_trades_record():
        # Load all traded records
        try:
            with open("trades.pickle", "rb") as file:
                trades_data = pickle.load(file)
        except FileNotFoundError:
            trades_data = []
        return trades_data


    def record_trades(self, quantity, order_type, price):
        """
        Record a trade, with timestamp, quantity of shares, buy or sell indicator and
        traded price
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        
        if order_type not in ["buy", "sell"]:
            raise ValueError("Order type must be 'buy' or 'sell'.")
        
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        timestamp = datetime.datetime.now().timestamp()
        trade_data = {
            "timestamp": timestamp,
            "symbol": self.symbol,
            "quantity": quantity,
            "order_type": order_type,
            "traded_price": price

        }
        SuperSimpleStock.store_trade_data(trade_data)


    def calculate_volume_weighted_price(self):
        """
        Calculate Volume Weighted Stock Price based on trades in past 15 minutes
        """
        past_fifteen_minutes = datetime.datetime.now() - datetime.timedelta(minutes=15)
        total = 0
        quantities = 0
        trades_record = SuperSimpleStock.get_all_trades_record()
        for trade in trades_record:
            traded_time_stamp = datetime.datetime.fromtimestamp(trade["timestamp"])
            if traded_time_stamp >= past_fifteen_minutes and self.symbol == trade["symbol"]:
                total += trade["quantity"] * trade["traded_price"]
                quantities += trade["quantity"]
        quantities = 1 if quantities == 0 else quantities
        return total / quantities if quantities != 0 else 0
    
    @staticmethod
    def calculate_gbce_all_share_index():
        """
        Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
        """
        try:
            trades = SuperSimpleStock.get_all_trades_record()
            return  sum([trade["traded_price"] for trade in trades])/len(trades)
        except ZeroDivisionError:
            return None # when there are no trades
        

    # def get_gbce_all_share_index(self):
    #     """
    #     Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
    #     """
    #     try:
    #         total_prices = 1
    #         for trade in self.trades:
    #             total_prices *= trade["traded_price"]
            
    #         geometric_mean = total_prices ** (1 / len(self.trades))
    #         print("#######", geometric_mean)
    #         return geometric_mean
    #     except ZeroDivisionError:
    #         return None  # when there are no trades


if __name__ == "__main__":
    operations = """Select a number for corresponding operation:
                    1 For Calculating DIVIDEND yield.
                    2 For calculating P/E ratio.
                    3 For Recording Trade.
                    4 For Calculating Volume Weighted Stock Price.
                    5 For Calculating the GBCE All Share Index.
                    0 To exit, if you are done with all the operations.
                    ===============================================
                    Enter number: """

    stock_symbols = ["TEA", "POP", "ALE", "GIN", "JOE"]

    list_of_stock_symbols = f"Enter one of the stock symbol from given options in the choice: {','.join(stock_symbols)} "
    enter_stock_price = "Enter stock price: "
    enter_stock_quantity = "Enter stock quantity: "
    stock_type = "Enter stock order type from option buy, sell "
    re_enter_stock_type = "Please enter correct stock type  from buy, sell "
    stock_symbol = input(list_of_stock_symbols)
    if stock_symbol.upper() not in stock_symbols:
        raise ValueError(f"Enter valid symbol from {','.join(stock_symbols)} ")

    stock_obj = SuperSimpleStock(stock_symbol.upper())
    while True:
        try:
            operation_num = int(input(operations))
            if operation_num == 1:
                price = int(input(enter_stock_price))
                dividend = stock_obj.calculate_dividend(price)
                print(f"Dividend yield for {stock_symbol} at {price} is: {dividend}")
            elif operation_num == 2:
                price = int(input(enter_stock_price))
                pe_ratio = stock_obj.calculate_pe_ratio(price)
                print(f"PE ratio yield for {stock_symbol} at {price} is: {pe_ratio}")
            elif operation_num == 3:
                import time
                time.sleep(1)
                stock_type = input(stock_type)
                price = int(input(enter_stock_price))
                quantity = int(input(enter_stock_quantity))
                if stock_type.lower() not in ["buy", "sell"]:
                    print(re_enter_stock_type)
                    continue
                stock_obj.record_trades(quantity, stock_type, price)
                trades = SuperSimpleStock.get_all_trades_record()
                print(f"recorded trades data {trades}")
            elif operation_num == 4:
                import pdb
                pdb.set_trace()
                quantity = stock_obj.calculate_volume_weighted_price()
                if quantity == 0:
                    print("No trade data found to calculate")
                    continue
                print("Volume Weighted Stock Price based on trades in past 15 minutes {quantity}")
            elif operation_num == 5:
                gbce_all_share_index = SuperSimpleStock.calculate_gbce_all_share_index()
                print(f"GBCE All Share Index using the geometric mean of prices for all stocks {gbce_all_share_index}")
            elif operation_num == 0:
                break
        except (KeyError, ValueError, Exception) as error:
            print(f"Something went wrong. Error: {error}")
            continue



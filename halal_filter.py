def is_halal_stock(symbol):
    # قائمة وهمية للأسهم المتوافقة مع الشريعة
    halal_stocks = ["AAPL", "MSFT", "GOOG", "AMZN"]
    return symbol in halal_stocks

def filter_stocks(stocks_list):
    return [stock for stock in stocks_list if is_halal_stock(stock["symbol"])]

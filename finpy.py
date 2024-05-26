
def alphaVantage(api,symbol):
    '''
    Alpha Vantage:
    
    Website: Alpha Vantage
    API Key: Required (free tier available)
    Features: Stock time series, technical indicators, sector performance, foreign exchange, cryptocurrency, etc.
    '''
    #25 Queries per day
    limit = 25
    
    import requests
    
    api_key = api
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    print(data)

def yahooFinance(symbol):
    '''
    Yahoo Finance API (via yfinance library in Python):
    
    Website: Yahoo Finance
    API Key: Not required
    Features: Historical market data, real-time market data, stock fundamentals, etc.
    '''
    import yfinance as yf
    
    stock = yf.Ticker(symbol)
    
    # Get historical market data
    hist = stock.history(period="1mo")
    print(hist)
    
    # Get stock info
    info = stock.info
    print(info)

def iexCloud(api,symbol):
    '''
    IEX Cloud:
    
    Website: IEX Cloud
    API Key: Required (free tier available)
    Features: Real-time market data, historical data, company info, financials, etc.
    '''
    import requests
    
    api_key = api
    url = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    print(data)

def polygonIO(api,symbol):
    '''
    Polygon.io:
    
    Website: Polygon.io
    API Key: Required (free tier available)
    Features: Real-time and historical stock data, Forex, crypto data, market news, etc.
    '''
    
    #5 API calls / minute
    limit = 5
    import requests
    
    api_key = api
    url = f'https://api.polygon.io/v1/open-close/{symbol}/2023-01-09?adjusted=true&apiKey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    print(data)

def finnhub(api,symbol):
    '''
    Finnhub:
    
    Website: Finnhub
    API Key: Required (free tier available)
    Features: Stock data, news, fundamentals, technical indicators, sentiment analysis, etc.
    '''
    import requests
    
    api_key = api
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    print(data)

def main():
    symbol = ['AAPL','MSFT','AMZN']
    alphaAPI = "C71FN2PA3UP925DE"
    iexCloudAPI = ""
    polygonAPI = "6W_TR1c4iR4ajJEV6XUMCDBowT4TcGdB"
    finnAPI = "cp79elhr01qpb9rakgt0cp79elhr01qpb9rakgtg"
    
    for sym in symbol:
        print("====== ALPHA ======")
        alphaVantage(alphaAPI,sym)
        print("====== YAHOO ======")
        yahooFinance(sym)
        print("====== POLYGON ======")
        polygonIO(sym,polygonAPI)
        print("====== FINN ======")
        finnhub(sym,finnAPI)
        
        
        
        
        
main()
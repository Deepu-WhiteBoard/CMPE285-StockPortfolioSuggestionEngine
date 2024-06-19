import yfinance as yf
from yahoo_fin import stock_info as si
from tabulate import tabulate
import json


def get_live_price(symbol):
    return si.get_live_price(symbol)

def get_5d_hist(symbol,intervel='5d'):
    ticker = yf.Ticker(symbol)
    data = ticker.history(intervel)
    close_list= [data["Close"][0],data["Close"][1],data["Close"][2],data["Close"][3],data["Close"][4]]
    return (close_list)
    
    

def get_5d_hist_portfolio(symbols):
    list5d =[0,0,0,0,0]
    for symbol in symbols:
        print(symbol)
        currentlist = get_5d_hist(symbol)
        print(currentlist)
        addlist = [a+b for a, b in zip(list5d, currentlist)]
        list5d= addlist
    print (list5d)   
    return list5d
      






def getindexinvestment(amount, option='Snp500'):

    print("amount is",amount)
    switcher = {
        "bonds" :"ILTB",
        "total_stock_market" : "VTI",
        "Snp500": "SPY"
    }
    
    ticker= switcher.get(option)
    price = get_live_price(ticker)
    hist= get_5d_hist(ticker)
    shares =amount//price
    change =amount%price
    
    output=[['Stock Symbol',"Number of shares" ,'Current price','Invested Amount']]
    stock =[ticker,shares, price,amount-change]
    output.append(stock)
    output_json= json.dumps(output)
    print(output_json)
    return output,change

    



    
    
    
    


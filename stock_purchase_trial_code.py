import yfinance as yf

# Manually specified input for testing
user_input_value = 10000

ethical_spread = yf.download(tickers = "ADBE BYND TMO", period = "5d", interval = "1d", group_by="ticker")

# Divide investment between each stock
# Get 5d open and last day close
# Total portfolio should be positive
stock_spread = {'ADBE':1,'BYND':1,'TMO':1}
investment = user_input_value

adbe_open = ethical_spread['ADBE']['Open'][0]
print('adbe open:', adbe_open)
bynd_open = ethical_spread['BYND']['Open'][0]
print('bynd open:', bynd_open)
tmo_open = ethical_spread['TMO']['Open'][0]
print('tmo open:', tmo_open)
prices = {'ADBE':adbe_open,'BYND':bynd_open,'TMO':tmo_open}

adbe_sell = ethical_spread['ADBE']['Close'][4]
print('adbe sell:', adbe_sell)
bynd_sell = ethical_spread['BYND']['Close'][4]
print('bynd sell:', bynd_sell)
tmo_sell = ethical_spread['TMO']['Close'][4]
print('tmo sell:', tmo_sell)
sells = {'ADBE':adbe_sell,'BYND':bynd_sell,'TMO':tmo_sell}

min_investment = adbe_open + bynd_open + tmo_open

# Case: user input less than price of 1 each stock
if investment < min_investment:
    print("We suggest a minimum investment of: ${:,.2f}".format(min_investment))
# Case: price only enough to buy 1 of each
elif investment <= min_investment + min(adbe_open,bynd_open,tmo_open):
    print(stock_spread)

adbe_change = adbe_sell - adbe_open
bynd_change = bynd_sell - bynd_open
tmo_change = tmo_sell - tmo_open
changes = {'ADBE':adbe_change,'BYND':bynd_change,'TMO':tmo_change}
print(changes)
print(max(changes, key=changes.get))
# Biggest Margin
# Working money = investment - min_investment
working_value = investment - min_investment
print(working_value)


# Purchase highest return, else purchase second highest, else purchase cheapest
# Maybe add safety if all profits are negative
while working_value > prices[min(changes, key=changes.get)]:
    if working_value > prices[max(changes, key=changes.get)]:
        print('Purchasing greatest return')
        working_value -= prices[max(changes, key=changes.get)]
        stock_spread[max(changes, key=changes.get)] += 1
    elif working_value > prices[sorted(changes,key=changes.get)[2]]:
        print('Purchasing second greatest')
        working_value -=  prices[sorted(changes,key=changes.get)[2]]
        stock_spread[sorted(changes,key=changes.get)[2]] += 1
    else:
        print('Purchasing cheapest')
        working_value -= prices[min(changes, key=changes.get)]
        stock_spread[min(changes, key=changes.get)] += 1

print('Final Spread', stock_spread)
print('Remaining Investment:', working_value)

profit = 0
for k,v in stock_spread.items():
    print(k,v, "Buy:",prices[k]*v,"Sell:",sells[k]*v,"Profit:",changes[k]*v)
    profit+=changes[k]*v

adjusted_invest = investment-working_value
end_profit = adjusted_invest + profit
if end_profit > 0:
    roi = profit / adjusted_invest
    print('If you invested ${:,.2f} 5 days ago, you could have made ${:,.2f}'.format(adjusted_invest,profit))
    print("That's an ROI of {:.2%}!".format(roi))
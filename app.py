from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import yfinance as yf
#import indexStratagy as indexStratagy
app = Flask(__name__)
#app.config["DEBUG"] = True

app.config['MYSQL_USER'] = 'TeamProject202'
app.config['MYSQL_PASSWORD'] = 'bdTsJtQ9zOmUuxU0CYPJ'
app.config['MYSQL_HOST']= 'database-1.cw0lzkridbhb.us-west-1.rds.amazonaws.com'
app.config['MYSQL_DB'] = 'sys'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def strategy(strategyname):
    if(strategyname=='ethical'):
        return 'ADBE', 'BYND',  'TMO'
    elif (strategyname=='growth'):
        return 'FB','NFLX','AMZN'
    elif (strategyname=='value'):
        return 'BNTX','WFC','CS'
    elif (strategyname=='quality'):
        return 'AAPL','HD','ABT'
    elif (strategyname=='index'):
        return 'ILTB','VTI','SPY'
    else:
        return 0,0,0
    
def fiveDayPrices(portfolio):
    # Get 5day info
    # Get tickers from portfolio
    tickers = ""
    for key in portfolio.keys():
        tickers += key + " "
    # Use tickers to get stock prices
    portfolio_stocks = yf.download(tickers = tickers, period = "5d", interval = "1d", group_by="ticker")
    # Calculate daily values of portfolio
    portfolio_values = []
    for i in range(len(portfolio_stocks)):
        sum_value = 0
        for k,v in portfolio.items():
            sum_value += portfolio_stocks[k]['Close'][i]*v
        portfolio_values.append(sum_value)
    # return list of values
    return portfolio_values
    
    
def investmentStrategy(tick1,tick2,tick3,investment):
    tickers = tick1 + " " + tick2 + " " + tick3
    investment_data = yf.download(tickers = tickers, period = "5d", interval = "1d", group_by="ticker")
    # Divide investment between each stock
    # Get 5d open and last day close
    # Total portfolio should be positive
    

    # Get Opening Prices 5 days ago
    open1 = investment_data[tick1]['Open'][0]
    open2 = investment_data[tick2]['Open'][0]
    open3 = investment_data[tick3]['Open'][0]

    prices = {tick1:open1,tick2:open2,tick3:open3}

    # Get Todays Sell Prices
    sell1 = investment_data[tick1]['Close'][4]
    sell2 = investment_data[tick2]['Close'][4]
    sell3 = investment_data[tick3]['Close'][4]
    

    # At a min, buy 1 of each stock
    min_investment = open1 + open2 + open3

    # Case: user input less than price of 1 each stock
    if investment < min_investment:
        min_error = "We suggest a minimum investment of: ${:,.2f}".format(min_investment)
        return {tick1:0,tick2:0,tick3:0},[0,0,0,0,0]
        #return jsonify({'message':min_error})

    # Calculate change over 5 days
    change1 = sell1 - open1
    change2 = sell2 - open2
    change3 = sell3 - open3
    changes = {tick1: change1, tick2: change2, tick3: change3}

    # Biggest Margin
    working_value = investment % min_investment
    set_count = investment // min_investment
    stock_spread = {tick1: set_count, tick2: set_count, tick3: set_count}


    # Purchase highest return, else purchase second highest, else purchase cheapest
    while working_value > prices[min(changes, key=changes.get)]:
        if working_value > prices[max(changes, key=changes.get)]:
            working_value -= prices[max(changes, key=changes.get)]
            stock_spread[max(changes, key=changes.get)] += 1
        elif working_value > prices[sorted(changes,key=changes.get)[2]]:
            working_value -=  prices[sorted(changes,key=changes.get)[2]]
            stock_spread[sorted(changes,key=changes.get)[2]] += 1
        else:
            working_value -= prices[min(changes, key=changes.get)]
            stock_spread[min(changes, key=changes.get)] += 1

    profit = 0
    for k,v in stock_spread.items():
        profit+=changes[k]*v

    # Calculate profit
    adjusted_invest = investment-working_value
    end_profit = adjusted_invest + profit
    if end_profit > 0:
        roi = profit / adjusted_invest
    
    # Get prices over 5 days
    portfolio_values = fiveDayPrices(stock_spread)
    
    # Output stock purchases as json
    return stock_spread,portfolio_values
    
    
@app.route('/')

#home page
@app.route('/home', methods=['GET','POST'])
def home():
    if (request.method == 'GET'):
        data = "hello home"
        return jsonify({'data': data})

# registering a new user
@app.route('/register' ,methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        cursor = None

        _json = request.get_json()
        _name = _json['name']
        _password = _json['password']
        _email = _json['email']

        cursor = conn.cursor()
        _id = "SELECT max(id) FROM user"
        _id=_id+1

        sql = "INSERT INTO user (id,name,password,email) VALUES (%d,%s,%s,%s);"
        sql_insert=(_id, _name , _password , _email ,)

        cursor.execute(sql,sql_insert)
        conn.commit()
        cursor.close()
        return jsonify({_name : 'You have registered successfully'})
    if request.method == 'GET':
        return 'register frontend'

#login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cursor = None
        _json = request.get_json()
        _email = _json['email']
        _password = _json['password']
        
        if _email and _password:
            cursor = conn.cursor()

            sql = "SELECT * FROM user WHERE email=%s"
            sql_where = (_email,)

            cursor.execute(sql, sql_where)
            row = cursor.fetchone()

        if row:
            if 	(row[3]== _password):
                session['name'] = row[1]
                session['id'] = str(row[0])
                return jsonify({'message' : 'You are logged in successfully'})
            else:
                return jsonify({'message' : 'Error!! Invalid password'})
        else:
            return jsonify({'message' : 'Error!! Invalid credentials'})

    elif request.method == 'GET':
        return 'login frontend'

#logout
@app.route('/logout' ,methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        if 'id' in session:
            session.pop('id', None)
        return jsonify({'message' : 'You successfully logged out'})

    if request.method== 'GET':
        return 'logout frontend'

#Customer landing page
@app.route('/landing', methods=['GET','POST'])
def landing():
    if (request.method == 'POST'):
        _json = request.get_json()
        _strategy1 = _json['_strategy1']
        _strategy2 = _json['_strategy2']
        strategy1 = _strategy1.lower()
        strategy2 = _strategy2.lower()
        _amount1 = _json['_amount1']
        _amount2 = _json['_amount2']

        ticker1,ticker2,ticker3 = strategy(strategy1)
        stock_spread1, portfolio_values1 = investmentStrategy(ticker1,ticker2,ticker3,_amount1)
        if(strategy2!=''):
            ticker1_2,ticker2_2,ticker3_2 = strategy(strategy2)
            stock_spread2, portfolio_values2 = investmentStrategy(ticker1_2,ticker2_2,ticker3_2,_amount2)
            return jsonify({'portfolio1': stock_spread1,'day0_1':portfolio_values1[0],'day1_1':portfolio_values1[1],'day2_1':portfolio_values1[2],'day3_1':portfolio_values1[3],'day4_1':portfolio_values1[4],'portfolio2': stock_spread2,'day0_2':portfolio_values2[0],'day1_2':portfolio_values2[1],'day2_2':portfolio_values2[2],'day3_2':portfolio_values2[3],'day4_2':portfolio_values2[4]})

        else:
            return jsonify({'portfolio1': stock_spread1,'day0_1':portfolio_values1[0],'day1_1':portfolio_values1[1],'day2_1':portfolio_values1[2],'day3_1':portfolio_values1[3],'day4_1':portfolio_values1[4]})
     
    elif request.method == 'GET':
        return 'landing page frontend'


# driver function
if __name__ == '__main__':
    app.run(debug=True)

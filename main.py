import config
import websocket, json
import requests
import time
import schedule
import datetime

socket = config.ALPACA_WEBHOOK
price =''
lastPrice =''
bot_token = config.TOKEN_TEL_BOT
bot_chatID = config.TEL_CHAT_AL
#bot_chatID = config.TEL_CHAT_LE
timetest=time.time()
alertList=[{
    "Ticker": 'AAPL',
    "Support": 143.200,
    "First Resistance": 144.000,
    "First Take Profit": 144.500,
    "Stop Loss": 142.500,
    "Swing Target": 145.000,
    "LastPrice": 0.000,
    "SupportTriggerU": time.time()-10000,
    "SupportTriggerD": time.time()-10000,
    "SupportTriggerP": time.time()-10000,
    "FirstResistanceTriggerU": time.time()-10000,
    "TakeProfitTriggerU": time.time()-10000,
    "StopLossTriggerD": time.time()-10000,
    "SwingTargetTriggerU": time.time()-10000
},{
    "Ticker": 'GM',
    "Support": 56.300,
    "First Resistance": 56.800,
    "First Take Profit": 57.300,
    "Stop Loss": 56.000,
    "Swing Target": 57.900,
    "LastPrice": 0.000,
    "SupportTriggerU": time.time()-10000,
    "SupportTriggerD": time.time()-10000,
    "SupportTriggerP": time.time()-10000,
    "FirstResistanceTriggerU": time.time()-10000,
    "TakeProfitTriggerU": time.time()-10000,
    "StopLossTriggerD": time.time()-10000,
    "SwingTargetTriggerU": time.time()-10000
}]

def on_open(ws):
    print("opened")
    
    auth_data = {
        "action": "auth",
        "key": config.API_KEY, 
        "secret": config.SECRET_KEY
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "subscribe", "bars": [alertList[0]["Ticker"], alertList[1]["Ticker"]]}

    ws.send(json.dumps(listen_message))

def on_message(ws, message):
    print("received a message")
    messageJ = json.loads(message)
    print(messageJ)
    #print("this is the close price of " + messageJ[0]["S"])
    stockSymb = messageJ[0]["S"]
    priceN = messageJ[0]["c"]
    priceN = float(priceN)
    #print(priceN)
    getStock(priceN, stockSymb)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("closed connection")

def getStock(price, stock):
     for dic in alertList:
        try:
            if stock != dic["Ticker"]:
                return
            if dic["LastPrice"] == 0: 
                dic["LastPrice"] = price
            lastPrice = dic["LastPrice"]
            message = ''
            #print("Hello, this is the price: " + str(price))
            #print("Test: " + str(dic["First Resistance"]))
            if price > dic["First Resistance"] and lastPrice < dic["First Resistance"] and time.time()-dic["FirstResistanceTriggerU"] >=3600:
                message = dic["Ticker"] + ' just broke through the first resistance (' + str(dic["First Resistance"]) + ')'
                dic["FirstResistanceTriggerU"] = time.time()
            elif price > dic["First Take Profit"] and lastPrice < dic["First Take Profit"] and time.time()-dic["TakeProfitTriggerU"] >=3600:
                message = dic["Ticker"] + ': Take first profits (' + str(dic["First Take Profit"]) + ')'
                dic["TakeProfitTriggerU"] = time.time()
            elif price > dic["Swing Target"] and lastPrice < dic["Swing Target"] and time.time()-dic["SwingTargetTriggerU"] >=3600:
                message = dic["Ticker"] + ' just reached the Swing Target (' + str(dic["Swing Target"]) + ')'
                dic["SwingTargetTriggerU"] = time.time()
            elif price > dic["Support"] and lastPrice < dic["Support"] and time.time()-dic["SupportTriggerU"] >=3600:
                message = dic["Ticker"] + ' just pushed through the Support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerU"] = time.time()
            elif price < dic["Support"] and lastPrice > dic["Support"] and time.time()-dic["SupportTriggerD"] >=3600:
                message = dic["Ticker"] + ' just fell through support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerD"] = time.time()
            elif price == dic["Support"] and time.time()-dic["SupportTriggerP"] >=3600:
                message = dic["Ticker"] + ' just reached support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerP"] = time.time()
            elif price < dic["Swing Target"] and lastPrice > dic["Swing Target"] and time.time()-dic["SwingTargetTriggerU"] >=3600:
                message = dic["Ticker"] + ': Stop loss triggered (' + str(dic["Stop Loss"]) + ')'
                dic["SwingTargetTriggerU"] = time.time()
            dic["LastPrice"] = price
            if message != '':
                send_text='https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + message
                response=requests.get(send_text)
                print(message)
                print(response)
            print('Old Price of ' + dic["Ticker"] + ': ' + str(lastPrice))
            print('New Price of ' + dic["Ticker"] + ': ' + str(price))
        except Exception as e:
            print("OS error: {0}".format(e))

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
ws.run_forever()
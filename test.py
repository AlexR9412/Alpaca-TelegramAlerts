import config
import websocket, json, time, requests

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

closePrice =''
lastPrice =''
bot_token = config.TOKEN_TEL_BOT
bot_chatID = config.TEL_CHAT_AL
#bot_chatID = config.TEL_CHAT_LE

def on_open(ws):                # wird beim 1. Start ausgeführt
    print("======================")
    print("Connecting...")


def on_message(ws,message):
    message = json.loads(message)[0]
    if message["T"]=="success" and message["msg"]=="connected":
        print("-Success-")
        print("Authenticate...")
        auth_data = {"action": "auth",
                     "key":config.API_KEY,
                     "secret": config.SECRET_KEY}
        ws.send(json.dumps(auth_data))      # senden der KEYs an die API
    elif message["T"]=="success" and message["msg"]=="authenticated":
        print("-Success-")
        print("Start Stream...")
        listen_message = {"action":"subscribe","bars":watchlist}
        ws.send(json.dumps(listen_message)) # senden der Ticker Anfrage
    elif message["T"]=="subscription":
        print("Subscripted to: "+ str(message["bars"]))
        print("======================")
    elif message["T"]=="b":
        checkAlerts(str(message["S"]),float(message["c"]),float(message["v"]))
        print(message)
    else:
        print(message["T"])

def on_close(ws):
    print("Closed connection")

def connect_to_socket():
    ws.run_forever()

def new_thread(mode):
    import threading
    if mode == 1:
        t = threading.Thread(target=connect_to_socket)
        t.start()
    #if mode == 2:
    #    t2 = threading.Thread(target=watch)
    #    t2.start()

def checkAlerts(symbol, closePrice, volume):
    for dic in alertList:
        try:
            if symbol != dic["Ticker"]:
                return
            if dic["LastPrice"] == 0: 
                dic["LastPrice"] = closePrice
            lastPrice = dic["LastPrice"]
            message = ''
            #print("Hello, this is the price: " + str(price))
            #print("Test: " + str(dic["First Resistance"]))
            if closePrice > dic["First Resistance"] and lastPrice < dic["First Resistance"] and time.time()-dic["FirstResistanceTriggerU"] >=3600:
                message = dic["Ticker"] + ' just broke through the first resistance (' + str(dic["First Resistance"]) + ')'
                dic["FirstResistanceTriggerU"] = time.time()
            elif closePrice > dic["First Take Profit"] and lastPrice < dic["First Take Profit"] and time.time()-dic["TakeProfitTriggerU"] >=3600:
                message = dic["Ticker"] + ': Take first profits (' + str(dic["First Take Profit"]) + ')'
                dic["TakeProfitTriggerU"] = time.time()
            elif closePrice > dic["Swing Target"] and lastPrice < dic["Swing Target"] and time.time()-dic["SwingTargetTriggerU"] >=3600:
                message = dic["Ticker"] + ' just reached the Swing Target (' + str(dic["Swing Target"]) + ')'
                dic["SwingTargetTriggerU"] = time.time()
            elif closePrice > dic["Support"] and lastPrice < dic["Support"] and time.time()-dic["SupportTriggerU"] >=3600:
                message = dic["Ticker"] + ' just pushed through the Support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerU"] = time.time()
            elif closePrice < dic["Support"] and lastPrice > dic["Support"] and time.time()-dic["SupportTriggerD"] >=3600:
                message = dic["Ticker"] + ' just fell through support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerD"] = time.time()
            elif closePrice == dic["Support"] and time.time()-dic["SupportTriggerP"] >=3600:
                message = dic["Ticker"] + ' just reached support (' + str(dic["Support"]) + ')'
                dic["SupportTriggerP"] = time.time()
            elif closePrice < dic["Swing Target"] and lastPrice > dic["Swing Target"] and time.time()-dic["SwingTargetTriggerU"] >=3600:
                message = dic["Ticker"] + ': Stop loss triggered (' + str(dic["Stop Loss"]) + ')'
                dic["SwingTargetTriggerU"] = time.time()
            dic["LastPrice"] = closePrice
            if message != '':
                send_text='https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + message
                response=requests.get(send_text)
                print(message)
                print(response)
            print('Old Price of ' + dic["Ticker"] + ': ' + str(lastPrice))
            print('New Price of ' + dic["Ticker"] + ': ' + str(closePrice))
            print('Volume:' + str(volume))
        except Exception as e:
            print("OS error: {0}".format(e))

def init():
    new_thread(1)

    #time.sleep(XX)
    # die Fukntion watch() soll erst nach einer gewissen Zeit gestartet werden
    #new_thread(2)
    


def getWatchList():
    tickers = ''
    for dic in alertList:
        tickers = tickers + dic["Ticker"]
    print(tickers)
    return tickers
    
watchlist = ["GM", "AAPL"]

socket = "wss://stream.data.alpaca.markets/v2/iex"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)

init()
import config, threading
import websocket, json
import requests
import time
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL

#conn = tradeapi.stream2.StreamConn(config.API_KEY, config.SECRET_KEY, config.ALPACA_WEBHOOK)
conn = Stream(config.API_KEY,
                  config.SECRET_KEY,
                  base_url=URL(config.ALPACA_WEBHOOK),
                  data_feed='iex')
price =''
lastPrice =''
bot_token = config.TOKEN_TEL_BOT
bot_chatID = config.TEL_CHAT_AL
#bot_chatID = config.TEL_CHAT_LE

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

@conn.on(r'^AM.AAPL$')
async def on_minute_bars(conn, channel, bar):
    print('bars', bar)

def ws_start():
	conn.run(['AM.AAPL'])

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

#start WebSocket in a thread
ws_thread = threading.Thread(target=ws_start, daemon=True)
ws_thread.start()
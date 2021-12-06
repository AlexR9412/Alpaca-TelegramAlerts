import config, logging
import time
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

socket = config.ALPACA_WEBHOOK
price =''
lastPrice =''
tickerList = []
bot_token = config.TOKEN_TEL_BOT
bot_chatID = config.TEL_CHAT_AL
#bot_chatID = config.TEL_CHAT_LE

alertList=[{
    "Ticker": 'LTCUSD',
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
    "Ticker": 'ETHUSD',
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

def run_connection(conn):
    try:
        conn.run()
    except Exception as e:
        print(f'Exception from websocket connection: {e}')

async def print_bars(bar):
    print('bar', bar)

if __name__ == '__main__':
    for dic in alertList:
        tickerList.append(dic["Ticker"])
    tickerListStr = str(tickerList)[1:-1]
    print(tickerList)
    print(tickerListStr)
    conn = Stream(config.API_KEY,
                  config.SECRET_KEY,
                  base_url=URL('https://paper-api.alpaca.markets'),
                  data_feed='iex')
    #conn.unsubscribe_crypto_bars("ETHUSD")
    conn.subscribe_crypto_bars(print_bars, "ETHUSD")

    run_connection(conn)
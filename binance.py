from binance.client import Client
import pandas as pd
from colorama import init
from decimal import *
import time
import requests
import os

init()
clear = lambda: os.system('cls')
binance = Client('api_key', 'secret')
tumFiyatlar = binance.get_all_tickers()
coinler = []
free_ = []

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def fiyatBul(sym):
    count = 0
    for i in tumFiyatlar:
        count += 1
        ticker = i.get('symbol')
        if ticker == sym:
            val = i.get('price')
            count = count-1
            return count
            
def do():
    coinler = []
    free_ = []
    coinGetir = binance.get_account()
    for i in range(0, len(coinGetir['balances'])): 
        if(Decimal(coinGetir['balances'][i]['free']) > 1):
            if(coinGetir['balances'][i]['asset'] != 'USDT'):
                coinler.append(coinGetir['balances'][i]['asset']+'USDT')
                free_.append(coinGetir['balances'][i]['free'])

    for i in range(0, len(coinler)):
        orderS = binance.get_all_orders(symbol=coinler[i], limit=1)
        if(orderS[0]['type'] == 'MARKET' and  orderS[0]['side'] == 'BUY'):
            alınanMiktar = Decimal(orderS[0]['executedQty'])
            toplamFiyat = Decimal(orderS[0]['cummulativeQuoteQty'])
            alımFiyatı = Decimal(orderS[0]['cummulativeQuoteQty']) / Decimal(orderS[0]['executedQty'])

            anlıkFiyat = Decimal(tumFiyatlar[fiyatBul(coinler[i])].get('price'))
            eldekiAdet = Decimal(free_[i])

            toplamFiyatAnlık = anlıkFiyat * eldekiAdet

            if(toplamFiyatAnlık > toplamFiyat):
                yuzdeDegisim = Decimal(((anlıkFiyat - alımFiyatı) / alımFiyatı) * 100)
                fiyatDeğişimi = Decimal(toplamFiyatAnlık - toplamFiyat)
                yuzdeDegisimDuzeltilsim = Decimal(yuzdeDegisim).quantize(Decimal('.001'), rounding=ROUND_DOWN)
                fiyatDegisimDuzeltilsim = Decimal(fiyatDeğişimi).quantize(Decimal('.001'), rounding=ROUND_DOWN)
                if(yuzdeDegisimDuzeltilsim > 6):
                    minSatmaOranı_ = binance.get_symbol_info(orderS[0]['symbol'])
                    minSatmaOranı = Decimal(minSatmaOranı_['filters'][2]['minQty'])
                    if(minSatmaOranı == Decimal("1.00000000")):
                        satılacakMiktar=int(eldekiAdet)
                    if(minSatmaOranı == Decimal("0.10000000")):
                        satılacakMiktar=Decimal(eldekiAdet).quantize(Decimal('.1'), rounding=ROUND_DOWN)
                    if(minSatmaOranı == Decimal("0.01000000")):
                        satılacakMiktar=Decimal(eldekiAdet).quantize(Decimal('.01'), rounding=ROUND_DOWN)
                    if(minSatmaOranı == Decimal("0.00100000")):
                        satılacakMiktar = Decimal(eldekiAdet).quantize(Decimal('.001'), rounding=ROUND_DOWN)
                    if(minSatmaOranı == Decimal("0.00010000")):
                        satılacakMiktar=Decimal(eldekiAdet).quantize(Decimal('.0001'), rounding=ROUND_DOWN)
                    if(minSatmaOranı == Decimal("0.00001000")):
                        satılacakMiktar=Decimal(eldekiAdet).quantize(Decimal('.00001'), rounding=ROUND_DOWN)
                    if(minSatmaOranı == Decimal("0.00000100")):
                        satılacakMiktar=Decimal(eldekiAdet).quantize(Decimal('.000001'), rounding=ROUND_DOWN)
                    order = binance.order_market_sell(symbol=orderS[0]['symbol'],quantity=satılacakMiktar)
                    send_text = 'https://api.telegram.org/bot'+bot_id+'/sendMessage?chat_id='+chat_id+'&text='+orderS[0]['symbol']+' '+str(fiyatDegisimDuzeltilsim)
                    response = requests.get(send_text)
                print(bcolors.WARNING + orderS[0]['symbol'] + bcolors.ENDC+' '+bcolors.OKGREEN +'%'+ str(yuzdeDegisimDuzeltilsim) + bcolors.ENDC+' '+bcolors.OKGREEN + str(fiyatDegisimDuzeltilsim) + bcolors.ENDC)

            if(toplamFiyat > toplamFiyatAnlık):
                yuzdeDegisim = Decimal(((anlıkFiyat - alımFiyatı) / alımFiyatı) * 100)
                fiyatDeğişimi = Decimal(toplamFiyatAnlık - toplamFiyat)
                yuzdeDegisimDuzeltilsim = Decimal(yuzdeDegisim).quantize(Decimal('.001'), rounding=ROUND_DOWN)
                fiyatDegisimDuzeltilsim = Decimal(fiyatDeğişimi).quantize(Decimal('.001'), rounding=ROUND_DOWN)
                print(bcolors.WARNING + orderS[0]['symbol'] + bcolors.ENDC+' '+bcolors.FAIL +'%'+ str(yuzdeDegisimDuzeltilsim) + bcolors.ENDC+' '+bcolors.FAIL + str(fiyatDegisimDuzeltilsim) +bcolors.ENDC)
        #time.sleep(1)
                

if __name__ == "__main__":
    while True:
        try:
            for i in range(5):
                i += 1
                tumFiyatlar = binance.get_all_tickers()
                do()
                if(i == 5):
                    clear()
                    i = 0
        except:
            print("timeout") 
            pass
            

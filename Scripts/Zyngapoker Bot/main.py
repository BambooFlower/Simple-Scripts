#!mitmdump -s

"""
MVP:
    https://github.com/mitmproxy/mitmproxy/issues/3306
"""
#from server import start
from selenium import webdriver
from read_file import Game
#import multiprocessing
import subprocess
import threading

#new_loop = asyncio.new_event_loop()
#proxy_server = threading.Thread(target=start,args=(new_loop,))
##proxy_server.daemon = True
#proxy_server.start()


server = subprocess.Popen(('python', 'server.py'), stdout=subprocess.PIPE)
server.daemon = True
#ps.wait()

proxy_ip = '127.0.0.1'
proxy_port = 8080
PROXY = '{}:{}'.format(proxy_ip,proxy_port)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(options=chrome_options)
chrome.get("https://www.zyngapoker.com/")

def game_start():
    global G
    G = Game()
    x = threading.Thread(target=G.read_file)
    x.start()

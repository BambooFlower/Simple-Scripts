
from multiprocessing import Process

import mitmproxy.addonmanager
import mitmproxy.connections
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
import mitmproxy.websocket
import mitmproxy.proxy.protocol

import requests

import json
import os

import threading
import time

from selenium import webdriver

from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster

import asyncio

class SniffWebSocket:
    def __init__(self):
        self.msgs = []
    
    # Websocket lifecycle
    def websocket_handshake(self, flow: mitmproxy.http.HTTPFlow):
        """
            Called when a client wants to establish a WebSocket connection. The
            WebSocket-specific headers can be manipulated to alter the
            handshake. The flow object is guaranteed to have a non-None request
            attribute.
        """

    def websocket_start(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has commenced.
        """

    def websocket_message(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            Called when a WebSocket message is received from the client or
            server. The most recent message will be flow.messages[-1]. The
            message is user-modifiable. Currently there are two types of
            messages, corresponding to the BINARY and TEXT frame types.
        """
        msgs = []
        for flow_msg in flow.messages:
            packet = flow_msg.content
            #print( packet[:100])
            msgs.append([time.time(),packet])
            #with open('wss.out','w') as f:
            #     f.write(str(packet))
        
        # if not os.file.path.exists('wss.out'):
        #     self.msgs = []
        
            
        with open('wss.out','a') as f:
            f.write(str(time.time())+","+str(flow.messages[-1])+"\n")

        #if len(flow.messages) > 30:
        #    r1 = requests.get("http://127.0.0.1:8080/")
        #    jar = r1.cookies
        #    csrf_token = jar.get('_xsrf')
        #    r2 = requests.post("http://127.0.0.1:8080/clear?_xsrf={0}".format(csrf_token), cookies=jar)

    def websocket_error(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has had an error.
        """

    def websocket_end(self, flow: mitmproxy.websocket.WebSocketFlow):
        """
            A websocket connection has ended.
        """

# addons = [
#     SniffWebSocket()
# ]

proxy_ip = '127.0.0.1'
proxy_port = 8080
PROXY = '{}:{}'.format(proxy_ip,proxy_port)

#def start(loop):
def start():
    #asyncio.set_event_loop()
    myaddon = SniffWebSocket() #AddHeader()
    opts = options.Options(listen_host=proxy_ip, listen_port=proxy_port)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

start()


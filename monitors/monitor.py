#!/usr/bin/env python
#
# monitor.py - Remote monitor for packetbeacon.py
#
#
# Author: Patrick F. Wilbur (pdub.net)
#
# Copyright 2019 Patrick F. Wilbur. All Rights Reserved.
# 


import socketserver

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print(data)

if __name__ == "__main__":
    server = socketserver.UDPServer(('', 13337), MyUDPHandler)
    server.serve_forever()


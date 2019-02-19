#!/usr/bin/env python
#
# monitor_raspberrypi.py - Remote monitor for packetbeacon.py,
# which toggles an LED every time someone on the
# local network browses the Web unsafely.
#
#
# Author: Patrick F. Wilbur (pdub.net)
#
# Copyright 2019 Patrick F. Wilbur. All Rights Reserved.
# 

import socketserver
import threading
import time
import RPi.GPIO as GPIO

LED = False
LED_until = 0

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global LED,LED_until
        data = self.request[0].strip()
        print data
        LED = True
        LED_until = time.time() + 5

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    server = socketserver.UDPServer(('', 13337), MyUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "now monitoring unsafe web activity..."
    while True:
        if time.time() > LED_until:
            LED = False
        if LED:
            print "LED ON"
        GPIO.output(7,LED)
        time.sleep(1)


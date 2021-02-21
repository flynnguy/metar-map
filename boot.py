# -*- coding: utf-8 -*-
# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
import ujson
# import webrepl
# webrepl.start()
gc.collect()

with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secrets['wifi']['ssid'], secrets['wifi']['pass'])
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


do_connect()  # Alternatively, you can call this from your main.py program

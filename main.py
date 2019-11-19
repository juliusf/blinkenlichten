from umqtt.simple import MQTTClient
import machine
import utime
import ubinascii
import p9813
from machine import Pin

from config import SERVER, COMMAND_TOPIC, STATE_TOPIC, AVAILABILITY_TOPIC
 
LED = machine.Pin(2, machine.Pin.OUT, value=1)
 
CLIENT = None
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

pin_clk = Pin(5, Pin.OUT)
pin_data = Pin(4, Pin.OUT)

num_leds = 1
chain = p9813.P9813(pin_clk, pin_data, num_leds)

 
def new_msg(topic, msg):
 
    print("Received {}".format(msg))
 
    if msg == b"on":
        LED.value(0)
        chain[0] = (0,0,0)
        chain.write()
        CLIENT.publish(STATE_TOPIC, "on")
    elif msg == b"off":
        LED.value(1)
        chain[0] = (255,0,0)
        chain.wite()
        CLIENT.publish(STATE_TOPIC, "off")
 
 
def main():
    global CLIENT
    CLIENT = MQTTClient(CLIENT_ID, SERVER)
    CLIENT.set_callback(new_msg)
    CLIENT.connect()
 
    CLIENT.subscribe(COMMAND_TOPIC)
    chain[0] = (255,0,32)
    chain.write()
    # Publish as available once connected
    CLIENT.publish(AVAILABILITY_TOPIC, "online")
 
    print("Connected to {}, subscribed to {} topic".format(SERVER, COMMAND_TOPIC))
 
    try:
        while 1:
            CLIENT.wait_msg()
    finally:
        CLIENT.publish(AVAILABILITY_TOPIC, "offline")
        CLIENT.disconnect()
 
main()

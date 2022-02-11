# python3.6

import random
import RPi.GPIO as gpio
import time
from paho.mqtt import client as mqtt_client

gpio.setmode(gpio.BOARD)
GPIO_SITTING_ROOM_LIGHTS = 15
gpio.setup(GPIO_SITTING_ROOM_LIGHTS, gpio.OUT)
GPIO_WATER_PUMP = 12
gpio.setup(GPIO_WATER_PUMP, gpio.OUT)
GPIO_FAN = 13
gpio.setup(GPIO_FAN, gpio.OUT)
GPIO_GATE = 29
gpio.setup(GPIO_GATE, gpio.OUT)

broker = '172.16.32.81'
port = 1883
activateTopic = "device/activate"
deactivateTopic = "device/deactivate"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def activateSubscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.payload.decode() == 'sitting-room-lights':
            print('sitting-room-lights activated')
            gpio.output(GPIO_SITTING_ROOM_LIGHTS, True)
        elif msg.payload.decode() == 'waterPump':
            print('waterPump activated')
            gpio.output(GPIO_WATER_PUMP, True)
        elif msg.payload.decode() == 'gateSwitch':
            print('gateSwitch activated')
            gpio.output(GPIO_GATE, True)
        elif msg.payload.decode() == 'fan':
            print('gateSwitch activated')
            gpio.output(GPIO_FAN, True)
        elif msg.payload.decode() == 'sitting-room-lights2':
            print('sitting-room-lights activated')
            gpio.output(GPIO_SITTING_ROOM_LIGHTS, False)
        elif msg.payload.decode() == 'waterPump2':
            print('waterPump activated')
            gpio.output(GPIO_WATER_PUMP, False)
        elif msg.payload.decode() == 'gateSwitch2':
            print('gateSwitch activated')
            gpio.output(GPIO_GATE, False)
        elif msg.payload.decode() == 'fan2':
            print('gateSwitch activated')
            gpio.output(GPIO_FAN, False)
        else:
            print('Device not present')
            # deactivateSubscribe(client)

    client.subscribe(activateTopic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    activateSubscribe(client)
    # deactivateSubscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()


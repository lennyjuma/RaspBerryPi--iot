# python3.6

import random
import RPi.GPIO as gpio
import time
from paho.mqtt import client as mqtt_client

gpio.setmode(gpio.BOARD)
GPIO_BULB_FRONT = 15
gpio.setup(GPIO_BULB_FRONT, gpio.OUT)
GPIO_BULB_BACK = 12
gpio.setup(GPIO_BULB_BACK, gpio.OUT)
GPIO_FAN = 13
gpio.setup(GPIO_FAN, gpio.OUT)

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
        if msg.payload.decode() == 'Temperature-bulb-front':
            print('Temperature-bulb-front activated')
            gpio.output(GPIO_BULB_FRONT, True)
        elif msg.payload.decode() == 'Temperature-bulb-back':
            print('Temperature-bulb-back activated')
            gpio.output(GPIO_BULB_BACK, True)
        elif msg.payload.decode() == 'fan':
            print('fan activated')
            gpio.output(GPIO_FAN, True)
        elif msg.payload.decode() == 'Temperature-bulb-front2':
            print('Temperature-bulb-front deactivated')
            gpio.output(GPIO_BULB_FRONT, False)
        elif msg.payload.decode() == 'Temperature-bulb-back2':
            print('Temperature-bulb-back deactivated')
            gpio.output(GPIO_BULB_BACK, False)
        elif msg.payload.decode() == 'fan2':
            print('fan deactivated')
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


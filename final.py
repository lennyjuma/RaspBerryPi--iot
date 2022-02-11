# python3.6

import random
import RPi.GPIO as gpio
import Adafruit_DHT
import time
import paho.mqtt.publish as publish
from paho.mqtt import client as mqtt_client


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17
# import os

gpio.setmode(gpio.BOARD)
GPIO_BULB_FRONT = 8
gpio.setup(GPIO_BULB_FRONT, gpio.OUT)
# gpio.output(GPIO_BULB_FRONT, True)
GPIO_BULB_BACK = 12
gpio.setup(GPIO_BULB_BACK, gpio.OUT)
GPIO_FAN = 13
gpio.setup(GPIO_FAN, gpio.OUT)

broker = '172.16.32.81'
port = 1883
topic = "device/activate"

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
    run_dht11()
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def activateSubscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # run_dht11()
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

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    activateSubscribe(client)
    # deactivateSubscribe(client)
    client.loop_forever()


def run_dht11():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}C  Humidity={1:0.1f}%".format(temperature, humidity))
            publish.single("temperature", temperature, hostname="172.16.32.81")
            publish.single("humidity", humidity, hostname="172.16.32.81")
        else:
            print("Sensor failure. Check wiring.");
        time.sleep(3)


if __name__ == '__main__':
    run()
    # os.system("python3 temp.py")


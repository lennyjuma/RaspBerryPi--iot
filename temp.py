import Adafruit_DHT
import time
import paho.mqtt.publish as publish

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}C  Humidity={1:0.1f}%".format(temperature, humidity))
        publish.single("temperature", temperature, hostname="172.16.32.81")
        publish.single("humidity", humidity, hostname="172.16.32.81")
    else:
        print("Sensor failure. Check wiring.");
    time.sleep(3)

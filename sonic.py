
#Libraries
import RPi.GPIO as GPIO
import time
import random

from paho.mqtt import client as mqtt_client

broker = '172.16.33.43'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 16
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


## This function will be called after connecting the client, 
##and we can determine whether the client is connected successfully according to rc in this function.
# Usually, we will create an MQTT client at the same time and this client will connect to broker.emqx.io 

def connect_mqtt():
#    def on_connect(client, userdata, flags, rc):
   #     if rc == 0:
    #        print("Connected to MQTT Broker!")
     #   else:
      #      print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
 #   client.on_connect = on_connect
    client.connect(broker, port)
    return client

#First, we define a while loop. In this loop, and we will set the MQTT client publish function to send messages to the topic /python/mqtt every second

def publish(client):
     msg_count = 0
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1


def distance(client):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    client.publish("testTopic/distance", distance)
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            client = connect_mqtt()
            client.loop_start()
#            client.publish("testTopic/distance", dist)
            dist = distance(client)
            client.publish("testTopic/distance", dist)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(5)                  
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

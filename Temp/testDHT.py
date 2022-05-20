import Adafruit_DHT
import time

dht=Adafruit_DHT.DHT22
pin = 21
while 1:
    h,t= Adafruit_DHT.read_retry(dht,pin)
    print ("temp = %2.2f humidity = %2.2f" %(t,h))
    time.sleep(2)
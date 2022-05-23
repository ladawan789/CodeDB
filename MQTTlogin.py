import paho.mqtt.publish as publish
import time

hostname = "10.11.1.71"
port = 1883
auth = {
 'username':'admin',
 'password':'CL@333/6'
}

while True:
 print("Sending 1...")
 publish.single("Login","1", hostname=hostname, port=port, auth=auth)
 time.sleep(6)
 print("Sending 0...")
 publish.single("Login","0", hostname=hostname, port=port, auth=auth)
 time.sleep(3)
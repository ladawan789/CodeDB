import time
import RPi.GPIO as GPIO
import mysql.connector
import paho.mqtt.publish as publish

db = mysql.connector.connect(
  host="10.11.16.66",
  user="IOT_1",
  passwd="SnccOOling",
  database="attendance_system"
)

hostname = "10.11.1.71"
port = 1883
auth = {
 'username':'admin',
 'password':'CL@333/6'
}

cursor = db.cursor()
a=0

try:
  while True:
    print('Place Card to\nrecord attendance')
    id = input("RFID : ")

    cursor.execute("Select name FROM users WHERE rfid_uid="+str(id))
    result = cursor.fetchone()

    if cursor.rowcount >= 1:
      print("Welcome " + result[0])
      cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
      publish.single("Login",payload=result[0], hostname=hostname, port=port, auth=auth)
      time.sleep(1)
      a=1
      db.commit()
    else:
        print("User does not exist.")
        time.sleep(2)
        
    if (a==1):
        print('Place Card to\nrecord attendance')
        id = input("RFID : ")

        cursor.execute("Select name FROM product WHERE rfid_uid="+str(id))
        result = cursor.fetchone()

        if cursor.rowcount >= 1:
            print("Welcome " + result[0])
            cursor.execute("INSERT INTO productOrder (user_id) VALUES (%s)", (result[0],) )
            publish.single("Login1",payload=result[0], hostname=hostname, port=port, auth=auth)
            time.sleep(1)
            a=0
            db.commit()
        else:
            print("User does not exist.")
            a=0
            time.sleep(2)
finally:
  GPIO.cleanup()
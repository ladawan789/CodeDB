import time
import RPi.GPIO as GPIO
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="IOT-2",
  passwd="SnccOOling",
  database="attendance_system"
)

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
            a=0
            db.commit()
        else:
            print("User does not exist.")
            a=0
            time.sleep(2)
finally:
  GPIO.cleanup()
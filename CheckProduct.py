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

try:
  while True:
    print('Place Card to\nrecord attendance')
    id, text = input("RFID : ")

    cursor.execute("Select id, name FROM product WHERE rfid_uid="+str(id))
    result = cursor.fetchone()

    if cursor.rowcount >= 1:
      print("Welcome " + result[1])
      cursor.execute("INSERT INTO productOrder (user_id) VALUES (%s)", (result[0],) )
      db.commit()
    else:
        print("User does not exist.")
        time.sleep(2)
finally:
  GPIO.cleanup()
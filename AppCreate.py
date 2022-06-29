import tkinter
from tkinter import*
import mysql.connector

root=Tk()
root.geometry("400x400")
root.title("Test DB")
t_conn=StringVar()
def connDB():
    db = mysql.connector.connect(
  host="localhost",
  user="IOT-2",
  passwd="SnccOOling",
  database="attendance_system"
)
    cursor = db.cursor()
    query = "select * from users"
    cursor.execute(query)
    result = cursor.fetchall()
    bb = cursor.execute(query)
    if cursor:
        condb = "Connection OK"
    else:
        condb = "Connection Fail"
    db.colse()
    t_conn.set(condb)
button = Button(root, text="connect DB",command = connDB)
button.pack()
label_1=Label(root,textvariable=t_conn)
label_1.pack()
root.mainloop()
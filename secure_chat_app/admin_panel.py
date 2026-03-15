import tkinter as tk
import sqlite3

def view_users():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")

    users = cursor.fetchall()

    output.delete(1.0, tk.END)

    for user in users:
        output.insert(tk.END, user[0] + "\n")

    conn.close()

def view_logs():
    output.delete(1.0, tk.END)

    with open("logs.txt","r") as f:
        logs = f.readlines()

    for log in logs:
        output.insert(tk.END, log)

window = tk.Tk()
window.title("Admin Panel")

btn1 = tk.Button(window,text="View Users",command=view_users)
btn1.pack()

btn2 = tk.Button(window,text="View Logs",command=view_logs)
btn2.pack()

output = tk.Text(window,height=20,width=60)
output.pack()

window.mainloop()
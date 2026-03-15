import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from encryption import encrypt, decrypt

HOST = "127.0.0.1"
PORT = 5000

name = input("Enter your name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(name.encode())

window = tk.Tk()
window.title("Secure Chat")

chat_area = ScrolledText(window, state="disabled", width=50, height=20)
chat_area.pack(padx=10, pady=10)

msg_entry = tk.Entry(window, width=40)
msg_entry.pack(side=tk.LEFT, padx=10, pady=10)

def display_message(message):
    chat_area.config(state="normal")
    chat_area.insert(tk.END, message + "\n")
    chat_area.config(state="disabled")
    chat_area.yview(tk.END)

def receive():
    while True:
        try:
            message = decrypt(client.recv(1024))
            window.after(0, display_message, message)
        except:
            break

def send():
    message = msg_entry.get()
    msg_entry.delete(0, tk.END)

    if message.startswith("/"):
        client.send(encrypt(message))
    else:
        full = f"{name} : {message}"
        client.send(encrypt(full))

send_button = tk.Button(window, text="Send", command=send)
send_button.pack(side=tk.RIGHT, padx=10)

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

window.mainloop()
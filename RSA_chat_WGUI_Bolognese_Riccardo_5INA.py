import socket
import threading
import rsa
import tkinter as tk
from tkinter import scrolledtext

public_key, private_key = rsa.newkeys(1024)
public_partner = None
client = None


def sending_messages():
    message = message_entry.get()
    if message:
        encrypted_message = rsa.encrypt(message.encode(), public_partner)
        client.send(encrypted_message)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "Tu: " + message + "\n")
        chat_area.config(state=tk.DISABLED)
        message_entry.delete(0, tk.END)


def receiving_messages():
    while True:
        try:
            message = client.recv(1024)
            if message:
                decrypted_message = rsa.decrypt(message, private_key).decode()
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, "Partner: " + decrypted_message + "\n")
                chat_area.config(state=tk.DISABLED)
        except Exception as e:
            print("Errore nella ricezione del messaggio:", e)
            break


def setup_connection():
    global client, public_partner

    choice = choice_var.get()

    if choice == "1": 
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 9999))
        server.listen()
        chat_area.insert(tk.END, "In attesa di connessioni...\n")
        client, _ = server.accept()
        chat_area.insert(tk.END, "Connessione stabilita.\n")

        client.send(public_key.save_pkcs1("PEM"))
        public_partner_data = client.recv(1024)
        public_partner = rsa.PublicKey.load_pkcs1(public_partner_data)

    elif choice == "2": 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("localhost", 9999))
        client.send(public_key.save_pkcs1("PEM"))

        public_partner_data = client.recv(1024)
        public_partner = rsa.PublicKey.load_pkcs1(public_partner_data)

    else:
        chat_area.insert(tk.END, "Scelta non valida. Uscita.\n")
        return

  
    threading.Thread(target=receiving_messages, daemon=True).start()


root = tk.Tk()
root.title("Chat Sicura")


chat_area = scrolledtext.ScrolledText(root, height=20, width=50)
chat_area.pack(padx=10, pady=10)
chat_area.config(state=tk.DISABLED)


message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5)


send_button = tk.Button(root, text="Invia", width=10, command=sending_messages)
send_button.pack(pady=5)

choice_var = tk.StringVar(value="1")
host_radio = tk.Radiobutton(root, text="Host", variable=choice_var, value="1")
host_radio.pack(pady=5)
client_radio = tk.Radiobutton(root, text="Client", variable=choice_var, value="2")
client_radio.pack(pady=5)


start_button = tk.Button(root, text="Avvia Connessione", command=setup_connection)
start_button.pack(pady=5)

root.mainloop()

import socket
import threading
import rsa


public_key, private_key = rsa.newkeys(1024)
public_partner = None


def sending_messages(c):
    while True:
        message = input("Tu: ") 
        encrypted_message = rsa.encrypt(message.encode(), public_partner)
        c.send(encrypted_message)
        print("Tu: " + message)
       
     


def receiving_messages(c):
    while True:
        try:
            message = c.recv(1024)
            if message:
                decrypted_message = rsa.decrypt(message, private_key).decode()
                print("\nPartner: " + decrypted_message)
                print("Tu: ", end="", flush=True)  
        except Exception as e:
            print("Errore nella ricezione del messaggio:", e)
            break
            


choice = input("Vuoi hostare (1) o connetterti (2): ")

if choice == "1":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.10.12.15", 9999))  
    server.listen()

    print("In attesa di connessioni...")
    client, _ = server.accept()
    print("Connessione stabilita.")

 
    client.send(public_key.save_pkcs1("PEM"))


    public_partner_data = client.recv(1024)
    public_partner = rsa.PublicKey.load_pkcs1(public_partner_data)

elif choice == "2":
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("10.10.12.15", 9999)) 
    client.send(public_key.save_pkcs1("PEM"))

    public_partner_data = client.recv(1024)
    public_partner = rsa.PublicKey.load_pkcs1(public_partner_data)

else:
    print("Scelta non valida. Uscita.")
    exit()


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()

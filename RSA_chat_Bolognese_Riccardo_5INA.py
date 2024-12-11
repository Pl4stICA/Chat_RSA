import socket
import threading
import random
from sympy import isprime
import json

############################
##   GEN.  NUMERI PRIMI   ##
############################

def generate_large_prime(length):
    while True:
        candidate = random.getrandbits(length * 4)
        if isprime(candidate):
            return candidate
        
############################
## MASSIMO COMUN DIVISORE ##
############################

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

############################
##     MODULO INVERSO     ##
############################

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

############################
##          CHIAVI        ##
############################

def generate_keys(bits):
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = mod_inverse(e, phi)
    return (e, n), (d, n)  # chiavi

############################
##         CIFRATURA      ##
############################

def encrypt(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

############################
##         DECIFRATURA    ##
############################

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted

public_key = None
private_key = None
public_partner = None

def sending_messages(c):
    while True:
        message = input("Tu: ")
        encrypted_message = encrypt(message, public_partner)
        
      
        c.send(json.dumps(encrypted_message).encode())  
        print("Tu: " + message)

def receiving_messages(c):
    buffer = b""
    while True:
        try:
            data = c.recv(1024)
            if not data:
                break 

            buffer += data 
            try:
                
                message = buffer.decode()
                encrypted_message = json.loads(message)  
                decrypted_message = decrypt(encrypted_message, private_key)
                print("\nPartner: " + decrypted_message)
                print("Tu: ", end="", flush=True)
                buffer = b""  
            except json.JSONDecodeError:
              
                continue
        except Exception as e:
            print("Errore nella ricezione del messaggio:", e)
            break

choice = input("Vuoi hostare (1) o connetterti (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()
    print("In attesa di connessioni...")
    client, _ = server.accept()
    print("Connessione stabilita.")

    public_key, private_key = generate_keys(300)  

    client.send(json.dumps(public_key).encode())  

    public_partner_data = client.recv(1024)
    public_partner = json.loads(public_partner_data.decode())  
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    public_key, private_key = generate_keys(300)  

    client.send(json.dumps(public_key).encode()) 

    public_partner_data = client.recv(1024)
    public_partner = json.loads(public_partner_data.decode())  

else:
    print("Scelta non valida. Uscita.")
    exit()


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()

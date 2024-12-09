import socket
import threading
import rsa

choice = input("Vuoi hostare (1) o connetterti (2): ")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.10.12.19", 9999)) #Ip del computer, cambiare se è un computer diverso
    server.listen()
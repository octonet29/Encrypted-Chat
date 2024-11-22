import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    # Host
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("172.16.10.117", 9999))
    server.listen()

    print("Baglanshyga garashyar...")
    client, _ = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    print("Baglanylddynyz!")

elif choice == "2":
    # Connect to the host
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = input("Ip salgy: ")
    client.connect((host_ip, 9999))

    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    print("Hosta birikdi!")

else:
    exit()

def sending_messages(sock):
    while True:
        message = input("")
        # sock.send(rsa.encrypt(message.encode(), public_partner))
        sock.send(message.encode())
        print("Siz: " + message)

def receiving_messages(sock):
    while True:
        try:
           # data = rsa.decrypt(sock.recv(1024), private_key).decode()
            data = (sock.recv(1024).decode())
            if not data:
                print("Baglanshyk kesildi.")
                break
            print("Partnyor: " + data)
        except Exception as e:
            print(f"Error: {e}")
            break

if choice == "1":
    threading.Thread(target=sending_messages, args=(client,)).start()
    threading.Thread(target=receiving_messages, args=(client,)).start()
elif choice == "2":
    threading.Thread(target=sending_messages, args=(client,)).start()
    threading.Thread(target=receiving_messages, args=(client,)).start()

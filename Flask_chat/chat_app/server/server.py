from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

#GOLBAL VARIABLES
HOST = 'localhost'
PORT = 9000
BUFFSIZ = 512
ADDR = (HOST, PORT)

#GLOBAL VARIABLES
persons = []

# setting up the server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    """
    send new message to all clients

    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, "utf8") + msg)
        except Exception as e:
            print("[failure]", e)

def client_communication(person):
    """
    handling the incoming messages
    """
    run = True
    client = person.client

    name = client.recv(BUFFSIZ).decode("utf8")
    person.set_name(name)

    msg = bytes("{} joined the chat".format(name), "utf8")
    broadcast(msg, "") # broadcast welcome msg

    while run:
        msg = client.recv(BUFFSIZ)
        if msg == bytes("{quit}", "utf8"):
            client.close()
            persons.remove(person)
            broadcast(bytes("{} has left the room".format(name),"utf8"), "")
 
            print("[DISCONNECTED] {} ".format(name))
            break
        else:
            broadcast(msg, name + ": ")
            print("{}:".format(name), msg.decode("utf8"))

def wait_for_connections():
    """
    WAIT for connections
    """
    run = True

    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print("[CONNECTION]: {} connected to the server at {}".format(addr, time.time()))

            Thread(target=client_communication, args=(person,)).start()

        except Exception as e:
            print('[failure]',e)
            break
    print("[SERVER CRASHED]")


if __name__ == "__main__":
    SERVER.listen(5) # listen for max connections
    print("[STARTED] waiting for the connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close() 
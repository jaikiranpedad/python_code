from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client():
    """
    For the communication 
    """
    #GOLBAL VARIABLES
    HOST = 'localhost'
    PORT = 9000
    BUFFSIZ = 512
    ADDR = (HOST, PORT)

    def __init__(self, name):
        """
        initiating the client
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.msgs = []
        recieve_thread = Thread(target=self.recieve_msg)
        recieve_thread.start()
        self.send_message(name)
        self.lock = Lock()
    
    def recieve_msg(self):
        """
        recieving the messages from the server
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFSIZ).decode()
                self.lock.acquire()
                self.msgs.append(msg)
                self.lock.release()

            except Exception as e:
                print("[failure]", e)
                break
    
    def send_message(self, msg):
        """
        send messages to the server
        : param  msg: str
        : return None
        """
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)
    
    def get_messages(self):
        """
        return the entire message strong
        """
        messages_copy = self.msgs[:]

        self.lock.acquire()
        self.msgs =[]
        self.lock.release()

        return messages_copy
    
    def disconnect(self):
        self.send_message("{quit}") 
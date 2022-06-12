import socket
import threading
import pickle
import time

SERVER_IP = socket.gethostname()
PORT = 2222
DATA_SIZE = 1024

class ThreadRecv(threading.Thread):
    def __init__(self,client,  client_socket, screen, id):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.screen = screen
        self.flag = True
        self.id = id
        self.client = client

    def run(self):
        global client
        while self.flag:
            try:
                message = self.client_socket.recv(8192)
                message = self.un_pick(message)
                if message != "Exception":
                    if hasattr(message, 'ascii'):
                        if message.ascii == 's':
                            self.screen.addsprite(message)
                        elif message.ascii == 'b':
                            self.screen.addgun(message)
                    else:
                        if message == int(self.id):
                            self.screen.hp_down(message)
                        if message == "start":
                            print("starting")
                            self.client.start = True

            except Exception as e:
                print(e)
                self.flag = False

    def un_pick(self, message):
        try:
            message = pickle.loads(message)
            return message
        except Exception as e:
            print("Unpicking exception")
            return "Exception"



class ClientGame(object):
    def __init__(self, screen):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_IP, PORT))
            self.screen = screen
            self.id = self.client_socket.recv(1024).decode()
            self.start = False
            print(self.id)
            ThreadRecv(self, self.client_socket, self.screen, self.id).start()
        except Exception as e:
            print(e)


    def send_message(self, message):
        self.client_socket.send(pickle.dumps(message))

    def close_client(self):
        self.client_socket.close()



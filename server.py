import socket
import threading
import pickle

IP = "0.0.0.0"
PORT = 2222
clients_list = []

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.flag = True
        self.conn_counter = 1

    def startup(self):
        """
        create a server waiting for clients to answer a quiz.
        for every client he open private communicate thread and add him to list of clients.
        """
        try:
            self.server_socket.bind((IP, PORT))
            self.server_socket.listen()
            InputThread().start()
        except Exception as e:
            print(e)

    def run(self):
        global clients_list
        while self.flag:
            client_socket, client_address = self.server_socket.accept()
            print(f"{client_address} connected")
            message = str(self.conn_counter)
            client_socket.send(message.encode())
            clients_list.append(client_socket)
            self.conn_counter += 1
            ProducerThread(client_socket, client_address).start()


class ProducerThread(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address

    def run(self):
        flag = True
        while flag:
            try:
                message = self.client.recv(8192)
                self.send_all(message)
            except Exception as e:
                print(f"{self.address} client has disconnected")
                flag = False

    def send_all(self, message):
        global clients_list
        for client in clients_list:
            if client != self.client:
                client.send(message)

class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global clients_list
        message = ""
        while message != "start":
            print("Enter start to start the game")
            message = input()
            print(message)
        for client in clients_list:
            client.send(pickle.dumps(message))

def main():
    server = Server()
    print("Server is up and running")
    server.startup()
    server.run()


if __name__ == "__main__":
    main()

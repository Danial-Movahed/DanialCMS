from .main import *

conn = []
id = 0

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class client_thread(threading.Thread):
    def __init__(self, clientsocket, id, userList):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientsocket.setblocking(0)
        self.id = id
        self.connected = True
        self.loggedInUser = None
        self.userList = userList

    def run(self):
        while self.connected:
            try:
                self.clientsocket.send("keep-alive".encode())
                if self.loggedInUser == None:
                    ready = select.select([self.clientsocket], [], [], 10)
                    if ready[0]:
                        data = self.clientsocket.recv(4096)
                        print(str(self.id)+" "+data.decode()+" Check login!")
                        data = data.decode().split(" ")
                        for u in self.userList:
                            if u.Username == data[0] and u.Password == data[1]:
                                self.clientsocket.send("Ok".encode())
                                print("Ok")
                                self.loggedInUser = u
                        if data[0] == "public" and data[1] == "7c34faf3351e3df0d7958ecf36b094a5f3e1b677907cae2469c1ac1c22abefbe":
                            self.clientsocket.send("Ok".encode())
                            print("Ok")
                            u=User()
                            u.Username="public"
                            u.Password="public"
                            u.isAdmin=False
                            self.loggedInUser = u
                        if self.loggedInUser == None:
                            self.clientsocket.send("No".encode())
                            print("No")
                else:
                    ready = select.select([self.clientsocket], [], [], 5)
                    if ready[0]:
                        data = self.clientsocket.recv(4096)
                        print(str(self.id)+" "+data.decode())
            except:
                self.connected = False
                global id,conn
                id-=1
                conn.remove(self)
                print(conn)

def runServer(userList):
    global id,conn
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("", 4411))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        print("accepted!")
        conn.append(client_thread(clientsocket,id,userList))
        conn[id].start()
        id += 1

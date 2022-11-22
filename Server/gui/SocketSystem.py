from .main import *
from time import sleep

conn = []
userList = []
postList = []
rss = ""
id = 0


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


class RSSServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global rss
        self.send_response(200)
        self.send_header("Content-type", "application/rss+xml")
        self.end_headers()
        self.wfile.write(rss)


class client_thread(threading.Thread):
    def __init__(self, clientsocket, id, blogTitle):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientsocket.setblocking(0)
        self.id = id
        self.blogTitle = blogTitle
        self.connected = True
        self.loggedInUser = None
        self.whatWrk = "f"

    def run(self):
        global userList, postList, whatWrk
        while self.connected:
            try:
                if self.loggedInUser == None:
                    ready = select.select([self.clientsocket], [], [], 10)
                    if ready[0]:
                        data = self.clientsocket.recv(4096)
                        print(str(self.id)+" "+data.decode()+" Check login!")
                        data = data.decode().split(" ")
                        for u in userList:
                            if u.Username == data[0] and u.Password == data[1]:
                                self.clientsocket.send(("Ok "+self.blogTitle).encode())
                                sleep(1)
                                print("Ok")
                                self.loggedInUser = u
                        if data[0] == "public" and data[1] == "7c34faf3351e3df0d7958ecf36b094a5f3e1b677907cae2469c1ac1c22abefbe":
                            self.clientsocket.send(("Ok "+self.blogTitle).encode())
                            sleep(1)
                            print("Ok")
                            u = User()
                            u.Username = "public"
                            u.Password = "public"
                            u.isAdmin = False
                            self.loggedInUser = u
                        if self.loggedInUser == None:
                            self.clientsocket.send("No".encode())
                            sleep(1)
                            print("No")
                else:
                    if self.whatWrk == "f":
                        self.clientsocket.send("FS".encode())
                        sleep(0.1)
                        for p in postList:
                            if self.loggedInUser.Username in p.WhoCanRead.split(" "):
                                tmp = pickle.dumps(p)
                                self.clientsocket.send(tmp)
                                sleep(0.1)
                        self.clientsocket.send("Done".encode())
                        sleep(0.1)
                        self.whatWrk = ""
                    elif self.whatWrk == "n":
                        if self.loggedInUser.Username in postList[-1].WhoCanRead.split(" "):
                            self.clientsocket.send("NP".encode())
                            sleep(0.1)
                            tmp = pickle.dumps(postList[-1])
                            self.clientsocket.send(tmp)
                            sleep(0.1)
                            self.clientsocket.send("Done".encode())
                            sleep(0.1)
                        self.whatWrk = ""
                    elif self.whatWrk == "e":
                        self.clientsocket.send("EP".encode())
                        sleep(0.1)
                        for p in postList:
                            if self.loggedInUser.Username in p.WhoCanRead.split(" "):
                                tmp = pickle.dumps(p)
                                self.clientsocket.send(tmp)
                                sleep(0.1)
                        self.clientsocket.send("Done".encode())
                        sleep(0.1)
                        self.whatWrk = ""
                    elif self.whatWrk == "d":
                        self.clientsocket.send("DP".encode())
                        sleep(0.1)
                        for p in postList:
                            if self.loggedInUser.Username in p.WhoCanRead.split(" "):
                                tmp = pickle.dumps(p)
                                self.clientsocket.send(tmp)
                                sleep(0.1)
                        self.clientsocket.send("Done".encode())
                        sleep(0.1)
                        self.whatWrk = ""
                    

                    ready = select.select([self.clientsocket], [], [], 1)
                    if ready[0]:
                        data = self.clientsocket.recv(4096)
                        data=data.decode()
                        print(data)
                        for i in range(len(postList)):
                            if postList[i].Title == data:
                                try:
                                    postList[i].ReadBy+=", "+self.loggedInUser.Username
                                except:
                                    postList[i].ReadBy=self.loggedInUser.Username

                self.clientsocket.send("keep-alive".encode())
                sleep(0.1)
            except:
                self.connected = False
                global id, conn
                id -= 1
                conn.remove(self)
                print(conn)


def runServer(blogTitle):
    global id, conn, userList
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("", 4523))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        print("accepted!")
        conn.append(client_thread(clientsocket, id, blogTitle))
        conn[id].start()
        id += 1

def runRSSServer():
    webServer = HTTPServer(("", 8080), RSSServer)
    webServer.serve_forever()
from .main import *
from time import sleep

conn = []
blogList = []
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
    def __init__(self, clientsocket, id):
        threading.Thread.__init__(self)
        self.clientsocket = clientsocket
        self.clientsocket.setblocking(0)
        self.id = id
        self.connected = True
        self.whatWrk = "f"

    def run(self):
        global blogList
        while self.connected:
            try:
                if self.whatWrk == "f":
                    self.clientsocket.send("FS".encode())
                    sleep(0.5)
                    for b in blogList:
                        tmp = pickle.dumps(b)
                        self.clientsocket.send(tmp)
                        sleep(0.5)
                    self.clientsocket.send("Done".encode())
                    sleep(0.5)
                    self.whatWrk = ""
                if self.whatWrk == "n":
                    self.clientsocket.send("NB".encode())
                    sleep(0.5)
                    tmp = pickle.dumps(blogList[-1])
                    self.clientsocket.send(tmp)
                    sleep(0.5)
                    self.clientsocket.send("Done".encode())
                    sleep(0.5)
                    self.whatWrk = ""
                self.clientsocket.send("keep-alive".encode())
                sleep(0.5)
            except:
                self.connected = False
                global id, conn
                id -= 1
                conn.remove(self)
                print(conn)


def runServer():
    global id, conn, userList
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(("", 4524))
    serversocket.listen(5)
    while True:
        (clientsocket, address) = serversocket.accept()
        print("accepted!")
        conn.append(client_thread(clientsocket, id))
        conn[id].start()
        id += 1

def runRSSServer():
    webServer = HTTPServer(("", 8080), RSSServer)
    webServer.serve_forever()
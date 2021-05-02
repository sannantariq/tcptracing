import socket
import socketserver
import sys
import time

RECV_BUFSIZE = 1024 * 100
WRITE_DATA_SIZE = 1024 * 10000
WRITE_BUF_SIZE = 1024 * 10
PORT=8080

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(RECV_BUFSIZE)
        while self.data:
            self.data = self.request.recv(RECV_BUFSIZE)
        # print("{} wrote:".format(self.client_address[0]))
        # print(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

def serve():
    HOST, PORT = "0.0.0.0", 8080

    # Create the server, binding to localhost on port 8080
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()


def client(dst_host='localhost', dst_port=8080):
    HOST, PORT = dst_host, dst_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(b'a' * WRITE_DATA_SIZE)

def long_lasting_client(dst_host='localhost', dst_port=8080):
    HOST, PORT = dst_host, dst_port
    MAX_TIME = 5
    PAUSE_TIME = 1.4
    SEND_SIZE = 1024 * 1000
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        start = time.time()
        while time.time() - start < MAX_TIME:
            client.sendall(b'a' * (SEND_SIZE))
            time.sleep(PAUSE_TIME)

def pausing_client(dst_host='localhost', dst_port=8080):
    HOST, PORT = dst_host, dst_port
    PAUSE_TIME = 2

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(b'a' * (WRITE_DATA_SIZE//2))
        time.sleep(PAUSE_TIME)
        client.sendall(b'a' * (WRITE_DATA_SIZE//2))

def app_limited_client(dst_host='localhost', dst_port=8080):
    HOST, PORT = dst_host, dst_port
    SMALL_SEND_SIZE = 130 * 1024
    INITIAL_SEND = WRITE_DATA_SIZE // 10
    MIDDLE_SEND = INITIAL_SEND
    APP_PACERATE = 0.2
    app_limited_send = WRITE_DATA_SIZE - INITIAL_SEND - MIDDLE_SEND

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client.sendall(b'a' * (INITIAL_SEND))
        remaining_bytes = app_limited_send
        send_paced(client, remaining_bytes//2, SMALL_SEND_SIZE, APP_PACERATE)
        client.sendall(b'a' * (MIDDLE_SEND))
        send_paced(client, remaining_bytes//2, SMALL_SEND_SIZE, APP_PACERATE)

def send_paced(sock, nbytes, send_size, sleep_time):
    while nbytes > 0:
        bytes_sent = sock.send(b'a' * (send_size))
        nbytes -= bytes_sent
        time.sleep(sleep_time)

def variant_client_1(dst_host='localhost', dst_port=8080):
    HOST, PORT = dst_host, dst_port
    SMALL_SEND_SIZE = 100 * 1024
    BIG_SEND_SIZE = 500 * 1024
    APP_PACERATE = 0.25
    # app_limited_send = WRITE_DATA_SIZE - INITIAL_SEND - MIDDLE_SEND
    remaining_bytes = WRITE_DATA_SIZE

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        while remaining_bytes > 0:
            client.sendall(b'a' * (BIG_SEND_SIZE))
            send_paced(client, SMALL_SEND_SIZE * 5, SMALL_SEND_SIZE, APP_PACERATE)
            remaining_bytes -= (BIG_SEND_SIZE + (SMALL_SEND_SIZE * 5))

def variant_client_2():
    """
    This client is bursty
    """

def variant_client_3():
    """
    This client starts off as app limited
    and later converts to bandwidth limited
    """

def variant_client_4():
    """
    This client has very little difference between
    the throughputs during app limited and
    bandwidth limited periods
    """

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {__file__} server|client [destination host] [port]")
        sys.exit(0)

    if len(sys.argv) > 2:
        dst_host = sys.argv[2]
        if len(sys.argv) > 3:
            dst_port = sys.argv[3]

    if sys.argv[1] == 'server':
        serve()
    elif sys.argv[1] == 'client':
        client(dst_host=dst_host, dst_port=dst_port)
    elif sys.argv[1] == 'pauser':
        pausing_client(dst_host=dst_host, dst_port=dst_port)
    elif sys.argv[1] == 'long':
        long_lasting_client(dst_host=dst_host, dst_port=dst_port)
    elif sys.argv[1] == 'app':
        app_limited_client(dst_host=dst_host, dst_port=dst_port)
    elif sys.argv[1] == 'var1':
        variant_client_1(dst_host=dst_host, dst_port=dst_port)
    else:
        print("Invalid roll")
        sys.exit(0)


if __name__ == "__main__":
    main()
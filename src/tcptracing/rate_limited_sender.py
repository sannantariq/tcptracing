

import socket
import socketserver
import sys
import time


MTU = 1360

class TokenBucket:

    def __init__(self, tokens, time_unit, forward_callback, drop_callback):
        self.tokens = tokens
        self.time_unit = time_unit
        self.forward_callback = forward_callback
        self.drop_callback = drop_callback
        self.bucket = tokens
        self.last_check = time.time()

    def handle(self, packet):
        current = time.time()
        time_passed = current - self.last_check
        self.last_check = current

        self.bucket = self.bucket + \
            time_passed * (self.tokens / self.time_unit)

        if (self.bucket > self.tokens):
            self.bucket = self.tokens

        if (self.bucket < 1):
            self.drop_callback(packet)
        else:
            self.bucket = self.bucket - 1
            self.forward_callback(packet)



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
        print(f"Serving on {HOST}:{PORT}. Press Ctrl+C to interrupt.")
        server.serve_forever()

def client(dst_host='localhost', dst_port=8080, sendtime=10, rate=1000000):
    HOST, PORT = dst_host, dst_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

        def snd_packet(p):
          client.sendall(b'a' * MTU)

        def drop_packet(p):
          pass

        print(f"Connecting to {HOST}:{PORT}")
        client.connect((HOST, PORT))

        rate_to_send = rate//(MTU*8)
        print(f"Writing at rate {rate} bps for {sendtime} seconds")
        tb = TokenBucket(rate_to_send, 1, snd_packet, snd_packet, drop_packet)
        start_time = time.time()
        while time.time() < sendtime + start_time:
            tb.handle("")
        print(f"Done.")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {__file__} server|client host port rate(bps) duration(seconds)")
        sys.exit(0)        

    if sys.argv[1] == 'server':
        serve()
    elif sys.argv[1] == 'client':
        print("Executing basic Client")
        dst_host = sys.argv[2]
        dst_port = int(sys.argv[3])
        send_rate = float(sys.argv[4])
        send_duration = float(sys.argv[5])
        client(dst_host=dst_host, dst_port=dst_port)
    else:
        print("Invalid roll")
        sys.exit(0)
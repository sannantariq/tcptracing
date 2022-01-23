

import socket
import socketserver
import sys
import time


MTU = 1360
CHUNKS_SENT = 0

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

def client(dst_host='localhost', dst_port=8080, sendtime=40, chunksize=2000000, delay=0.75):
    HOST, PORT = dst_host, dst_port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        

        def snd_chunk(p):
            CHUNKS_SENT += 1
            client.sendall(b'a' * chunksize)
            time.sleep(delay)

        print(f"Connecting to {HOST}:{PORT}")
        client.connect((HOST, PORT))

        print(f"Writing {chunksize} bytes with delay of {delay} seconds for {sendtime} seconds")
        start_time = time.time()
        while time.time() < sendtime + start_time:
            snd_chunk("")
        print(f"Done. {CHUNKS_SENT} chunks sent.")

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {__file__} server|client host port chunksize(bytes) delay(seconds) duration(seconds)")
        sys.exit(0)        

    if sys.argv[1] == 'server':
        serve()
    elif sys.argv[1] == 'client':
        print("Executing basic Client")
        dst_host = sys.argv[2]
        dst_port = int(sys.argv[3])
        chunksize = int(sys.argv[4])
        delay = float(sys.argv[5])
        send_duration = float(sys.argv[6])
        client(dst_host=dst_host, dst_port=dst_port, sendtime=send_duration, chunksize=chunksize, delay=delay)
    else:
        print("Invalid roll")
        sys.exit(0)

if __name__ == "__main__":
  main()
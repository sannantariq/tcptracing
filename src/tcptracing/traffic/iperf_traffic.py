

class IperfPair:
    def __init__(self, server_host, server_port, sender_cc_algo) -> None:
        self.server_host = server_host
        self.server_port = server_port
        self.sender_cc_algo = sender_cc_algo

    def start_server(self):
        """
        Start the iperf server
        """
        pass

    def stop_server(self):
        """
        Stop the iperf server
        """
        pass

    def start_sender(self, send_time=-1):
        """
        Start the iperf sender that sender for send_time seconds
        """
        pass

    def stop_sender(self):
        """
        Stops the iperf sender
        """
        pass
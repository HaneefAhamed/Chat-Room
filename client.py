import threading
import time

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc


import argparse

# Adding arguments to accept name, port, ip_address for client
parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, help="id of clients")
parser.add_argument('--port', type=str, help='port id of connection')
parser.add_argument('--ip_address', type=str, help='ip address of connection', default="localhost")
parser.add_argument('--testing_mode', action='store_true', help="Testing mode")
args = parser.parse_args()

class Client:

    def __init__(self, u: str, port, ip_address, testing_mode):

        self.username = u
        self.port = port
        self.ip_address = ip_address
        self.testing_mode = testing_mode

        # create a gRPC channel + stub
        channel = grpc.insecure_channel(str(self.ip_address) + ':' + str(self.port))
        self.conn = rpc.ChatServerStub(channel)

        self.chats = []
        self.lastIndex = -1
        
        # create new listening thread for when new message streams come in
        thread_a = threading.Thread(target=self.listen_messages)
        thread_a.daemon = True
        thread_a.start()

        # Create a listening thread when the user sends in a message to the server
        thread_b = threading.Thread(target=self.setup_message)
        thread_b.daemon = True
        thread_b.start()
        
        while True:
            time.sleep(1)

    def listen_messages(self):
        
        # Test each message coming from the server and print it in the user's screen
        for note in self.conn.ChatStream(chat.User(name=self.username)):
                print("Recieved from Server {}: [{}] {}".format(self.username, note.name, note.message))

    # Make chat.Note messages to sent to the server
    def make_messages(self, message):
        self.chats.append(message)
        self.lastIndex += 1 
        n = chat.Note()
        n.name = self.username
        n.message = message
        return n
    
    def setup_message(self):
        # Implemented a testing mode to accept an array of static strings instead of user input
        lastIndex = 0
        if self.testing_mode:
            generator = self.bot_message
        else:
            generator = self.send_message

        for response in generator():
            conf = self.conn.SendNote(response)
            if conf.value:
                print("Sent to Server {}: [{}] {}".format(self.username, self.username, self.chats[self.lastIndex]))

    def bot_message(self):
        # Static test to send in testing mode
        messages = [self.make_messages("Welcome " + self.username)]
        for msg in messages:
            yield msg

    def send_message(self):

        #  Takes user input and send it to the server. 
        while True:
            message = input()
            if message != '':
                yield self.make_messages(message)


if __name__ == '__main__':
    # Start up the client with the required arguments.
    c = Client(args.name, args.port, args.ip_address, args.testing_mode)
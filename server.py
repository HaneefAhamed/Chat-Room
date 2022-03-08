from concurrent import futures

import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--names', type=str, help="names of clients", nargs="+")
parser.add_argument('--port', type=str, help="Port address of connection")
args = parser.parse_args()


class ChatServer(rpc.ChatServerServicer):  # inheriting here from the protobuf rpc file which is generated

    def __init__(self, names):
        # List with all the chat history
        self.chats = []
        self.groups = names
        print('Starting server connection on Port ', args.port, ' Welcome the group, with members ', self.groups)

    # The stream which will be used to send new messages to clients
    def ChatStream(self, request_iterator: chat.User, context):
        # This is a response-stream type call. This means the server can keep sending messages
        # Every client opens this connection and waits for server to send new messages
        lastindex = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True:
            # Check if there are any new messages
            while len(self.chats) > lastindex:
                n = self.chats[lastindex]
                lastindex += 1
                if request_iterator.name != n.name and request_iterator.name in self.groups and n.name in self.groups:
                    yield n

    def SendNote(self, request: chat.Note, context):
        # This method is called when a clients sends a Message to the server
        # Add it to the chat history
        self.chats.append(request)
        return chat.Confirmation(
            value=True)  # It is necessary to return something. We simply return an empty message as required by the protobuf language.


if __name__ == '__main__':
    # when there are ten customers connected, the number of workers is equivalent to the number of threads that can
    # be opened at the same time.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # create a gRPC server
    rpc.add_ChatServerServicer_to_server(ChatServer(args.names), server)  # register the server to gRPC
    # gRPC basically manages all the threading and server responding logic, which is perfect!
    server.add_insecure_port('[::]:' + str(args.port))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    server.wait_for_termination()

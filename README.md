# Chat-Room

In this project, we will implement a simple client-server "group chat" system with n clients/configuration. With Alice, Bob, and Chad (the three client 
processes).

## Requirements: 

1. The clients should be able to send/receive messages from the server.
2. The server keeps track of the clients that have received the messages and only sends the unread messages.

## Test Cases:

1. Alice sends a single message. Chad and Bob come online after a 5 second delay and receives all messages from Alice. (Log the message in the console)
2. Alice, Bob, and Chad are online. Bob sends a message to all; Chad and Alice receive the message (The sender Bob doesn’t receive the message from the server). 
3. Alice sends a message to all; Bob and Chad receive it (but not Alice). Doug, not part of the group, joins the server but receives no message.

## Implementation:


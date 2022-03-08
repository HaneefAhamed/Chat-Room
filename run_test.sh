#!/bin/bash

echo "After each login, we show who sent the message, and who received the message"
echo "Starting the server"

python3 -u server.py --names Alice Bob Chad --port 5080 &
echo $! > SERVER_PID

sleep 2 && echo " ....................................................."
sleep 5
sleep 2 && echo "Alice joined the server and the group"

python3 -u client.py --name Alice --port 5080 --testing_mode &
echo $! > ALICE_PID

sleep 2 && echo " ....................................................."
sleep 5
sleep 2 && echo "Bob joined the server and the group"

python3 -u client.py --name Bob --port 5080 --testing_mode &
echo $! > BOB_PID

sleep 2 && echo " ....................................................."
sleep 5
sleep 2 && echo "Chad joined the server and the group"

python3 -u client.py --name Chad --port 5080 --testing_mode &
echo $! > CHAD_PID

sleep 2 && echo " ....................................................."
sleep 5
sleep 2 && echo "Doug joined the sever"

python3 -u client.py --name Doug --port 5080 --testing_mode &
echo $! > DOUG_PID
sleep 5

kill `cat ALICE_PID`
kill `cat BOB_PID`
kill `cat CHAD_PID`
kill `cat DOUG_PID`
kill `cat SERVER_PID`

rm ALICE_PID
rm BOB_PID
rm CHAD_PID
rm DOUG_PID
rm SERVER_PID

exit 1
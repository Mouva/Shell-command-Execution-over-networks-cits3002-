import networkstuff as net

import time

socks = net.start_client(["localhost"])


def incomingPacket(packet):
    print(packet.filename, packet.data)


sendFile = 1

try:
    while True:
        net.poll(incomingPacket)

        if sendFile:
            print("Sending File")
            time.sleep(0.2)

            for packet in net.enpacket("bbbbig"):
                print(packet.asBytes())
                net.send(socks[0], packet)
            sendFile = 0

            print("File sent")

        time.sleep(1)
        print(".")
except KeyboardInterrupt:
    for sock in socks:
        sock.close()

import networkstuff as net


net.start_client(["localhost"])


def incomingPacket(packet):
    print(packet.filename, packet.data)


sendFile = 1

while True:
    net.poll(incomingPacket)

    if sendFile:
        net.enpacket("bbbbig")
        sendFile = 0

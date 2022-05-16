import networkstuff as net


net.start_server()


def incomingPacket(packet):
    print(packet.filename, packet.data)


while True:
    net.poll(incomingPacket)

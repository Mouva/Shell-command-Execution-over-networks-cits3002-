import networkstuff as net
import systemstuff as sus
import time, subprocess

processes = []

def incoming_packet(packet):
    match packet.control:
        case 0: # command cost query
            net.packet(0, "", packet.filesize, sus.getSysPerf(), b"").send(packet.socket)
        case 1: # command
            
        case 2: # file transfer
            net.write_packet(packet)
        case 3: # command result
            pass

    

def main():
    net.start_server()

    while True:
        poll()

def poll():
    net.poll(incoming_packet)

    for process in processes:
        if process.poll():  # Process is done
            stdout, _ = process.communicate()
            processes.remove(process)
            print(stdout)

            net.packet(3, "", 0, 0, b"", )


if __name__ == "__main__":
    main()
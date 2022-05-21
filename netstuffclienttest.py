import networkstuff as net
import sys, subprocess

socks = net.start_client(["localhost"])
processes = []
remote_processes = []


def incomingPacket(packet):
    print(packet.filename, packet.data)

    match packet.control:
        case 0:  # command cost
            pass
        case 1:  # command
            pass
        case 2:  # file transfer
            net.write_packet(packet)


# sendFile = 1

# try:
#     while True:
#         net.poll(incomingPacket)

#         if sendFile:
#             print("Sending File")
#             time.sleep(0.2)

#             for packet in net.enpacket("bbbbig"):
#                 print(packet.asBytes())
#                 net.send(socks[0], packet)
#             sendFile = 0

#             print("File sent")

#         time.sleep(1)
#         print(".")
# except KeyboardInterrupt:
#     for sock in socks:
#         sock.close()


def main():
    path = "Rakefile"
    port = None
    hosts = None

    if len(sys.argv) > 1:
        path = sys.argv[1]

    # Open and parse Rakefile
    with open(path, "r") as r:
        actionsets = []
        currentset = -1

        for line in r.readlines():
            if line.startswith("#"):
                continue
            elif line.endswith(":"):
                currentset += 1
                actionsets.append([])
            elif line.startswith("PORT"):
                port = line.split("=")[-1].strip()
            elif line.startswith("HOSTS"):
                hosts = line.split("=")[-1].split(" ")
            elif line.startswith("\t\trequires"):
                actionsets[currentset][-1].append(line[10:].split(" "))
            elif line.startswith("\tremote-"):
                actionsets[currentset].append([line[8:], True])
            elif line.startswith("\t"):
                actionsets[currentset].append([line[1:], False])
            else:
                print("scomo lost lol")

    net.start_client(hosts, port)

    for actionset in actionsets:
        execute(actionset)


def execute(actionset):
    for i, command in enumerate(actionset):
        if command[1]:  # Run Remotely

            # Determine best server to run command on
            remote_processes.append(net.remoteProcess(i, command[0]))

        else:  # Run Locally
            processes.append(
                subprocess.Popen(
                    command[0],
                    shell=True,
                    capture_output=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
            )

    ready = False
    while not ready:
        ready = poll()  # Poll until everything is ready


def poll():
    net.poll(incomingPacket)

    for process in processes:
        if process.poll():  # Process is done
            stdout, _ = process.communicate()
            processes.remove(process)
            print(stdout)

    if processes:  # Unfinished local processes
        return False

    if remote_processes:  # Unfinished remote processes
        return False

    return True


if __name__ == "__main__":
    main()

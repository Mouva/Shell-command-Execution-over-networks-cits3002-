# 22973676, Adrian Bedford
# 22989775, Oliver Lynch


import networkstuff as net
import sys, subprocess

processes = []
remote_processes = []


def incoming_packet(packet):
    match packet.control:
        case 0:  # command cost
            for process in remote_processes:
                if process.id == packet.filesize:
                    process.candidate(packet)
        case 1:  # command
            pass
        case 2:  # file transfer
            net.write_packet(packet)
        case 3:  # command result
            completed_process = None
            for process in remote_processes:
                if process.id == packet.filesize:
                    completed_process = process
            if completed_process:
                remote_processes.remove(completed_process)
                print(packet.data.decode("utf-8"))


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
            elif not line.strip():
                continue
            elif line.strip().endswith(":"):
                currentset += 1
                actionsets.append([])
            elif line.startswith("PORT"):
                port = line.split("=")[-1].strip()
            elif line.startswith("HOSTS"):
                hosts = line.split("=")[-1].strip().split(" ")
            elif line.replace("    ", "\t").startswith("\t\trequires"):
                actionsets[currentset][-1].append(line[10:].split(" "))
            elif line.replace("    ", "\t").startswith("\tremote-"):
                actionsets[currentset].append([line.strip()[7:], True])
            elif line.replace("    ", "\t").startswith("\t"):
                actionsets[currentset].append([line.strip(), False])
            else:
                print("Could not parse line: ", line)

    # Rakefile finished parsing, start networking
    net.start_client(hosts, port)

    for actionset in actionsets:
        execute(actionset)


def execute(actionset):
    for i, command in enumerate(actionset):
        if command[1]:  # Run Remotely

            # Determine best server to run command on,
            # the remote process class will determine the
            # correct server and run the command automatically
            remote_processes.append(net.remoteProcess(i, command[0]))

        else:  # Run Locally
            processes.append(
                subprocess.Popen(
                    command[0],
                    shell=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )  # Non-blocking
            )

    ready = False
    while not ready:
        ready = poll()  # Poll until everything is ready


def poll():
    net.poll(incoming_packet)  # Read and write to/from network

    for process in processes:
        if process.poll() != None:  # Process is done
            stdout, _ = process.communicate()
            processes.remove(process)
            print(stdout)

    if processes:  # Unfinished local processes
        return False

    if remote_processes:  # Unfinished remote processes
        return False

    return True  # Not waiting on any local or remote processes


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye. ")
    finally:
        net.close()


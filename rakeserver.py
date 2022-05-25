# 22973676, Adrian Bedford
# 22989775, Oliver Lynch


import networkstuff as net
import systemstuff as sus
import subprocess

processes = {}
process_sock = {}


def incoming_packet(packet):
    match packet.control:
        case 0:  # command cost query
            net.packet(0, "", packet.filesize, sus.getSysPerf(), b"").send(
                packet.socket
            )
        case 1:  # command
            process_sock[packet.filesize] = packet.socket
            processes[packet.filesize] = subprocess.Popen(
                packet.data.decode("utf-8"),
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        case 2:  # file transfer
            net.write_packet(packet)
        case 3:  # command result
            pass


def main():
    net.start_server()

    while True:
        poll()


def poll():
    net.poll(incoming_packet)

    completed_processes = []
    for pid, process in processes.items():
        if process.poll() != None:  # Process is done
            stdout, _ = process.communicate()
            completed_processes.append(pid)

            net.packet(
                3,
                "",
                pid,
                0,
                stdout.encode("utf-8"),
            ).send(process_sock[pid])

            process_sock.pop(pid)

    for completed_process in completed_processes:
        processes.pop(completed_process)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye. ")
    finally:
        net.close()

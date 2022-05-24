# 22973676, Adrian Bedford
# 22989775, Oliver Lynch

import subprocess
import re

# Matches CPU usage variables from top
cpuUsageRE = re.compile(
    r"^CPU usage: (?P<cpuUser>[0-9.]+)% user, (?P<cpuSys>[0-9.]+)% sys, (?P<cpuIdle>[0-9.]+)% idle.*$",
    re.M,
)

# Matches memory usage variables from top
memUsageRE = re.compile(
    r"^PhysMem: (?P<memUsed>\d+). used \((?P<memWired>\d+). wired\), (?P<memUnused>\d+). unused\..*$",
    re.M,
)

# Gets current usage statistics and returns a single averaged int
def getSysPerf():
    # Run top to determine system usage
    perfProc = subprocess.run(["top", "-l", "1", "-n", "0"], capture_output=True)

    if not perfProc.returncode:
        cpuPerc = 0
        memPerc = 0

        perf = perfProc.stdout.decode("utf-8")

        cpuMatch = cpuUsageRE.search(perf)
        memMatch = memUsageRE.search(perf)

        if cpuMatch:
            cpuPerc = 100 - float(cpuMatch.group("cpuIdle"))

        if memMatch:
            memPerc = (
                float(memMatch.group("memUsed"))
                / (
                    float(memMatch.group("memUsed"))
                    + float(memMatch.group("memUnused"))
                )
            ) * 100

        if cpuMatch and memMatch:
            totalPerf = (cpuPerc + memPerc) / 2
        elif cpuMatch:
            totalPerf = cpuPerc
        elif memMatch:
            totalPerf = memMatch
        else:
            totalPerf = 100

        return int(totalPerf)
    return 100


if __name__ == "__main__":
    print(getSysPerf(), "%")

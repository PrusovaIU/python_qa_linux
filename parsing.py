from re import split as resprlit
from typing import List
import subprocess


class Process:
    def __init__(self, user: str, pid: int, cpu: float, mem: float, vsz: int, rss: int,
                 tty: str, _stat: str, start: str, time: str, command: str):
        self.user = user
        self.pid = pid
        self.cpu = cpu
        self.mem = mem
        self.vsz = vsz
        self.rss = rss
        self.tty = tty
        self.stat = _stat
        self.start = start
        self.time = time
        self.command = command


PROCESSES_LIST_TYPE = List[Process]


def parse_ps_aux() -> (PROCESSES_LIST_TYPE, str):
    shell = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, text=True)
    psaux_lines = shell.stdout.split('\n')
    psaux_lines.pop(0)  # remote the title
    processes: PROCESSES_LIST_TYPE = list()
    for line in psaux_lines:
        els: List[str] = resprlit(r"\s+", line, maxsplit=10)
        if len(els) == 11:
            processes.append(
                Process(
                    user=els[0],
                    pid=int(els[1]),
                    cpu=float(els[2]),
                    mem=float(els[3]),
                    vsz=int(els[4]),
                    rss=int(els[5]),
                    tty=els[6],
                    _stat=els[7],
                    start=els[8],
                    time=els[9],
                    command=els[10]
                )
            )
    return processes, shell.stdout


def get_users(processes: PROCESSES_LIST_TYPE) -> List[str]:
    records_users = set(process.user for process in processes)
    return list(records_users)

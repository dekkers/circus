#!/usr/bin/env python

import os
import errno

base_dir = "/sys/fs/cgroup"

def get_current_cgroup(subsystem):
    cgroups = {}
    with open("/proc/self/cgroup") as f:
        for line in f:
            line = line.strip().split(":")
            if subsystem in line[1].split(","):
                return line[2]

def get_hierarchies_for_subsystems(subsystems):
    hierachies = []
    with open("/proc/cgroups") as f:
        f.readline()
        for line in f:
            line = line.strip().split("\t")
            if line[0] in subsystems:
                hierachies.append(line[1])

    return hierachies

def get_unique_hierarchies(subsystems):
    pass

def change_cgroup(subsystem, name, create=True):
    #subsystems = get_unique_hierarchies(subsystems)
    current = get_current_cgroup(subsystem)
    new = os.path.join(current, name)
    directory = os.path.join(base_dir, subsystem) + new
    if create:
        try:
            os.mkdir(directory)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
    pid = os.getpid()
    with open(os.path.join(directory, "tasks"), "a") as f:
        f.write(str(pid))

if __name__ == "__main__":
    print "current", get_current_cgroup("cpuacct")
    change_cgroup("cpuacct", "test")
    print "current", get_current_cgroup("cpuacct")

import psutil
import platform
from datetime import datetime
import os
import re

## Service List
service_list = []
service_library = []

def get_ubuntu_host_info():
    print("OS Version is Ubuntu...")

    try:
        print("Listing running services")
        for line in os.popen("systemctl --type=service --state=running"):
            ## ignore lines with whitespace
            if line.strip(): 
                services = line.split()
                # only record services that contain .service
                if ".service" in services[0]:
                    service_list.append(services[0])
            pass        
    except OSError as ose:
        print("Error when listing services", ose)
    pass

## define service class
class Services(object):
    def __init__(self, name, loaded, active, pid, memory, cpu):
        self.loaded = loaded
        self.name = name
        self.active = active
        self.pid = pid
        self.memory = memory
        self.cpu = cpu

    def print_info(self): 
        table = [[self.name], [self.loaded], [self.active], [self.pid], [self.memory], [self.cpu]]

def check_service_versions():
    print("Checking Service Versions...")

    for s_name in service_list:
        #print("Service name is: " + s_name)
        for line in os.popen(f"systemctl status {s_name}"):
            if line.strip():
                # include with flag for debug output?
                # service_status = line.split()
                # print(service_status)

                # if line contains active, print it
                if "Active" in line:
                    s_active = line.split()
                    s_active = s_active[1]

                # if line contains memory, print it
                if "Memory" in line  and "MemoryAccounting" not in line:
                    s_memory = line.split()
                    s_memory = s_memory[1]            

                if "Loaded" in line:
                    s_loaded = line.split()
                    s_loaded = s_loaded[1]

                # if line contains main, print it
                if "Main" in line:
                    s_pid = line.split()
                    s_pid = s_pid[2]

                # if line contains CPU, print it
                if "CPU" in line and "CPUAccounting" not in line:
                    s_cpu = line.split()
                    s_cpu = s_cpu[1]

        
        service_meta = Services(s_name, s_loaded, s_active, s_pid, s_memory, s_cpu)
        service_library.append(service_meta)
        

    for service_a in service_library:
        print("="*5, service_a.name,"="*5)
        print("Loaded: ", service_a.loaded)
        print("Active: ", service_a.active)
        print("Memory: ", service_a.memory)
        print("CPU:    ", service_a.cpu)
        print("PID:    ", service_a.pid)

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
        self.name = name
        self.loaded = loaded
        self.active = active
        self.pid = pid
        self.memory = memory
        self.cpu = cpu

def check_service_versions():
    print("Checking Service Versions...")

    for single_service in service_list:
        for line in os.popen(f"systemctl status {single_service}"):
            if line.strip():
                # include with flag for debug output?
                # service_status = line.split()
                # print(service_status)

                # if line contains active, print it
                if "Active" in line:
                    s_active = line.split()
                    print(s_active)

                # if line contains loaded, print it
                if "Loaded" in line:
                    s_loaded = line.split()
                    print(s_loaded)

                # if line contains memory, print it
                if "Memory" in line:
                    s_memory = line.split()
                    print(s_memory)

                # if line contains main, print it
                if "Main" in line:
                    s_pid = line.split()
                    print(s_pid)

                # if line contains CPU, print it
                if "CPU" in line:
                    s_cpu = line.split()
                    print(s_cpu)

        
        service_meta = Services(single_service, s_loaded, s_active, s_pid, s_memory, s_cpu)
        service_library.append(service_meta)

    

    for service_l in service_library: 
        print("I am printing from Service Library " + service_l.name)
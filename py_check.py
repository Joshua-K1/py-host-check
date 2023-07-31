import psutil
import platform
from datetime import datetime
import os
import re

from ub_host_check import (
    get_ubuntu_host_info,
    check_service_versions
)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor: 
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_like_distro():
    info = platform.freedesktop_os_release()
    ids = [info["ID"]]
    if "ID_LIKE" in info:
        ids.extend(info["ID_LIKE"].split())

# Check if /etc/os-release file exists
os_release_path = "/etc/os-release"
os_release_lookup = "PRETTY_NAME"

if os.path.isfile(os_release_path): 
    with open(os_release_path) as file:
        for num, line in enumerate(file, 1):
            if os_release_lookup in line:
                line_split = line.split('"')[1::2]
                os_release_pretty = line_split[0] 



## Print System Information
print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System:     | {uname.system}")
print(f"OS Release: | {os_release_pretty}")
print(f"Release:    | {uname.release}")
print(f"Node Name:  | {uname.node}")
print(f"Version:    | {uname.version}")
print(f"Machine:    | {uname.machine}")
print(f"Processor:  | {uname.processor}")

## Print boot date and time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
boot_time = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {boot_time.year}/{boot_time.month}/{boot_time.day}/{boot_time.hour}/{boot_time.minute}:{boot_time.second}")

## Print CPU Information
print("="*40, "CPU Information", "="*40)
print("Physical Cores: ", psutil.cpu_count(logical=False))
print("Total Cores: ", psutil.cpu_count(logical=True))

## CPU Frequencies
cpu_freq = psutil.cpu_freq()
if cpu_freq.max == 0.00: 
    print(f"Max Frequency: {cpu_freq.max: .2f}Mhz <---- 0.00 means no Max Freq Value has been set")
else: 
    print(f"Max Frequency: {cpu_freq.max: .2f}Mhz")
if cpu_freq.max == 0.00: 
    print(f"Min Frequency: {cpu_freq.min: .2f}Mhz <---- 0.00 means no Min Freq Value has been set")
else: 
    print(f"Min Frequency: {cpu_freq.min: .2f}Mhz")
print(f"Current Frequency: {cpu_freq.current: .2f}Mhz")


## CPU Usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}:, {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

## Disk Usage
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")

## Network Information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

## Call function to get service info depending on OS Version
if "Ubuntu" in os_release_pretty:
    get_ubuntu_host_info()

## Check the version of each of the running services
check_service_versions()
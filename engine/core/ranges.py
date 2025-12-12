from ipaddress import ip_address
from loguru import logger
import ipaddress
import queue
import random

'''
Some functions to validate ip address ranges received as arguments.
Detects the type of range, for example if it is CIDR and generates a queue with all the targets to send to the Threadscan object.  
'''

def get_ranges(start,end):
    #Get total of ip addresses
    start_int = int(ip_address(start).packed.hex(), 16)
    end_int = int(ip_address(end).packed.hex(), 16)
    return [ip_address(ip).exploded for ip in range(start_int, end_int)]

def get_total_ip_ranges(file):
    total = []

    with open(file, 'r') as flist:
        blocks = list(filter(None, flist.read().splitlines()))
    for ip in blocks:
        targets = detect_range_type(ip)

        for t in targets:
            total.append(t)

    return total

def put_targets_in_queue(targets):
    q = queue.Queue()
    for t in targets:
        q.put(t)
    return q

def single_range(iprange):

    total = detect_range_type(iprange)
    return randomize_list(total)

def multiple_ranges(file):

    total = get_total_ip_ranges(file)
    return randomize_list(total)

def randomize_list(total):
    shuffled = sorted(total, key=lambda L: random.random())
    return put_targets_in_queue(shuffled)

def detect_range_type(iprange):
    if "," in iprange:
        ranges = iprange.split(",")
        result = get_ranges(ranges[0],ranges[1])
    elif "/" in iprange:
        result = get_cidr(iprange)
    else:
        logger.info("Invalid target")
        exit()
    return result

def get_cidr(iprange):
    return [str(ip) for ip in ipaddress.IPv4Network(iprange)]

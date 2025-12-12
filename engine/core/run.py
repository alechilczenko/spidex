from core.threadscan import Threadscan
from core.api import submit_report
from datetime import datetime
from config import Config
from loguru import logger

def launch_scanner(targets, threads, timeout, top_ports, all_ports, custom):
    Discover = Threadscan(targets)

    if top_ports:
        Discover.set_ports(Config.TOP_PORTS)
    elif all_ports:
        Discover.set_ports(Config.PORTS)
    elif custom:
        Discover.set_ports(custom)
    else:
        logger.info("Please set port scan mode")
        exit()

    start = datetime.now()

    Discover.start_threads(threads, timeout)

    end = datetime.now()

    exec_time = end-start
    logger.info("Execution time: {}".format(exec_time))

    found = Discover.get_total_found()
    total = Discover.get_total()

    submit_report(total,found,exec_time,start,end)


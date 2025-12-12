#!/usr/bin/env python
from loguru import logger
from core.ranges import single_range, multiple_ranges
from core.parser import get_flags
from loguru import logger
from core.run import launch_scanner
import sys

def main():
    
    iprange,threads,path,timeout,top_ports,all_ports,custom,logs = get_flags()

    logger.remove(0)

    logger.add(sys.stderr,colorize=True,format="<blue>{time:HH:mm:ss} <level>{level: <8}</level> <level>{message}</level></blue>", enqueue=True)

    if logs:
        logger.add("logs/{time}.log", enqueue=True)
        
    if  iprange:
        targets = single_range(iprange)
        launch_scanner(targets,threads,timeout,top_ports,all_ports,custom)

    elif path:
        targets = multiple_ranges(path)
        launch_scanner(targets,threads,timeout,top_ports,all_ports,custom)
    else:
        logger.info("Please use -h to see all options")
        exit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        exit()

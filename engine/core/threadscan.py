#Local modules
from loguru import logger
import queue

import threading

from core.portscan import Portscan
from core.geoparser import create_json
from core.api import submit_data
from config import Config

'''
Threadscan class receives the queue with the ip addresses and starts threads.
Then it instantiates the portscan object.
If the portscan contains valid targets, it calls a function to process and send that data to an API.
'''

class Threadscan():
    def __init__(self,targets):
        self.q = targets
        self.results = queue.Queue()
        self.lock = threading.Lock()
        self.count = 0
        self.total = self.q.qsize()

    def set_ports(self,ports):
        self.ports = ports

    def job(self,timeout):
        while True:
            try:
                ip = self.q.get(timeout=3)
                self.progress_bar()

            except queue.Empty:
                return

            Scanner = Portscan(ip)
            Scanner.start(timeout,self.ports)

            if Scanner.contain_results():
                banners, hostname, ports, tags = Scanner.get_results()
                device, output = create_json(ip,banners,hostname,ports,tags)

                submit_data(device,Config.SERVER_NAME,Config.API_DEVICE_ENDPOINT)

                self.results.put_nowait(device)
                
                logger.success(output)
                
            self.q.task_done()

    def start_threads(self,max_threads,timeout):
        #Implemeting Queue, safe threading
        #Count total of results with Queue
        try:
            logger.info(f"Waiting for Queue to complete, {self.q.qsize()} jobs")

            for _ in range(max_threads):
                thread = threading.Thread(target=self.job,args=(timeout,),daemon=True)
                thread.start()

            self.q.join()
            logger.info(f"Total discovered devices: {self.results.qsize()}")

        except KeyboardInterrupt:
            logger.info("You pressed CTRL+C")
            exit()

    def progress_bar(self):
        with self.lock:

            self.count += 1
            percent = (self.count * 100) / self.total
            output = "{}% {}/{}".format(percent,self.count, self.total)
            print(output, end="\r")

    def get_total_found(self):
        return self.results.qsize()
    
    def get_total(self):
        return self.total




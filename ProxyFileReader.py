import threading
import time
import re
import os
from os import listdir
from os.path import  isfile, join
from Proxy import Proxy


class ProxyFileReader(threading.Thread):

    def __init__(self):
        super(ProxyFileReader, self).__init__()

    def run(self):
        while True:
            fileList = [f for f in listdir('ProxyFiles') if isfile(join('ProxyFiles', f)) and f != '.gitkeep']
            for file in fileList:
                print("New file ready for processing: " + file)

                lines = [line.strip() for line in open(join('ProxyFiles', file))]
                for line in lines:
                    if re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$', line) is not None:
                        proxyParts = line.split(":")
                        px = Proxy(proxyParts[0], int(proxyParts[1]))

                        px.updateProxy()
                        # print(line, flush=True)
                    else:
                        print("Odd line: " + line, flush=True)

                print("File processed and deleted: " + file)

                os.remove(join('ProxyFiles', file))
            time.sleep(60)
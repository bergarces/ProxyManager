import threading
from Proxy import Proxy


class ProxyUpdater(threading.Thread):

    def __init__(self, numberOfThreads):
        self.numberOfThreads = numberOfThreads

        super(ProxyUpdater, self).__init__()

    def run(self):
        # Create threads that will be constantly filled
        print('ProxyUpdater started')
        proxyList = []
        threadsList = []
        for i in range(self.numberOfThreads):
            t = threading.Thread(target=ProxyUpdater._worker, args=(i, proxyList,))
            threadsList.append(t)
            t.start()
            print('Thread ' + str(i) + ' started')

        while True:
            # Append more items to the list when needed
            if len(proxyList) < 100:
                print('100 more items added')
                proxyList.extend(Proxy.getProxyBag(100))

    @staticmethod
    def _worker(threadNumber, proxyList):
        while True:
            try:
                proxy = proxyList.pop(0)
                proxy.updateProxy()
                # print('Proxy ' + proxy.host + ':' + str(proxy.port) + ' updated by thread ' + str(threadNumber))
            except:
                pass
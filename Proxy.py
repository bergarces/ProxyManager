from ProxyDB import ProxyDB
import ProxyTester
import time
import datetime


class Proxy:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self._pDB = ProxyDB()
        dbObject = self._pDB.getProxy(self.host, self.port)
        if dbObject is not None:
            self.currenttStatus = dbObject['currentStatus']
            self.currentDelta = dbObject['currentDelta']
            self.lastChecked = dbObject['lastChecked']
            self._calculateScore(dbObject['pastQueries'])

    def updateProxy(self):
        startTime = time.time()
        result = ProxyTester.proxyQuery(self.host, self.port)
        endTime = time.time()

        deltaTime = endTime - startTime
        self._pDB.updateProxy(self.host, self.port, result, deltaTime if result else 0,
                              datetime.datetime.fromtimestamp(startTime, None))

        self.resultStatus = result
        self.resultDelta = deltaTime
        self.resultTime = startTime

        self._updateScore()

        return result

    def _updateScore(self):
        pastQueries = self._pDB.getPastQueries(self.host, self.port)
        self._calculateScore(pastQueries)
        self._pDB.updateScore(self.host, self.port, self.score)

    def _calculateScore(self, pastQueries):
        successList = list(query for query in pastQueries if query['status'])
        self.successRate = len(successList) / len(pastQueries)

        if len(successList) > 0:
            deltaList = list(x['delta'] for x in successList)
            self.avgDelta = sum(deltaList) / len(deltaList)
        else:
            self.avgDelta = 0

        self.score = self.__computeProxyScore()

    def __computeProxyScore(self):
        return self.successRate * 10 - (self.avgDelta * 0.2)

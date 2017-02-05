from pymongo import MongoClient

class ProxyDB:

    def __init__(self):
        self._client = MongoClient()
        self._db = self._client['proxy-manager']

    def getProxy(self, proxyHost, proxyPort):
        result = self._db['proxies'].find_one(
            {
                "host": proxyHost,
                "port": proxyPort
            }
        )

        return result

    def updateProxy(self, proxyHost, proxyPort, resultStatus, resultDelta, resultTime):
        self._db['proxies'].update(
            {
                "host": proxyHost,
                "port": proxyPort
            },
            {
                "$set": {
                    "host": proxyHost,
                    "port": proxyPort,
                    "currentStatus": resultStatus,
                    "currentDelta": resultDelta,
                    "lastChecked": resultTime
                },
                "$push": {
                    "pastQueries": {
                        "$each": [ { "status": resultStatus, "delta": resultDelta, "time": resultTime } ],
                        "$position": 0,
                        "$slice": 10
                    }
                }
            },
            upsert=True
        )

    def updateScore(self, proxyHost, proxyPort, score):
        self._db['proxies'].update(
            {
                "host": proxyHost,
                "port": proxyPort
            },
            {
                "$set": {
                    "score": score
                }
            }
        )

    def getPastQueries(self, proxyHost, proxyPort):
        result = self._db['proxies'].find_one(
            {
                "host": proxyHost,
                "port": proxyPort
            },
            {
                "pastQueries": 1,
                "_id": 0
            }
        )

        return result['pastQueries']

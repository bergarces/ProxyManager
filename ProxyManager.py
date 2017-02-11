from ProxyFileReader import ProxyFileReader
from ProxyUpdater import ProxyUpdater


if __name__ == '__main__':
    fReader = ProxyFileReader()
    fReader.start()

    fUpdater = ProxyUpdater(10)
    fUpdater.start()
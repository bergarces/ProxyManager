from io import BytesIO
import pycurl
import time


def proxyQuery(proxyHost, proxyPort, attempts=1):
    ipCheckerUrl = 'icanhazip.com'

    c = pycurl.Curl()
    result = BytesIO()

    c.setopt(pycurl.URL, ipCheckerUrl)
    c.setopt(pycurl.CONNECTTIMEOUT, 10)
    c.setopt(c.WRITEFUNCTION, result.write)
    c.setopt(pycurl.PROXY, proxyHost)
    c.setopt(pycurl.PROXYPORT, proxyPort)
    c.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    try:
        c.perform()
    except pycurl.error as e:
        c.close()

        if attempts < 3 and e.args[0] not in [28]:
            time.sleep(5)
            return proxyQuery(proxyHost, proxyPort, attempts+1)
        else:
            print(e, end='', flush=True)
            return False
    except:
        return False
    finally:
        c.close()

    content = result.getvalue().decode('utf-8')
    content = content.strip()
    return content == proxyHost

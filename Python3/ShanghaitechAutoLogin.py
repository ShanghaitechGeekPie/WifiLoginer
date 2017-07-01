import urllib.request
import http.cookiejar
import random
import json
import time
import subprocess
import platform
import traceback

class IncompleteFieldException(Exception):
    def __init__(self, err='Please set your username and password!'):
        Exception.__init__(self, err)

def sleep(seconds):
    for _ in range(seconds):
        time.sleep(1)

def getTimeStr():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

def getRandomString(n = 32):
    _char = 'abcdefghijklmnopqrstuvwxyz0123456789'.upper()
    return ''.join((_char[random.randint(0, len(_char)-1)] for _ in range(n)))

def login(username, password):
    if username is None or password is None:
        raise IncompleteFieldException()
    url = 'https://controller1.net.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action'
    data = {'userName': username,
            'password': password,
            'hasValidateCode': 'false',
            'validCode': '',
            'hasValidateNextUpdatePassword': 'true'}
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    header = {'Accept': '*/*',
              'Content-Type': 'application/x-www-form-urlencoded',
              'JSESSIONID': getRandomString(32),
              'User-Agent': 'ShanghaiTech_Network_AutoLoginer Python3'}

    request = urllib.request.Request(url, postdata, header)
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    response = opener.open(request)
    result = response.read().decode('utf-8')
    result_obj = json.loads(result)
    return result_obj

def sync(ipAddr, sessionID, XSRF_TOKEN):
    url = 'https://controller1.net.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!syncPortalAuthResult.action'
    data = {'clientIp': ipAddr,
            'browserFlag': 'zh'}
    postdata = urllib.parse.urlencode(data).encode('utf-8')
    header = {'Accept': '*/*',
              'Content-Type': 'application/x-www-form-urlencoded',
              'JSESSIONID': getRandomString(32),
              'User-Agent': 'ShanghaiTech_Network_AutoLoginer Python3',
              'X-Requested-With': 'XMLHttpRequest',
              'X-XSRF-TOKEN': XSRF_TOKEN,
              'Cookie': 'JSESSIONID='+sessionID+'; '+'XSRF_TOKEN='+XSRF_TOKEN}
    request = urllib.request.Request(url, postdata, header)
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

    response = opener.open(request)
    result = response.read().decode('utf-8')
    result_obj = json.loads(result)
    return result_obj
    
if __name__ == '__main__':

    USERNAME = None
    PASSWORD = None
    DEBUG = False
    
    print(getTimeStr(), 'Shanghaitech Auto Loginer has started.')
    print(getTimeStr(), 'Username =', USERNAME)
    print(getTimeStr(), 'Password =', ('******', '*'*len(str(PASSWORD)))[DEBUG])
    if DEBUG:
        print(getTimeStr(), 'Run in Debug Mode.')
        
    while True:
        try:
            ping_command = ('ping -W 1 -c 1 ', 'ping -w 1000 -n 1 ')['Windows' in platform.system()]
            domain_name = 'www.qq.com'
            s = subprocess.Popen(ping_command + domain_name,
                                 shell=True,
                                 stdout=(subprocess.PIPE, None)[DEBUG],
                                 stderr=(subprocess.PIPE, None)[DEBUG])
            s.wait()
            sleep(5)
            if s.returncode == 0 and not DEBUG:
                pass
            else:
                print(getTimeStr(), 'Authenticating...')
                login_result = login(USERNAME, PASSWORD)
                if DEBUG:
                    print(login_result)
                try:
                    message = login_result['message']
                    IP = login_result['data']['ip']
                    sessionID = login_result['data']['sessionId']
                    token = login_result['token'][6:]
                except TypeError:
                    print(getTimeStr(), message)
                    continue
                for i in range(15):
                    print(getTimeStr(), 'Synchronizing... ', end=' ')
                    sync_result = sync(IP, sessionID, token)
                    if DEBUG:
                        print(sync_result)
                    try:
                        status = sync_result['data']['portalAuthStatus']
                    except TypeError:
                        print(getTimeStr(), message)
                        continue
                    if status == 0:
                        print('Waiting...')
                    elif status == 1:
                        print('Connected.')
                        break
                    elif status == 2:
                        print('Auth Failed!')
                        break
                    else:
                        errorcode = sync_result['data']['portalErrorCode']
                        if errorcode == 5:
                            print('Exceed maximum device capacity!')
                        elif errorcode == 101:
                            print('Passcode error!')
                        elif errorcode == 8000:
                            print('Radius relay auth failed, errorcode =', errorcode - 8000)
                        else:
                            print('Auth Failed!')
                        break
                    sleep(3)
        except IncompleteFieldException as e:
            print(getTimeStr(), e)
        except Exception as e:
            print(getTimeStr(), 'Unhandled Exception!')
            print(getTimeStr(), repr(e))
            traceback.print_exc()

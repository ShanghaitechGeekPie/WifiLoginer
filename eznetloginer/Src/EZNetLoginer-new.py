# coding=utf-8
try:
    # python3 grammar
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    # python2 grammar
    from urlparse import urlparse
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError
import http.client
import argparse
import random
import json
import os
import time

def check_internet(url="http://www.baidu.com", timeout=1):
    try:
        urlopen(url=url, timeout=timeout)
        return True
    except URLError:
        return False

def shtlogin(username, pwd):
    params = urlencode(
        {'userName': username, 'password': pwd, 'hasValidateCode': False, 'authLan': 'zh_CN'})
    cookie_code = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], 32)).replace(' ', '')
    headers = {'Content-type': 'application/x-www-form-urlencoded'
        , 'Accept': '*/*', 'Cookie': 'JSESSIONID=' + cookie_code}
    httpClient = http.client.HTTPSConnection('controller.shanghaitech.edu.cn', 8445, timeout=30)
    try:
        httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!login.action', params, headers)
    except:
        return "Network connection error."
    response = httpClient.getresponse()
    if response.status != 200:
        return "Network is not available."
    else:
        response_data = response.read().decode('utf-8')
        response_data_json = json.loads(response_data)
        if response_data_json['success'] != True:
            return "Invalid username/password combination."
        else:
            return "Success."

def get_argparser():
    confparser = argparse.ArgumentParser(description='Make internet connect easier in Shanghaitech University.')
    fileconf = confparser.add_argument_group("File config")
    fileconf.add_argument("-c", "--config", type=str, default=None, help="Path to config json file.")
    fileconf.add_argument("--generate-config", type=str, default=None, help="Generate default config file at given"
                                                                            "path.")
    argconf = confparser.add_argument_group("Argument config")
    argconf.add_argument("-u", "--username", type=str, default="exam", help="Username.")
    argconf.add_argument("-p", "--password", type=str, default="exam123", help="Password.")
    argconf.add_argument("-a", "--auto-reconnect", default=False, action="store_true", help="Auto reconnect"
                                                                                              "after disconnected.")
    argconf.add_argument("--timeout", type=int, default=1, help="Timeout when checking internet connection.")
    argconf.add_argument("-t", "--check-interval", type=int, default=1, help="The time interval to check internet"
                                                                               "connection")
    argconf.add_argument("--try-times", type=int, default=3, help="Specify how many times will try when failed "
                                                                    "to reconnect.")
    argconf.add_argument("--check-url", type=str, default="http://www.baidu.com", help="Specify the url to check"
                                                                                         "internet connection.")
    return confparser

if __name__ == "__main__":
    parser = get_argparser()
    argsdict = vars(parser.parse_args())
    if argsdict["generate_config"] is not None:
        filepath = argsdict.pop("generate_config")
        argsdict.pop("config")
        with open(filepath, "w") as fp:
            json.dump(argsdict, fp, sort_keys=True, indent=2)
            print("Saved default config file at {}".format(filepath))
        exit(0)
    if argsdict["config"] is not None:
        if not os.path.isfile(argsdict["config"]):
            print("Config file {} doesn't not exist.".format(argsdict["config"]))
            exit(-1)
        else:
            with open(argsdict["config"]) as fp:
                fileargs = json.load(fp)
                if fileargs is None:
                    print("Errors occured when parsing config file, please check your syntax or use --generate-config"
                          "option to generate a valid config file. ")
                    exit(-1)
                else:
                    argsdict.update(fileargs)
    if argsdict["auto_reconnect"] is not True:
        print(shtlogin(argsdict["username"], argsdict["password"]))
    else:
        print("Auto-reconnect mode running...(press CTRL-C to stop)")
        while True:
            if not check_internet(url=argsdict["check_url"], timeout=argsdict["timeout"]):
                print("Internet disconnected")
                for i in range(argsdict["try_times"]):
                    print("Try to reconnect, {}/{} try...".format(i, argsdict["try_times"]))
                    reply = shtlogin(argsdict["username"], argsdict["password"])
                    print(reply)
                    if reply == "Success.":
                        break
                    elif i == argsdict["try_times"]-1:
                        exit(-1)
            time.sleep(argsdict["check_interval"])

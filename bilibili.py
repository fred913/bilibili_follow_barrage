# coding: utf-8
import random
import time
import base64 as b64

import requests

last_fan = {}

virtual_url = []

all_proxies = []
for i in eval(requests.get("http://www.cool-proxy.net/proxies.json").content.decode("utf-8")):
    _ = Demo = {
        "country_name": "Unknown",
        "working_average": 99.9998,
        "download_speed_average": 27170.0,
        "anonymous": 1,
        "ip": "45.55.23.78",
        "update_time": 1579414011.0,
        "score": 178.478,
        "port": 3128,
        "response_time_average": 4.63919,
        "country_code": "--"
    }
    all_proxies.append((i['ip'], i['port']))


def random_proxy():
    all = [('221.229.252.98', '9797'), ('114.237.144.34', '9999'), ('58.247.127.145', '53281'),
           ('124.237.83.14', '53281'), ('14.20.235.7', '808'), ('183.196.168.194', '9000'),
           ('124.205.155.151', '9090'), ('119.57.108.65', '53281'), ('182.18.13.149', '53281'),
           ('1.197.16.222', '9999'), ('58.247.127.145', '53281'), ('183.196.168.194', '9000'),
           ('122.136.212.132', '53281'), ('221.229.252.98', '9797'), ('115.233.210.218', '808')] + all_proxies
    return HTTP_Proxy(*random.choice(all))


def HTTP_Proxy(host, port):
    proxies = {'http': 'http://' + str(host) + ':' + str(port), 'https': 'http://' + str(host) + ':' + str(port)}
    return {
        "proxies": proxies,
        "verify": False
    }


def get_page(uid):
    headers = ['Host: api.bilibili.com', 'Connection: keep-alive',
               'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.2661.87 Safari/537.36',
               'Accept: */*', 'Referer: https://space.bilibili.com/' + str(uid) + '/fans/fans',
               'Accept-Encoding: gzip, deflate, br', 'Accept-Language: zh-CN,zh;q=0.9',
               "Cookie: CURRENT_FNVAL=16; LIVE_BUVID=AUTO7615792541864470; rpdid=|(k|~JYYklkJ0J'ul~mklRu)Y; sid=4i721n90; INTVER=1"]
    headers_dict = {}
    for i in headers:
        j, k = i.split(": ")
        headers_dict[j] = k
    res = requests.get(
        headers=headers_dict,
        url="https://api.bilibili.com/x/relation/followers?vmid=" + str(uid) + "&pn=1&ps=20&order=desc&jsonp=jsonp"
                                                                               "&callback=__jp6",
        **random_proxy()
    )
    res.encoding = "utf-8"
    data = res.text
    return data


def get_fans(uid):
    data = get_page(uid)
    data = data.replace(
        "__jp6",
        ""
    )
    undefined = null = None
    data = eval(data)
    data = data["data"]['list']
    new_data = []

    def create_vurl(url):
        global virtual_url
        virtual_url.append(url)
        id = int(len(virtual_url) - 1)
        time.sleep(0.1)
        res = requests.get(virtual_url[id])
        while res.status_code != 200:
            res = requests.get(virtual_url[id])
        return "data:image/png;base64," + (b64.b64encode(res.content).decode())

    for i in data:
        new_data.append((create_vurl(i["face"]), i['uname']))
    return new_data


def get_fans_uname(fans_data):
    d = []
    for i, j in fans_data:
        d.append(j)
    return d


def get_fans_face(fans_data):
    d = []
    for i, j in fans_data:
        d.append(i)
    return d


def get_new_fans(uid):
    global last_fan
    try:
        a = last_fan[uid]
        del a
    except:
        last_fan[uid] = None
    print(last_fan[uid])
    data = get_fans(uid)
    print(get_fans_uname(data))
    try:
        x = get_fans_uname(data).index(last_fan[uid])
    except:
        print("can't index last fan '" + str(last_fan[uid]) + "'. data:", str(get_fans_uname(data)), "not indexed")
        last_fan[uid] = get_fans_uname(data)[0]
        return []
    else:
        print("indexed last fan '" + str(last_fan[uid]) + "'. data:", str(get_fans_uname(data[0:x])), "indexed")
        last_fan[uid] = get_fans_uname(data)[0]
        return data[0:x]

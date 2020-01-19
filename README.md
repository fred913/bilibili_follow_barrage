# bilibili_follow_barrage
[Inspiration](https://www.bilibili.com/video/av83955084)

# 哔哩哔哩关注弹幕
灵感来源于[B站硬核拆解视频](https://www.bilibili.com/video/av83955084)

### DIY关注弹幕教程：
 - 本程序使用Python编写。由于灵感来源的UP不会Python，所以~~我加了UP的微信~~我编写了这个教程
 -  ~~众所周知，~~Python中有一个简单易用的框架，叫Flask，可以使用decorator的方式编写网站。
 - Flask普通HTTP服务器创建代码：
 ```Python
 	from flask import *
	app = Flask("bilibili_follow_barrage")
  @app.route("/")
  def index():
    return "HTTP服务器"
  
  
  app.run("127.0.0.1", 8998)
 ```
接着懒得写了，直接把剩下会调用的API写完就好了......
```python
# coding: utf-8
import socket
import time
import requests
from flask import *
import bilibili as bb


def readfile(filename):
    f = open(filename, "rb")
    c = f.read()
    f.close()
    return c


hy_string = [
    '刚刚加入了粉丝团！',
    "加入了帮派",
    "点击了至高无上的关注按钮！",
    "点了关注",
    "上了UP的贼船~"
]


def check_port_use(port, ip='127.0.0.1'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except:
        return False


def runweb(proj_name="bilibili_follow_barrage"):
    app = Flask(proj_name)

    @app.route("/")
    def index():
        return readfile("./index.html").decode("utf-8").replace("__UID__", request.args.get("uid") if request.args.get(
            "uid") is not None else "427494870").encode("utf-8")

    @app.route("/get")
    def get_new():
        try:
            uid = int(request.args.get("uid"))
        except:
            uid = 427494870
        while 1:
            try:
                return jsonify(
                    bb.get_new_fans(uid)
                )
            except:
                continue

    @app.route("/update")
    def update():
        bb.last_fan = {}
        return ""

    @app.route("/barrager.js")
    def barrager():
        return readfile("./barrager.js")

    @app.route("/bg.png")
    def bg_png():
        return readfile("./background.png")

    port = 1024
    while check_port_use(port):
        port += 1
    app.run("127.0.0.1", port)
```
 - 接下来写bilibili.py（哔哩哔哩获取粉丝的接口）
 ```python
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
 ```
 然后index.html也放出来吧，弹幕本来是B站的@啊泰_ 同学给了我一个jquery.barrager.js，结果不会用，自己写了一个
 ```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>哔哩哔哩关注弹幕 - ShengFAN制作</title>
    <link href="https://cdn.bootcss.com/mdui/0.4.3/css/mdui.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/mdui/0.4.3/js/mdui.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
    <style>
        .barrage {
            /*  设置为 绝对定位 */
            position: absolute;
            /* 设置为 块级元素 */
            display: block;
            /* 设置左边距 使弹幕初始位置在视频部分之外 */
            left: 100%;
        }
        body {
            background: url("/bg.png");
            background-size:cover;
        }
    </style>
    <script type="text/javascript">
    function createBarrageHTML(content){
        //创建一个span
        var barrage=document.createElement("div");
        //定义内容
        barrage.innerHTML=content;
        //指定class
        barrage.className="barrage";
        //为弹幕设置一个随机的高度
        barrage.style.top=randomNum(1,95)+'%';
        //宽度
        barrage.style.width=content.length*16+'px';
        //为弹幕设置一个随机的颜色
        barrage.style.color=randomColor();
        //加入video中
        document.getElementById("container").appendChild(barrage);
        //开始滚动
        rolling(barrage)
    }
    function randomNum(minNum,maxNum){
        return parseInt(Math.random()*(maxNum-minNum+1)+minNum,10);
    }
    function randomColor(){
        var color="#";
        for(var i=0;i<6;i++){
            color += (Math.random()*16 | 0).toString(16);
        }
        return color;
    }
    function randomhy() {
        var all = [
            '刚刚加入了粉丝团！',
            "加入了帮派",
            "点击了至高无上的关注按钮！",
            "点了关注",
            "上了UP的贼船~"
        ];
        return all[randomNum(0,4)];
    }
    function rolling(object){

        //启动一个定时器，每10秒执行一次
        var a= setInterval(function () {
            //判断是否滚动出屏幕
            //取左边距，如果弹幕的最后一个字符的左边距大于0，则一直执行自减操作，通过上边的css，我们知道每个字符的大小为16px
            if (object.offsetLeft>-object.innerHTML.length*16) {
                object.style.left=object.offsetLeft-3+'px';
            }else{
                //如果弹幕已移出屏幕，则删除本条弹幕
                object.parentNode.removeChild(object);
                //清理定时器
                clearInterval(a);
            }
        }, 1);
    }
    function onReady() {
        window.setInterval(function() {
            $.getJSON("/get", function(data) {
                for(i in data) {
                    createBarrageHTML("<div class=\"mdui-chip\"> \
    <img class=\"mdui-chip-icon\" src=\"" + data[i][0] + "\" /> \
    <span class=\"mdui-chip-title\">" + data[i][1] + randomhy() + "</span> \
</div>");
                }
            });
        }, 1000);
        window.setInterval(function() {
            $.get("/update", function(a,b) {});
        }, 10000);
    }
    $(onReady);
    </script>
</head>
<body>
<div class="mdui-container-fluid" id="container">

</div>
</body>
</html>
 ```
 如果你没有服务器也没关系，可以使用FredTools提供的服务器玩。FredTools服务器访问限速为一个账号只能使用一个浏览器，不然会出错，服务器会被Bilibili查封，所以在爱发电上提供了两个计划供用户选择，一个可以将QPS（每秒可访问的次数）提升到10，另一个可去除QPS限制。感谢您的支持！
 传送门：[点我](https://afdian.net/@bb_follow_barrage/plan)

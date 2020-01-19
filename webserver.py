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
        return readfile("./index.html").decode("utf-8") \
            .replace("__UID__", request.args.get("uid") if request.args.get("uid") is not None else "427494870") \
            .encode("utf-8")

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

    @app.route("/v", methods=['GET'])
    def vurl():
        print(bb.last_fan)
        try:
            id = int(request.args.get("i"))
            time.sleep(0.1)
            res = requests.get(bb.virtual_url[id])
            while res.status_code != 200:
                res = requests.get(bb.virtual_url[id])
            return res.content
        except:
            return "404", 404

    port = 1024
    while check_port_use(port):
        port += 1
    app.run("127.0.0.1", port)

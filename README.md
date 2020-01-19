# bilibili_follow_barrage
[Inspiration](https://www.bilibili.com/video/av83955084)

# 哔哩哔哩关注弹幕
灵感来源于[B站硬核拆解视频](https://www.bilibili.com/video/av83955084)

### DIY关注弹幕教程：
 - 本程序使用Python编写。由于灵感来源的UP不会Python，所以~~我加了UP的微信~~我编写了这个教程
 - ~~众所周知，~~Python中有一个简单易用的框架，叫Flask，可以使用decorator的方式编写网站。
 - Flask普通HTTP服务器创建代码：
 ```Python
 	from flask import *
	app = Flask("bilibili_follow_barrage")
  @app.route("/")
  def index():
    return "HTTP服务器"
  
  
  app.run("127.0.0.1", 8998)
 ```

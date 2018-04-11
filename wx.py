# 导入模块
from wxpy import *
# 初始化机器人，扫码登陆
bot = Bot()
# 向文件传输助手发送消息
bot.file_helper.send('Hello from wxpy!')

my_friend = bot.friends().search('oyytoy',city='深圳')[0]

my_friend.send('Hello, WeChat!')



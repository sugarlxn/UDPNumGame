# NumGame
![logo](image\numgamelogo.jpg)
这是一个基于UDP网络协议的猜数字游戏服务器与客户端
支持多用户在同一服务器上多人游戏，同时用户可以通过客户端查询游戏成绩排行榜

## usage
1. 将仓库下载到你的任意一个工作目录，并进入本文件夹
2. 安装使用UDP所需要的python库：
```sh
pip install sockets
```
3. 运行NumGameServer以及NumGameClient，用户即可在Client端进行游戏啦！(Client端可以多开，多人游戏)
```sh
python3 NumGameServer.py
python3 NumGameClient.py
```
![Client](image\Client.jpg)
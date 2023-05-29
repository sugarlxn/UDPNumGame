#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
二、实验内容：猜数字游戏。
1. 服务器上存储了一个0到1,000,000之间的整数，接收来自客户端猜测的数字，如果数字与服务器数字相等则发送成功，
否则如果猜测的数字大于服务器上数字则发送“big”，小于则发送“small”。服务器统计每个客户端猜测正确所需次数，
选出猜测次数最小的成为获胜者，并公布所有客户端的成绩。
'''

#version 2 on branch test3_game2

import socket
import sys
import random
import pprint

#新建一个游戏服务端的类
class game_server():
    def __init__(self) -> None:
        self.socket_port = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket_port.bind(("127.0.0.1", 6000))
        self.random_num = random.randint(0, 1000000)
        self.client_dict = {} #存储客户端的字典 {"username": {num: "num", count: guest_times, data_time:"time"}, ...}
        self.winner_dic = {} #{num:{user_name:"lxn",data_time:xxxxx}, ...}
        self.logo_winner = '''                       
 _  _  __  __ _  __ _  ____  ____
/ )( \(  )(  ( \(  ( \(  __)(  _ \
\ /\ / )( /    //    / ) _)  )   /
(_/\_)(__)\_)__)\_)__)(____)(__\_)

        '''

        self.logo_game = '''
  _  __ _  _  _  _  _     ___   __   _  _  ____    ____  ____  ____  _  _  ____  ____  _   
 / \(  ( \/ )( \( \/ )   / __) / _\ ( \/ )(  __)  / ___)(  __)(  _ \/ )( \(  __)(  _ \/ \  
 \_//    /) \/ (/ \/ \  ( (_ \/    \/ \/ \ ) _)   \___ \ ) _)  )   /\ \/ / ) _)  )   /\_/  
 (_)\_)__)\____/\_)(_/   \___/\_/\_/\_)(_/(____)  (____/(____)(__\_) \__/ (____)(__\_)(_)  
                                              
        '''
    def begin_page(self):
        print(self.logo_game)
        print("UDP bound on port 6000...")
        print("waiting for client...")

    def print_winner(self):
        sorted_list = []
        for keys,values in self.winner_dic.items():
            sorted_list.append((values["count"],keys))
        sorted_list.sort(reverse=False)
        # print(self.logo_winner)
        # pprint.pprint(sorted_list)
        print("client request winner_list!")
        # for i in sorted_list:
        #     print("user_name: %s, count: %s" % (i[1],i[0]))
        return [(i[1],i[0]) for i in sorted_list]


    def game_run(self):
        while True:
            data, addr = self.socket_port.recvfrom(1024)
            # print("Receive from %s:%s" % (addr,data.decode()))
            user_list = data.decode().split(",")
            # print(user_list)
            if(user_list[0] == "start_game"):
                self.mannager_member(user_list[1],user_list[2],addr) # user_name,data_time,address
            elif(user_list[0] == "guess"):
                self.guess_number(user_list[1],user_list[2],user_list[3],addr)
            elif(user_list[0]=="show_winner"):
                #发送获胜者列表给用户
                winner_list = self.print_winner()
                self.socket_port.sendto(str(winner_list).encode(), addr)
               

    def mannager_member(self,user_name,data_time,addr):
        #修改逻辑，无论用户是否存在，开始游戏直接覆盖
        #FIXME: 当用户名称相同时，会覆盖之前的用户信息
        self.client_dict[user_name] = {"num": random.randint(0, 1000000), "count": 0, "data_time": data_time}
        pprint.pprint(self.client_dict[user_name])
        

    def guess_number(self,user_name,data_time,guess,addr):
        # print("user_name: %s, data_time: %s, addr: %s" % (user_name,data_time,addr))
        if(user_name not in self.client_dict):
            self.socket_port.sendto(b"please start game first!\n", addr)
        else:
        
            self.client_dict[user_name]["count"] += 1                                 
            self.client_dict[user_name]["data_time"] = data_time 

            #guss 会出现字符串的情况，导致int(guess)报错，并且guess 也会出现空值的情况
            try:
                guess_int = int(guess)
            except Exception as e:
                print(e)
                self.socket_port.sendto(b"please input number!\n", addr)
                return
                
            if(guess_int == self.client_dict[user_name]["num"]):
                self.socket_port.sendto(b"correct!\n", addr)
                self.load_winner(self.client_dict[user_name],user_name)
            else:
                if(guess_int > self.client_dict[user_name]["num"]):
                    self.socket_port.sendto(b"big!\n", addr)
                elif(guess_int < self.client_dict[user_name]["num"]):
                    self.socket_port.sendto(b"small!\n", addr)
                else:
                    self.socket_port.sendto(b"data error!\n", addr)
                
    # 载入获胜者成绩
    def load_winner(self,user_dict,user_name):
        #存储客户端的字典 {"username": {num: "num", count: guest_times, data_time:"time"}, ...}
        if(user_name in self.winner_dic):
            if(self.winner_dic[user_name]["count"] > user_dict["count"]):
                self.winner_dic[user_name]["count"] = user_dict["count"]
                self.winner_dic[user_name]["data_time"] = user_dict["data_time"]
        else:
            self.winner_dic.update({user_name:{"count":user_dict["count"], "data_time":user_dict["data_time"]}})

        

if __name__ == "__main__":

    game_server = game_server()
    game_server.begin_page()
    game_server.game_run()


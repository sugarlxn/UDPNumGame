#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
import time
 
#version 2 on branch test3_game2

class game_client():
    def __init__(self) -> None:
        self.socket_port = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.addr = ("127.0.0.1", 6000)
        self.logo_winner = '''                    
                     _                       
                    (_)                      
            __      ___ _ __  _ __   ___ _ __ 
            \ \ /\ / / | '_ \| '_ \ / _ \ '__|
             \ V  V /| | | | | | | |  __/ |   
              \_/\_/ |_|_| |_|_| |_|\___|_|   
        '''
        
        self.logo_game = '''

        _                                                        _ 
        | |                                                      | |
        | |  _ __  _   _ _ __ ___     __ _  __ _ _ __ ___   ___  | |
        | | | '_ \| | | | '_ ` _ \   / _` |/ _` | '_ ` _ \ / _ \ | |
        |_| | | | | |_| | | | | | | | (_| | (_| | | | | | |  __/ |_|
        (_) |_| |_|\__,_|_| |_| |_|  \__, |\__,_|_| |_| |_|\___| (_)
                                    __/ |                         
                                    |___/                          
        '''
        self.guidance = '''
        -----------------guidance-----------------
        |welcome to the num game!
        |in this game you need to guess a number between 0 and 1000000;
        |if you guess right, you win;
        |if you guess wrong, you will get a hint;
        |if you want to quit the game, just input 'exit', and you will see the result on the sreen;
        |wish you have a good time!
        '''
        self.user_name = "passenger"

        self.menu = '''
        -----------------menu-----------------
        |1. start the game
        |2. show the winner
        |3. show guidance
        |4. exit the game
        '''

    def begin_page(self):
        print(self.logo_game)
        print(self.guidance)
        self.user_name = input("before the game,please just input your name: ")
        print("hello %s, now you can start the game!\n" % self.user_name)
        while True:
            print(self.menu)
            choice = input("<please input your choice>--→ ")
            if choice == "1":
                self.start_game()
                print("\033c")
                print(self.logo_game)
            elif choice == "2":
                print("\033c")
                self.show_winner()
            elif choice == "3":
                #清除终端
                print("\033c")
                print(self.logo_game)
                print(self.guidance)
            elif choice == "4":
                self.exit_game()
            else:
                print("please input the right number!!!")
                continue


    def start_game(self):
        str = "start_game" + "," + self.user_name + "," + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ","
        self.socket_port.sendto(str.encode(), self.addr)
        # response, addr = self.socket_port.recvfrom(1024)
        # print(response.decode())
        while True:
            guess = input("please input your guess: ")
            str1 = "guess" + ","  + self.user_name + "," + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "," + guess + ","
            self.socket_port.sendto(str1.encode(), self.addr)
            response, addr = self.socket_port.recvfrom(1024)
            print(response.decode())
            if response.decode() == "correct!\n":
                print("you win a game!")
                print("3 seconds later, you will return to the menu!")
                time.sleep(3)
                return
            elif response.decode() == "exit":
                return
            else:
                continue

    def show_winner(self):
        print(self.logo_winner)
        self.socket_port.sendto("show_winner,".encode(), self.addr)
        response, addr = self.socket_port.recvfrom(1024)
        winner_list = response.decode().split(",")
        if(len(winner_list)==1):
            print("\t!no one win the game!\n")
            return
        for i in range(0, len(winner_list), 2):
            print(
                '''
                \t👑%s win with %s times👑
                ''' % (winner_list[i], winner_list[i+1])
        )


    def exit_game(self):
        print("bye bye!")
        self.socket_port.close()
        sys.exit(0)


if __name__ == "__main__":
    client = game_client()
    client.begin_page()
    
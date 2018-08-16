#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'LotteWong'

'''
    该脚本用于微信私聊和群聊时类QQ的自动回复和类小娜的机器回复：其中对所有人开启自动回复，对特定人开启机器回复。
    后面注册的同类型消息会覆盖之前注册的同类型消息。
    search_friends(msg['FromUserName'])['NickName']是微信昵称，search_friends()['UserName']是机器号码。
'''

import itchat
from itchat.content import *
import requests, json
import time

# 处理私聊情况
@itchat.msg_register([TEXT, CARD, FRIENDS, PICTURE, RECORDING, VIDEO, ATTACHMENT, SHARING, MAP, NOTE, SYSTEM], isFriendChat=True)
def handle_friendchat(msg):
    global auto_reply
    global robot_reply, member_list

    FromFriendName = itchat.search_friends(userName=msg['FromUserName'])['NickName']

    print(FromFriendName)
    print(msg['Content'])

    # 开启自动回复模式
    if FromFriendName == MyName and msg['Content'] == 'Auto Reply Mode on':
        auto_reply = True
        itchat.send_msg('自动回复模式已开启', toUserName=msg['FromUserName'])
    elif FromFriendName == MyName and msg['Content'] == 'Auto Reply Mode off':
        if auto_reply == True:
            auto_reply = False
            itchat.send_msg('自动回复模式已关闭', toUserName=msg['FromUserName'])
        else:
            itchat.send_msg('自动回复模式未开启', toUserName=msg['FromUserName'])
    # 开启机器回复模式
    elif msg['Content'] == '。。。':
        robot_reply = True
        member_list.append(FromFriendName)
        itchat.send_msg('%s机器回复模式已开启' % FromFriendName, toUserName=MyUserName)
    elif msg['Content'] == '(':
        if robot_reply == False:
            itchat.send_msg('%s机器回复模式未开启' % FromFriendName, toUserName=MyUserName)
        else:
            robot_reply = False
            ToFriendName = itchat.search_friends(userName=msg['ToUserName'])['NickName']
            member_list.remove(ToFriendName)
            itchat.send_msg('%s机器回复模式已关闭' % ToFriendName, toUserName=MyUserName)

    if robot_reply == True and FromFriendName in member_list and FromFriendName != MyName:
        # 机器回复
        print('Robot Reply Mode [%s] works on %s' % (robot_reply, FromFriendName))
        time.sleep(1)
        str_msg = requests.get('http://www.tuling123.com/openapi/api?key=82f2c605257442e8b81b87d7db58d87b&info=%s' % msg['Content']).content.decode('utf-8')
        dict_msg = json.loads(str_msg)
        if dict_msg['code'] == 100000:
            itchat.send(dict_msg['text'], toUserName=msg['FromUserName'])
        elif dict_msg['code'] == 200000:
            itchat.send(dict_msg['url'], toUserName=msg['FromUserName'])
        elif dict_msg['code'] == 302000:
            itchat.send(dict_msg['list'], toUserName=msg['FromUserName'])
        elif dict_msg['code'] == 308000:
            itchat.send(dict_msg['list'], toUserName=msg['FromUserName'])
    else:
        if auto_reply == True and FromFriendName != MyName:
            # 自动回复
            print('Auto Reply Mode [%s] works on %s' % (auto_reply, FromFriendName))
            time.sleep(1)
            itchat.send_msg('[自动回复]我现在不在噢，等下再回复你吧xoxo', toUserName=msg['FromUserName'])

# 处理群聊情况
@itchat.msg_register([TEXT, CARD, FRIENDS, PICTURE, RECORDING, VIDEO, ATTACHMENT, SHARING, MAP, NOTE, SYSTEM], isGroupChat=True)
def handle_groupchat(msg):
    global auto_reply

    GroupName = itchat.update_chatroom(msg['FromUserName'])['NickName']

    # 若被@到
    if msg['isAt']:
        print(GroupName)
        print(msg['Content'])

        if auto_reply == True:
            # 机器回复
            time.sleep(1)
            itchat.send_msg('[自动回复]我现在不在噢，等下再回复你吧xoxo', toUserName=msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)

    auto_reply = False
    robot_reply = False

    MyName = itchat.search_friends()['NickName']
    MyUserName = itchat.search_friends()['UserName']
    member_list = []

    itchat.run()

#撤回时机器回复的处理可以整合
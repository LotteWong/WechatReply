# WechatReply
---  

#### 项目介绍
该脚本用于微信私聊和群聊时**类QQ的自动回复和类小娜的机器回复**，其中对所有人开启自动回复，对特定人开启机器回复。

#### 包含文件
- `wechat_auto_reply.py`

#### 实现原理
1. **设置关键词**和**特定收发人**来**改变标记变量** `auto_reply` 和`robot_reply` 的值
2. **先判断机器回复**，**再判断自动回复**，这样两者才不会重复
3. 自动回复的内容可以**自定义**，机器回复依赖于**图灵机器人**提供的接口

#### 注意事项
- 后面注册的同类型消息会覆盖之前注册的同类型消息
- `search_friends(msg['FromUserName'])['NickName']` 是微信昵称；`search_friends()['UserName']` 是机器号码  
- 微信昵称用于检索信息，机器号码用于收发信息  
- `auto_reply` 和 `robot_reply` 应定义为全局变量；`MyName` 和 `MyUserName` 应在登录后才能赋值

#### 如何运行
1. 复制本目录下的所有文件至本地  
2. 打开相关解释器，运行 `wechat_auto_reply.py` 即可  

#### 操作指南
- 首次需要扫码登录，在一定时间内支持热加载即无须重复扫码登录  
- **私聊时**：用户本人向自己发送关键词可开启或关闭自动回复；好友向用户本人发送关键词可开启机器回复，用户本人向自己发送关键词可关闭机器回复  
- **群聊时**：只有在自动回复打开且被 @ 到时才能启用  
- 该脚本作用于微信端，在解释器端会显示相关操作信息  

#### Bug
- 若出现生僻字或其它罕见符号，可能会出现乱码和报错的情况  
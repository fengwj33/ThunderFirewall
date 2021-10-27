# ThunderFirewall
# 4.10
本程序是一个基于SDN软件定义网络技术的一个网络游戏访问控制程序
## 功能介绍
监控SDN交换机下设备的流量，将用户账号（学生）与用户计算机网卡绑定，以实现流量控制的功能。具体功能是监控学生的流量，若是访问了规则内的游戏服务器地址， 则将连接情况（单位时间的流量）记入日志，并开始计时。到达具体指定的时间后，则断开其与游戏服务器的连接，同时向老师与家长发送邮件通知，但是规则外的流量 不受限制也不做记录。在学生休息了一段时间后（如5小时，演示时为了方便，时间设定得比较短），便可继续与游戏服务器进行通信。
## 技术简介
本程序使用python编写，SDN控制器底层使用openflow1.3与复数台SDN交换机进行通信，北向接口为Socket实现的一个基于命令的接口，总控制器通过北向接口与复数个 SDN控制器进行通信交互，因此仅需一个总控制器便可同时控制大量SDN交换机。部署在校园寝室楼极为适合。
上层使用webpy作为web服务器，一方面与总控制器进行交互获取数据，另一方面提供丰富的api接口供前端页面调用。
前端页面使用了bootstrap框架，与后端通信使用了ajax交互json来进行。
下面为整体的架构图：
![1.png](https://i.loli.net/2021/06/14/68YrqKGQDfadJoi.png)
## 视频演示
<iframe src="http://47.102.99.174:8080/static/GreenBarDemo.mp4" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>
<!--
### 用户编辑界面：
![avatar](http://45.78.37.214/static/Proj8_02.png)

### 联网规则编辑界面：
![avatar](http://45.78.37.214/static/Proj8_03.png)
-->
### 流量曲线查看界面：
![2.png](https://i.loli.net/2021/06/14/KfI3b9arCHeAJi2.png)

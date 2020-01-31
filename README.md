 ncov_2019_spider
-----
2019 冠状病毒疫情爬虫。疫情数据可视化。

## 项目背景
疫情数据分析

## 数据来源
丁香医生，从1.24号开始采集入库，所以工程包含了24号后的数据。

## 数据展示
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/WeChat%20Image_20200131111804.jpg )  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/WeChat%20Image_20200131111836.png )  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/WeChat%20Image_20200131111846.png)  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/WeChat%20Image_20200131111920.png )  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/2.jpg)  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/3.jpg)  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/4.jpg)  
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/5.jpg)  



## 技术栈
1. mongodb 用于存储采集数据
2. mysql 5.7 用于存储从mogodb采集的数据
3. python 3.7 采集数据和转换mongodb数据到mysql
4. 工程在win10 和 macOS 下测试通过。

## FAQ
1. 为什么要用2套数据库  
一部分用户不知道使用nosql。包括作者自己在做一些查询的时候还是sql来得顺手。

## 联系方式
WeChat  :  ajun-guo


----

## 安装和部署
 
#### mongodb 用于采集的数据库入库
安装方法for mac :https://www.runoob.com/mongodb/mongodb-osx-install.html
启动mongo 方法：
mongod --dbpath d:/workspace/mongodb
export PATH=/usr/local/mongodb/bin:$PATH && sudo mongod

#### mysql server安装

##### 卸载mysql(非必要操作)
```bash
sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
rm -rf ~/Library/PreferencePanes/My*
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
sudo rm -rf /var/db/receipts/com.mysql.*
networksetup -setairportpower en0 off && networksetup -setairportpower en0 on

下载 ： http://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.10-osx10.9-x86_64.dmg
安装方法：https://www.cnblogs.com/kimbo/p/8724595.html
root@localhost: 4O=ucCLx9y%3
/usr/local/mysql-5.7.10-osx10.9-x86_64/bin
```



##### 重置mysql密码(非必要操作)
```
1. 关闭mysql服务
sudo /usr/local/mysql/support-files/mysql.server stop 或者系统偏好里有个 MySQL 里关闭
2.来到mysql目录下
/usr/local/mysql-5.7.10-osx10.9-x86_64/bin
3.得到权限
sudo su
4.重启mysql服务
./mysqld_safe --skip-grant-tables &? 或者在系统编号中开启
5.重开终端
mysql -uroot -p （提示输入密码时随便输入即可
6. 拿到权限（可以修改密码）
flush privileges;
7.修改密码
set password for 'root'@'localhost'=password('root');
set password for 'root'@'localhost'=password('root');
```
 
#### 安装navicat for mysql
下载地址：http://www.pc6.com/mac/111878.html
打开终端，输入：sudo spctl --master-disable 回车，打开偏好设置的安全性与隐私，允许任何来源，重新打开Navicat for MySQL就OK了



#### 安装python依赖包
python3 -m pip install -r requirements.txt



### 工程说明
crawler.py 是爬虫启动的入口文件
python crawler.py 
启动后，就会循环不间断爬取，将数据入库到mongo

spider.py 是mongo 2 mysql 做数据转换的
主要是方便可以使用sql 做数据查询和研究。
也需要启动，启动实时转换数据到mysql
python spider.py

数据库名称：ncov
查询实例见：业务.sql

表 ：
1. dxyarea  省级数据
2. dxyarea_city 地市级数据 
3. dxyoverall 疫情数据概览 
![](https://github.com/junguoguo/ncov_2019_spider/raw/master/image/1.jpg )


----
### 启动工程
1. 启动数据库
export PATH=/usr/local/mongodb/bin:$PATH && sudo mongod
2. 启动数据转换（mongo 2 mysql）
cd /Users/HE/Desktop/ncov_spider/ && python3  spider.py
3. 启动爬虫（每天都要启动爬，启动不关机就会一直爬每天自动）
cd /Users/HE/Desktop/ncov_spider/ && python3  main.py 

以上3个命令，都开启一个新的终端执行。
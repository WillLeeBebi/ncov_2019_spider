
mongodb 用于采集的数据库入库
安装方法for mac :https://www.runoob.com/mongodb/mongodb-osx-install.html
启动mongo 方法：
mongod --dbpath d:/workspace/mongodb
export PATH=/usr/local/mongodb/bin:$PATH && sudo mongod

mysql 安装
卸载mysql
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

重置密码
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

 


安装navicat
http://www.pc6.com/mac/111878.html
打开终端，输入：sudo spctl --master-disable 回车，打开偏好设置的安全性与隐私，允许任何来源，重新打开Navicat for MySQL就OK了


安装依赖包

python3 -m pip install -r requirements.txt


crawler.py 是爬虫启动的入口文件
python crawler.py 
启动后，就会循环不间断爬取，将数据入库到mongo

spider.py 是mongo 2 mysql 做数据转换的
主要是方便可以使用sql 做数据查询和研究。
也需要启动，启动实时转换数据到mysql
python spider.py


#第一步：启动数据库
sudo pkill mongod
export PATH=/usr/local/mongodb/bin:$PATH && sudo mongod
#第二步：启动数据转换（mongo 2 mysql）
cd /Users/HE/Desktop/ncov_spider/ && python3  spider.py
# 第三部：启动爬虫（每天都要启动爬，启动不关机就会一直爬每天自动）
cd /Users/HE/Desktop/ncov_spider/ && python3  main.py 

以上3个命令，都开启一个新的终端执行。

数据库名称：ncov
查询实例见：业务.sql

表 ：
dxyarea  省级数据
dxyarea_city 地市级数据



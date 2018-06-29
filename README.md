### 世界杯赛程赛况API小项目

#### 安装部署

##### 获取代码
git clone https://github.com/Gopfu/WorldCupAPI.git

##### 安装python依赖包
pip install -r WorldCupAPI/requirments.txt

##### 初始化数据库并启动爬虫获取信息，并启动项目
cd WorldCupAPI
启动爬虫，默认30分钟更新一次信息
python update.py &
启动API服务
python app.py &

##### http:server_ip:5000 浏览器打开linux服务器地址进行访问

###### 获取所有32强所有球队，要求使用分页(参数page和per_page分别代表第几页和每页多少条记录)

http://server_ip:5000/groups?&page=2&pre_page=4

###### 获取每个小组净胜球最多的球队

http://server_ip:5000/truegoals

###### 获取比分差距最大的3场比赛记录(按照比赛日期逆序排序)

http://server_ip:5000/scorediff

###### 获取每个小组晋级的两只球队(排名优先级：积分、净胜球、球队名)

http://server_ip:5000/advance

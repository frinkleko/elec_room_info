# Elec Room Info: SCUT 宿舍水电空调余额提醒

## 功能

### v0.1.0

- [x] 水电空调余额跟踪
- [x] 余额不足报警
- [x] 充值检测
- [x] 邮件消息订阅

## 准备

- 一台长期运行的计算机，联网即可，不需要校园网。
- 校园一卡通web页面token（获取方式参考：企业微信 > 校园一卡通 > 复制网页链接 > 浏览器打开 > F12 Cookie > Session_ID）
- 编辑配置文件，参考[config.ini](/sample_config.ini)

## 运行

### docker(推荐)

构建docker镜像

`docker build -t elec_room_info:latest .`

创建运行目录

`mkdir project_dir && cd project_dir`

`mkdir data && cd data`

`mkdir configs && cd configs`

将配置文件放于`project_dir/data/configs`目录下

运行docker容器，替换容器映射路径

`docker run -v /path/to/elec_room_info:/app/data`

### 运行源代码

python 3.8

`pip install -r requirement.txt`

生成默认配置文件：

`python3 elec_room_info/utils/config.py`

运行程序

`python3 elec_room_info/main.py -c config.ini`

## Todos

- [ ] 用电日报
- [ ] 剩余水电时间估计
- [ ] 后端api
- [ ] 微信小程序接入
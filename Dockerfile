FROM python:3.8

WORKDIR /app

COPY elec_room_info/ /app/elec_room_info/
COPY requirements.txt .

RUN mkdir data && mkdir data/configs && mkdir data/logs && mkdir data/records

# 设置时区为东八区（中国标准时间）
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

# 安装依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

ENV PYTHONPATH=/app

RUN python3 ./elec_room_info/utils/config/config_omega.py

EXPOSE 7010

CMD ["python3", "./elec_room_info/main.py", "-c", "data/configs/config.yaml"]
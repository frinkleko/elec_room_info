FROM python:3.8

LABEL version=0.0.1

WORKDIR /app

COPY . /app

# 设置时区为东八区（中国标准时间）
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

# 安装依赖
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

EXPOSE 7010

CMD ["python3", "utils/config.py"]
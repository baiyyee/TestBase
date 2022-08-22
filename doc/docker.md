- Dockerfile

```console

FROM python:3.7-slim-stretch


ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure -f ${DEBIAN_FRONTEND} tzdata


RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && echo "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib" > /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian-security stretch/updates main" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list \
    && echo "deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >> /etc/apt/sources.list


RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set global.extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple/


RUN mkdir -p /usr/share/man/man1 && mkdir /usr/lib/x86_64-linux-gnu/fonts && apt-get update && apt-get install --no-install-recommends -y \
    default-jre \
    wget gzip cron vim \
    libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit python3-dev build-essential \
    wkhtmltopdf \
    && pip install --no-cache-dir cython \
    && pip install --no-cache-dir thriftpy \
    && pip install --no-cache-dir WeTest \
    && rm -rf /var/lib/apt/lists/*


ENV ALLURE_VERSION 2.19.0

RUN wget https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/$ALLURE_VERSION/allure-commandline-$ALLURE_VERSION.tgz -O allure-commandline-$ALLURE_VERSION.tgz \
    && tar -zxvf allure-commandline-$ALLURE_VERSION.tgz -C /opt/ \
    && rm allure-commandline-$ALLURE_VERSION.tgz \
    && ln -s /opt/allure-$ALLURE_VERSION/bin/allure /usr/bin/allure


COPY doc/fonts/simsun.ttc /usr/lib/x86_64-linux-gnu/fonts

```


- Docker CMD

```console

docker build -f Dockerfile -t hehuabo/wetest:latest .
docker push hehuabo/wetest:latest

```
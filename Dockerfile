FROM octahub.8lab.cn:5000/base/py-node:3.8-16.18 

ENV project "chain-monitor-example"

#ADD docker/sources.list /etc/apt/
ADD ./ /usr/local/${project}
WORKDIR /usr/local/${project}

RUN apt-get update && apt-get install -y libssl-dev --no-install-recommends && apt-get install -y libsqlite3-dev \
    && groupadd -r ubuntu -g 1000 && useradd -r -g ubuntu ubuntu -u 1000 -m -s /bin/bash -d /home/ubuntu \
    && chown -R ubuntu:ubuntu /usr/local/${project} \
    && mkdir /var/log/$project && chown -R ubuntu:ubuntu  /var/log/$project/ 
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt
COPY --chown=1000:1000 docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh
#USER ubuntu
ENTRYPOINT ["/entrypoint.sh"]


FROM ubuntu:20.04

ENV PYTHONUNBUFFERED=1

EXPOSE 8001

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y git
RUN apt-get install -y libssl-dev 
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

RUN mkdir -p /home/application
COPY requirements.txt /home/application
WORKDIR /home/application

# RUN pip3 install --upgrade pip
RUN set -ex
RUN pip3 install -r requirements.txt
# RUN pip install -U pyopenssl
RUN export LC_ALL=C.UTF-8
RUN export LANG=C.UTF-8

COPY . .

WORKDIR /home/application/HTTP2/sender
RUN ls
CMD ["uvicorn", "sender:app", "--port", "8001", "--host", "0.0.0.0"]
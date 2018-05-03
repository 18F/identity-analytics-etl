FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git
RUN apt-get install -y zip

# update pip
RUN python3.6 -m pip install --upgrade pip==9.0.3
RUN python3.6 -m pip install wheel
RUN cd /usr/local/bin && ln -s /usr/bin/python3 python

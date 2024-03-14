FROM python:3.8-bookworm
# FROM python:3.9-bookworm
# FROM python:3.10.12-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN apt-get update -y -qq && apt-get install -y -qq cmake libopenmpi-dev python3-dev zlib1g-dev libgl1-mesa-glx swig g++ git 

RUN pip install numpy 

# TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

# RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

# RUN apt-get install -y vim iputils-ping telnet
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install TA-Lib==0.4.28
RUN pip install -U numpy==1.23.5
RUN pip install int_date==0.1.8
RUN pip install plotly==5.19.0

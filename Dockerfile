FROM python:3.12

WORKDIR /api

COPY pyproject.toml /api

RUN apt-get update \
  && apt-get -y install gcc git curl openssh-server \
  && apt-get clean

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test
RUN  echo 'test:test' | chpasswd

RUN service ssh start
RUN /usr/sbin/sshd

EXPOSE 22

RUN python -m pip install --upgrade pip
RUN pip install trio
RUN pip install python-dotenv
RUN pip install -U -q google-generativeai
RUN pip install -qU streamlit

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry lock && poetry install

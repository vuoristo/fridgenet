FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3.5 build-essential python3-pip
RUN apt-get install -y git
RUN git clone https://github.com/vuoristo/fridgenet
WORKDIR fridgenet
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["runserver.py"]



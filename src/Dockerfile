FROM ubuntu:latest
MAINTAINER Daniel Gisolfi
EXPOSE 4400
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
RUN apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential\
    tzdata
    
#Set the TimeZone 
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure tzdata

WORKDIR /Miele
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["Miele.py"]

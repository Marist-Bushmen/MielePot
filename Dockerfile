FROM ubuntu:latest
MAINTAINER Daniel Gisolfi
EXPOSE 4400
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
WORKDIR /Miele
COPY /src .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["Miele.py"]

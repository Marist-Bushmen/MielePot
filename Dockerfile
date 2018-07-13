FROM ubuntu:latest
MAINTAINER Daniel Gisolfi
EXPOSE 4400
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
WORKDIR /Miele
COPY /src .
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["Miele.py"]

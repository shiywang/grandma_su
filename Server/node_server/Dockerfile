FROM node:latest
WORKDIR /code
COPY . /code/

RUN npm install -g npm@7.5.3 --silent
RUN npm install --quiet
RUN npm install zeromq
RUN npm install ip
RUN npm install socket.io

EXPOSE 3000
EXPOSE 5456
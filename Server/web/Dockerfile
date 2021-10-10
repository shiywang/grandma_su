FROM node:latest

WORKDIR /code
ENV PATH /code/care_app/node_modules/.bin:$PATH
COPY package.json ./
ADD package.json /code/package.json
COPY . .

RUN npm install react
RUN npm install -g npm@7.5.3 --silent
RUN npm install socket.io-client
RUN npm install -g react-scripts 


EXPOSE 3000



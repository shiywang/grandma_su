FROM node:latest
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN npm install react
RUN npm install -g npm@7.5.3 --silent
RUN npm install socket.io-client
RUN npm install -g react-scripts 

# ENV PATH /code/care_app/node_modules/.bin:$PATH
RUN cd /code/care_app/; yarn install

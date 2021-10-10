FROM node:latest
WORKDIR /code
COPY package*.json ./
ADD package.json /code/package.json
COPY . /code/

RUN npm install -g npm@7.5.3 --silent
RUN npm install socket.io-client
RUN npm install -g react-scripts 
COPY . .
EXPOSE 3000

ENV PATH /code/care_app/node_modules/.bin:$PATH

CMD ["npm", "start"]
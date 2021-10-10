FROM node:latest

WORKDIR /code
#ENV PATH /code/care_app/node_modules/.bin:$PATH
COPY package.json ./
ADD package.json /code/package.json
COPY . .

RUN npm cache clean --force
RUN npm install -g npm@latest --silent
RUN npm install socket.io-client
RUN npm install -g react-scripts 


EXPOSE 3000


#CMD ["npm", "start", "--prefix",  "care_app/"]
FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install solc

CMD ["node", "compile.js"]

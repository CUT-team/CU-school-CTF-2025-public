FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm install ethers express

EXPOSE 3000

CMD ["node", "deploy.js"]

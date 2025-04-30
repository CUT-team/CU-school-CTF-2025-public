FROM node:20

RUN npm install -g ganache
WORKDIR /app

COPY ./build-files ./build-files
COPY ./deployer/deploy.js ./deploy.js
COPY ./deployer/package.json ./package.json
RUN npm install

RUN apt-get update && apt-get install -y netcat-openbsd

EXPOSE 8545

CMD ["sh", "-c", "\
ganache --host 0.0.0.0 --mnemonic \"$MNEMONIC\" \
  --account=\"$ACCOUNT1\" \
  --account=\"$ACCOUNT2\" \
  --port=8545 & \
while ! nc -z localhost 8545; do sleep 1; done; \
node deploy.js"]

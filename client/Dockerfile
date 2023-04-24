FROM node:16-alpine3.17

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

EXPOSE 5000

CMD ["yarn", "dev"]
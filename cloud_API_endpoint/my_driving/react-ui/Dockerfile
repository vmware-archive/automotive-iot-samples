FROM node:10.9.0

COPY . .

# install dependencies
RUN yarn

# build app
RUN yarn build

RUN yarn global add serve

CMD serve -s build -l 4001




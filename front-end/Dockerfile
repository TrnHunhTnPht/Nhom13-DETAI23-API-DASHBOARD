# FROM node:lts-alpine
# # install simple http server for serving static content
# RUN npm install -g http-server
# # make the 'app' folder the current working directory
# WORKDIR /app
# # copy 'package.json' to install dependencies
# COPY package*.json ./
# # install dependencies
# RUN npm install
# # copy files and folders to the current working directory (i.e. 'app' folder)
# COPY . .
# # build app for production with minification
# RUN npm run build
# EXPOSE 8080
# CMD [ "http-server", "dist" ]
# # CMD ["npm", "run", "serve"]

# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
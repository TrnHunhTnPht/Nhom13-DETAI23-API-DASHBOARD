# Chọn hình ảnh cơ sở cho frontend
FROM node:lts-alpine as build-stage

# Thiết lập thư mục làm việc
WORKDIR /app

# copy 'package.json' to install dependencies
COPY package*.json ./

# Cài đặt các gói phụ thuộc và xây dựng ứng dụng Vue.js
RUN npm install

# copy files and folders to the current working directory (i.e. 'app' folder)
COPY . .

RUN npm run build

# Hình ảnh cuối cùng với Nginx để phục vụ ứng dụng
FROM nginx as production-stage

RUN mkdir /app

# Sao chép tệp được xây dựng từ frontend vào thư mục của Nginx
COPY --from=build-stage /app/dist /app

# Sao chép tệp cấu hình Nginx
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

# Mở cổng 80 để phục vụ ứng dụng
EXPOSE 80

# Chạy Nginx
CMD ["nginx", "-g", "daemon off;"]
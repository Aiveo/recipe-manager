FROM node:12.20 AS build
WORKDIR /opt/ng
COPY recipe-manager/package.json ./
RUN npm install
COPY recipe-manager/. ./
RUN node_modules/.bin/ng build

FROM httpd:2.4
COPY .htaccess /usr/local/apache2/htdocs/
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY --from=build /opt/ng/dist/frontend /usr/local/apache2/htdocs/

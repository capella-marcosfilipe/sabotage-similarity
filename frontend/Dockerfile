FROM nginx:1.27-alpine

RUN apk add --no-cache gettext

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY docker-entrypoint.sh /docker-entrypoint.d/40-generate-config.sh
COPY config.template.js /usr/share/nginx/html/config.template.js
COPY index.html /usr/share/nginx/html/index.html
COPY style.css /usr/share/nginx/html/style.css
COPY script.js /usr/share/nginx/html/script.js
COPY config.js /usr/share/nginx/html/config.js

RUN chmod +x /docker-entrypoint.d/40-generate-config.sh

EXPOSE 80

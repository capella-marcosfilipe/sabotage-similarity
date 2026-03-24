#!/bin/sh
set -eu

: "${API_BASE_URL:=}"
: "${API_PROXY_UPSTREAM:=}"

if [ -n "$API_PROXY_UPSTREAM" ]; then
cat > /etc/nginx/conf.d/default.conf <<EOF
server {
  listen 80;
  server_name _;

  root /usr/share/nginx/html;
  index index.html;

  location = /health {
    access_log off;
    add_header Content-Type text/plain;
    return 200 'ok';
  }

  location /api/ {
    proxy_pass http://${API_PROXY_UPSTREAM}/;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
  }

  location / {
    try_files \$uri \$uri/ /index.html;
  }
}
EOF
else
cat > /etc/nginx/conf.d/default.conf <<EOF
server {
  listen 80;
  server_name _;

  root /usr/share/nginx/html;
  index index.html;

  location = /health {
    access_log off;
    add_header Content-Type text/plain;
    return 200 'ok';
  }

  location / {
    try_files \$uri \$uri/ /index.html;
  }
}
EOF
fi

envsubst '${API_BASE_URL}' \
  < /usr/share/nginx/html/config.template.js \
  > /usr/share/nginx/html/config.js

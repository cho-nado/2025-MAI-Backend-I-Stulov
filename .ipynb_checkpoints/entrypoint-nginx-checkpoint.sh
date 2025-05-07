#!/bin/sh
set -e

if [ -n "$BASIC_AUTH_USER" ] && [ -n "$BASIC_AUTH_PASSWORD" ] && [ ! -f /etc/nginx/.htpasswd ]; then
    htpasswd -b -c /etc/nginx/.htpasswd \
      "$BASIC_AUTH_USER" "$BASIC_AUTH_PASSWORD"
fi

exec nginx -g "daemon off;"

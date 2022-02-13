#!/bin/bash
while ! mysqladmin ping -h"db" -P"3306" --silent; do
    echo "Waiting for MySQL to be up..."
    sleep 1
done
flask db migrate
flask db upgrade
flask init
flask run --host=0.0.0.0

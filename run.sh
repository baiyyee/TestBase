#!/bin/bash


# crontab
cp ./cron /etc/cron.d/cron
chmod 0644 /etc/cron.d/cron
crontab /etc/cron.d/cron
service cron restart


# env
printenv >> /etc/environment


# run pytest
$PYTEST_CMD


# allure report
allure serve -h 0.0.0.0 -p 8080 ./allure-result	

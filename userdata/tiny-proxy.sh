#!/bin/bash

amazon-linux-extras install epel
yum -y update
curl ifconfig.me/ip
yum -y install tinyproxy
systemctl enable tinyproxy
sed -i 's/^Allow.*$/Allow 172.31.0.0\/16/g' /etc/tinyproxy/tinyproxy.conf
systemctl start tinyproxy

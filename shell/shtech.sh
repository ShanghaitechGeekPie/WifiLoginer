#!/bin/sh
echo "Shanghaitech Login Shell"

num=$#
if [ "$num" = "2" ]; then
        curl -H "Content-Type: application/x-www-form-urlencoded" -X POST -v --data "userName=$1&password=$2&hasValidateCode=false&authLan=zh_CN"  --cookie "JSESSIONID=D56359E00B58C7877668AAB44B3BFE31"  https://controller.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction\!login.action
else
    echo "使用方法 ./shtech.sh 用户名 密码"
fi

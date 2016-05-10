#!/bin/sh
echo "Shanghaitech Login Shell"
echo "上科大登陆器shell版本"
num=$#
if [ "$num" = "2" ]; then
       result=` curl -H "Content-Type: application/x-www-form-urlencoded" -X POST -s --data "userName=$1&password=$2&hasValidateCode=false&authLan=zh_CN"  --cookie "JSESSIONI$
        resultSucess=`echo "$result" | sed "s/.*success\W*\(\w*\)\W*total.*/\1/g"`
        #echo "$resultSucess"
        if [ "$resultSucess"x = "true"x ]; then
                sucess=`echo "$result" | sed "s/.*account\W*\(\w*\)\W*accountRemainDays.*ip\W*\([0-9\.]*\)\W*login.*/Your account is \1 \nYour ip is  \2/g" `
                sucessZh=`echo "$result" | sed "s/.*account\W*\(\w*\)\W*accountRemainDays.*ip\W*\([0-9\.]*\)\W*login.*/你登陆的账号为 \1 \n你登陆的ip地址为  \2/g" `
                echo "登陆成功"
                echo "Success"
                echo "$sucess"
                echo "$sucessZh"
        else
                erros=`echo "$result" | sed "s/.*message\W*\([^\"]*\)\W*success.*/\1/g"`
                echo "$erros"
                echo "登陆失败"
                echo "请重新登陆"
                echo "Log in failed , Please try again"
                exit
                fi
else
    echo "使用方法 ./shtech.sh 用户名 密码"
    echo "Usage ./shtech.sh username password"
fi

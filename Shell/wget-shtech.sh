#!/bin/sh

echo "


 _______  _______  _______  _        _______ _________ _______ 
(  ____ \(  ____ \(  ____ \| \    /\(  ____ )\__   __/(  ____ \

| (    \/| (    \/| (    \/|  \  / /| (    )|   ) (   | (    \/
| |      | (__    | (__    |  (_/ / | (____)|   | |   | (__    
| | ____ |  __)   |  __)   |   _ (  |  _____)   | |   |  __)   
| | \_  )| (      | (      |  ( \ \ | (         | |   | (      
| (___) || (____/\| (____/\|  /  \ \| )      ___) (___| (____/\

(_______)(_______/(_______/|_/    \/|/       \_______/(_______/

"


echo $geekpie
echo "Shanghaitech Login Shell"
echo "Use wget"
echo "上科大登陆器shell版本"
num=$#
if [ "$num" = "2" ]; then
       #result=` curl -k -H "Content-Type: application/x-www-form-urlencoded" -X POST -s --data "userName=$1&password=$2&hasValidateCode=false&authLan=zh_CN"  --cookie "JSESSIONID=D56359E00B58C7877668AAB44B3BFE31"  https://controller.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction\!login.action`
        result=`wget -q --header="Content-Type: application/x-www-form-urlencoded"  --no-check-certificate   \
			       --header="Cookie:JSESSIONID=D56359E00B58C7877668AAB44B3BFE31"    \
		               --post-data="userName=$1&password=$2&hasValidateCode=false&authLan=zh_CN" \
				https://controller.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction\!login.action -O-`

	resultSucess=`echo "$result" | sed "s/.*success\W*\(\w*\)\W*token.*/\1/g"`
        #echo "$resultSucess"
        if [ "$resultSucess"x = "true"x ]; then
                sucess=`echo "$result" | sed "s/.*account\W*\(\w*\)\W*accountRemainDays.*ip\W*\([0-9\.]*\)\W*isNeedBindTel.*/Your account is \1 \nYour ip is  \2/g" `
                sucessZh=`echo "$result" | sed "s/.*account\W*\(\w*\)\W*accountRemainDays.*ip\W*\([0-9\.]*\)\W*isNeedBindTel.*/你登陆的账号为 \1 \n你登陆的ip地址为  \2/g" `
                echo "登陆成功"
                echo "

 _______           _______  _______  _______  _______  _______ 
(  ____ \|\     /|(  ____ \(  ____ \(  ____ \(  ____ \(  ____ \

| (    \/| )   ( || (    \/| (    \/| (    \/| (    \/| (    \/
| (_____ | |   | || |      | |      | (__    | (_____ | (_____ 
(_____  )| |   | || |      | |      |  __)   (_____  )(_____  )
      ) || |   | || |      | |      | (            ) |      ) |
/\____) || (___) || (____/\| (____/\| (____/\/\____) |/\____) |
\_______)(_______)(_______/(_______/(_______/\_______)\_______)
                                                               
"
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

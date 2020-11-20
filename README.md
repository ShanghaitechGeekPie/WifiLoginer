# **WifiLoginer**
上海科技大学网络自动验证登录器

这里有多位同学写的不同版本，大家可以根据介绍自行选用。



----------


### **EZNetLoginer**
作者：吕文涛

环境：Linux/Mac OS X/Windows/Android/UNIX Like

语言：Python 2.5+

实现登录功能、Heartbeat保持登录、记住密码、语言切换

----------


### **WifiLoginer**
作者：陈宸

环境：OS with ruby

语言：Ruby

实现登录功能

--------


### **Shtulogin**


作者：邓岂

环境：Linux/Mac OS X/Windows etc.

语言：Golang

基本的登录功能实现

--------

### **CURL**

作者：邓岂

环境：Linux/Mac OS X/Windows etc.

语言:shell 脚本


**需要curl**

1.命令行下直接：

```shell
curl -k -H "Content-Type: application/x-www-form-urlencoded" -X POST -v --data \
"userName=(你的用户名)&password=(你的密码)&hasValidateCode=false&authLan=zh_CN"  \
--cookie "JSESSIONID=D56359E00B58C7877668AAB44B3BFE31" \
https://controller.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction\!login.action
```

2.Shell 脚本:

```
./shtech.sh 用户名 密码
```

3.用wget
wget支持下载的时候认证，所以也可以用来做认证

```shell
wget --header="Content-Type: application/x-www-form-urlencoded"  \
--no-check-certificate   \
--header="Cookie:JSESSIONID=D56359E00B58C7877668AAB44B3BFE31"    \
--post-data="userName=(用户名)&password=（密码）&hasValidateCode=false&authLan=zh_CN" \
https://controller.shanghaitech.edu.cn:8445/PortalServer//Webauth/webAuthAction\!login.action \
```
----------


### **UWPLoginer**

作者：夏寅岑

环境：Windows 10 higher than version 1511(10586)

语言：C# & XAML

实现登录功能、记住密码、后台自动登陆*

---

### **Shtulogin**

作者：邓岂

环境：Windows only. 需要 Poweshell  > 4.0.

语言：

1. 基本的登录功能
2. 保持连接
3. 账号密码的本地存储（交互式）
4. 优雅的配色

---

### **launchd**

作者：荆玉琢

环境：macOS (only), 欢迎 port 到 systemd

语言：shell & launchd

1. 连上 Wi-Fi 后自动判断是否为ShanghaiTech，并自动进行登录
2. 可设定重试次数

使用方式：

1. 先用你最喜欢的编辑器打开`launchd/shtechlogin` 文件，修改`username`和`password`变量，然后在命令行中

```shell
chmod +x shtechlogin
cp shtechlogin /usr/local/bin/shtechlogin
```

此时若`/usr/local/bin/` 在`PATH` 中，则可直接通过命令行运行`shtechlogin` 进行一次性登录

2. 将服务文件添加到系统launchd托管

```shell
sed "s/WHOAMI/$(whoami)/g" org.geekpie.wifiloginer.plist > ~/Library/LaunchAgents/org.geekpie.wifiloginer.plist
launchctl load ~/Library/LaunchAgents/org.geekpie.wifiloginer.plist
```

此后每次接入ShanghaiTech都会自动进行登录，生成的log文件在`~/Library/Logs/shtechlogin.log`，可以用Console.app进行查看。

---

### **Auth-esp32-to-ShanghaiTech-wifi**

repo链接：https://github.com/ShanghaitechGeekPie/Auth-esp32-to-ShanghaiTech-wifi

作者：徐博文

环境：ESP32（arduino框架，去掉freertos部分大概可以port到其他支持arduino框架的板子上）

语言：C++

| 函数 | 用途 |
|  ----  | ----  |
| connect_to_ShanghaiTech() | 连接ShanghaiTech并验证 |
| connect_to_eduroam() | 连接eduroam并验证 |
| check_internet_connectivity() | 检查互联网连接 |

使用方式：

1. * 使用PlatformIO管理dependency  
     *此lib已提交registry，正等待moderation*  
   * 您亦可手动管理dependency  

2. 按需要引入头文件并调用相关函数，见examples文件夹内的样例  
   * ```#include <ShanghaiTechWifiAuth.h>``` for SSID:ShanghaiTech authentication  
   * ```#include <eduroam.h>``` for eduroam authentication  
   * ```#include <connectivity_util.h>``` for simple connectivity check  

---

### **ShanghaiTechLogin**

**Author**: Kiruya Momochi\
**Language**: PowerShell Core\
**Environment**: Windows PowerShell or PowerShell Core\
**Features**: Credential saving, Heartbeat, Auto relogin

#### Install

```powershell
Install-Module ShanghaiTechLogin
```

#### Basic Usage

```powershell
stulogin
```

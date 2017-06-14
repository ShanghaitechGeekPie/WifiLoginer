#!/usr/bin/env python3
 
import urllib
import urllib.parse
import urllib.request
import http.client
import string, random
import json
import getpass
import time

#======================================================
#自动登录请输入账号密码，留空将询问
username = ''
password = ''
#======================================================
#语言
lang = 'ZH'
#======================================================

print('')
if lang == 'ZH':
	print(u'上海科技大学 校园网络自动登录助手')
	print(u'开发:上海科技大学 信息科学与技术学院 吕文涛')
	print(u'开发版本，严禁外传')
else:
	print(u'ShanghaiTech EZNetLoginer')
	print(u'Developer : eastpiger (Lv Wentao) , SIST , ShanghaiTech University')
	print(u'Under development')
	
print(u'========================================')
httpClient = None
try:
	if username == '':
		if lang == 'ZH':
			print(u'请输入登录账号：',end="")
		else:
			print(u'Username:',end="")
		username = input('')
	if password == '':
		if lang == 'ZH':
			print(u'请输入登录密码（密码并不会在此处显示，请直接输入即可）：',end="")
		else:
			print(u'Password:',end="")
		password = getpass.getpass('')
	print('')
	if lang == 'ZH':
		print(u'读取到账号。')
	else:
		print(u'account got.')
	print(u'========================================')

	while True:
		#======================================================
		#Define
		url="https://controller1.net.shanghaitech.edu.cn:8445/PortalServer/Webauth/webAuthAction!login.action"
		params = urllib.parse.urlencode({'userName': username, 'password':password,'hasValidateCode':False,'authLan':'zh_CN'})
		cookie_code = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 32)).replace(' ','')
		headers = {'Content-type': 'application/x-www-form-urlencoded'
						, 'Accept': '*/*','Cookie':'JSESSIONID=' + cookie_code}
		httpClient = http.client.HTTPSConnection('controller1.net.shanghaitech.edu.cn', 8445, timeout=30)
		#======================================================

		if lang == 'ZH':
			print(u'正在登录……',end="")
		else:
			print(u'Logining……',end="")
		httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!login.action', params, headers)
		response = httpClient.getresponse()
		if response.status != 200:
			if lang == 'ZH':
				print(u'连接失败！请确认网络已经连接')
			else:
				print(u'Connection Failed! Is the network available?')
			connect()
			exit()
		else:
			response_data = response.read().decode('utf-8')
			response_data_json = json.loads(response_data)
			if response_data_json['success'] != True:
				if lang == 'ZH':
					print(u'登录失败！请确认账号可用')
				else:
					print(u'Login Failed! Is your account available?')
				print(response_data)
				exit()
			else:
				if lang == 'ZH':
					print(u'成功！')
					print(u'登录账号：' + response_data_json['data']['account'])
					print(u'内网ip：' + response_data_json['data']['ip'])
				else:
					print(u'Success!')
					print(u'Username:' + response_data_json['data']['account'])
					print(u'ClientIP:' + response_data_json['data']['ip'])

		print(u'========================================')
		#======================================================
		#Define
		params2 = urllib.parse.urlencode({'userName': username, 'clientIp':response_data_json['data']['ip']})
		#======================================================
		
		timer = 0
		while True:
			if timer==10:
				break
			timer=timer+1
			if lang == 'ZH':
				print(u'心跳信号……',end="")
			else:
				print(u'Heartbeat……',end="")
			httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!hearbeat.action', params2, headers)
			response = httpClient.getresponse()
			if response.status != 200:
				if lang == 'ZH':
					print(u'连接失败！请确认网络已经连接')
				else:
					print(u'Connection Failed! Is the network available?')
					break
			else:
				response_data = response.read().decode('utf-8')
				response_data_json = json.loads(response_data)
				if response_data_json['success'] != True:
					if lang == 'ZH':
						print(u'失败！请确认账号可用')
					else:
						print(u'Failed! Is your account available?')
					print(response_data)
					break
				else:
					if lang == 'ZH':
						print(u'成功！')
					else:
						print(u'Success!')
			time.sleep(120)
		print(u'========================================')
		
except Exception as e:
	if lang == 'ZH':
		print(u'未知错误，请确认网络已经连接')
	else:
		print(u'Unknown Error! Is the network available?')
	print(e)
finally:
	if httpClient:
		httpClient.close()

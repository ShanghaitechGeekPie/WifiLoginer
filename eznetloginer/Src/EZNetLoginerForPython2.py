#!/usr/bin/env python2
#coding=utf8
import httplib, urllib
import string, random
import json
import getpass
import time
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding( "utf-8" )

with open('./user.conf','a+') as f:
	pass
with open('./user.conf','r') as f:
	if f.read()=='':
		#还没有配置
		print 'choose language: EN or ZH'
		lang = raw_input('')
		print ''
		if lang == 'EN':
			print u'ShanghaiTech EZNetLoginer'
			print u'Developer : eastpiger (Lv Wentao) , SIST , ShanghaiTech University'
			print u'Under development'
			print u'username'
			username = raw_input('')
			print u'password'
			passowrd = getpass.getpass('')

		else:
			print u'上海科技大学 校园网络自动登录助手'
			print u'开发:上海科技大学 信息科学与技术学院 吕文涛'
			print u'开发版本，严禁外传'
			print u'请输入登录账号：',
			username = raw_input('')
			print u'请输入登录密码'
			password = getpass.getpass('')
	else:
		cf = ConfigParser.ConfigParser()
		cf.read('./user.conf')
		username = cf.get('user','username')
		password = cf.get('user','password')
		lang = cf.get('user','lang')

with open('./user.conf','w') as f:
	f.write('[user]\nusername = '+ username + '\npassword = '+ password + '\nlang = '+lang)

httpClient = None

try:
	while True:
		#======================================================
		#Define
		params = urllib.urlencode({'userName': username, 'password':password,'hasValidateCode':False,'authLan':'zh_CN'})
		cookie_code = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a','1','2','3','4','5','6','7','8','9','0'], 32)).replace(' ','')
		headers = {'Content-type': 'application/x-www-form-urlencoded'
						, 'Accept': '*/*','Cookie':'JSESSIONID=' + cookie_code}
		httpClient = httplib.HTTPSConnection('controller1.net.shanghaitech.edu.cn', 8445, timeout=30)
		#======================================================

		if lang == 'ZH':
			print u'正在登录……',
		else:
			print u'Logining……',
		httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!login.action', params, headers)
		response = httpClient.getresponse()
		if response.status <> 200:
			if lang == 'ZH':
				print u'连接失败！请确认网络已经连接'
			else:
				print u'Connection Failed! Is the network available?'
			connect()
			exit()
		else:
			response_data = response.read()
			response_data_json = json.loads(response_data)
			if response_data_json['success'] <> True:
				if lang == 'ZH':
					print u'登录失败！请确认账号可用'
				else:
					print u'Login Failed! Is your account available?'
				print response_data
				exit()
			else:
				if lang == 'ZH':
					print u'成功！'
					print u'登录账号：' + response_data_json['data']['account']
					print u'内网ip：' + response_data_json['data']['ip']
				else:
					print u'Success!'
					print u'Username:' + response_data_json['data']['account']
					print u'ClientIP:' + response_data_json['data']['ip']

		print u'========================================'
		#======================================================
		#Define
		params2 = urllib.urlencode({'userName': username, 'clientIp':response_data_json['data']['ip']})
		#======================================================
		
		timer = 0
		while True:
			if timer==10:
				break
			timer=timer+1
			if lang == 'ZH':
				print u'心跳信号……',
			else:
				print u'Heartbeat……',
			httpClient.request('POST', '/PortalServer/Webauth/webAuthAction!hearbeat.action', params2, headers)
			response = httpClient.getresponse()
			if response.status <> 200:
				if lang == 'ZH':
					print u'连接失败！请确认网络已经连接'
				else:
					print u'Connection Failed! Is the network available?'
					break
			else:
				response_data = response.read()
				response_data_json = json.loads(response_data)
				if response_data_json['success'] <> True:
					if lang == 'ZH':
						print u'失败！请确认账号可用'
					else:
						print u'Failed! Is your account available?'
					print response_data
					break
				else:
					if lang == 'ZH':
						print u'成功！'
					else:
						print u'Success!'
			time.sleep(120)
		print u'========================================'
		
except Exception, e:
	if lang == 'ZH':
		print u'未知错误，请确认网络已经连接'
	else:
		print u'Unknown Error! Is the network available?'
	print e
finally:
	if httpClient:
		httpClient.close()

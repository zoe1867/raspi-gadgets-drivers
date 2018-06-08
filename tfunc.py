#!/usr/bin/env python3  
# -*- coding: utf-8 -*- 

import requests
import json
import datetime
import time
import os

#serial module
import serial.tools.list_ports
import serial

#stock module
import tushare as ts
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot
import matplotlib.pyplot as plt 


def getcloseprice(sNum):
    sdf = ts.get_hist_data(sNum,start='2018-01-01',end='2018-05-22')
    sdf1 = sdf.sort_index()
    spd = sdf1['close']
    plt.plot(spd)
    plt.show()


def data2hex(data):
	result = ''
	hLen = len(data)
	for i in range(0,hLen):
		#hvol=ord(data[i])
		hhex='%02x'%data[i]
		result+=' '
		result+=hhex
	return result

def serialwritedata(ser, dat):
	ser.write(dat)
	ser.timeout=3
	data = ser.readall()
	strdata = data2hex(data)
	print(strdata)


def findserialports():
	port_list=list(serial.tools.list_ports.comports())
	if(len(port_list)==0):
		print('找不到串口')
	else:
		for i in range(0,len(port_list)):
			print(port_list[i])

def digitalclock():
    while 1:
	    t = time.strftime('%H:%M:%S',time.localtime(time.time()))
	    print(t)
	    time.sleep(0.999)
	    os.system('cls')

def weather():
	while 1:
		print('*************欢迎进入天气查询系统**************')
		city=input('请输入您要查询的城市名称(按0退出)：')
		if city=='0':
			print('您已退出天气查询系统！')
			break
		else:
			url='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city
			#使用requests发送请求，接受返回的结果
			response=requests.get(url)
			# print(type(response.text))
			#使用loads函数，将json字符串转换为python的字典或列表
			rs_dict=json.loads(response.text)
			#取出error
			error_code=rs_dict['error']
			#如果取出的error为0，表示数据正常，否则没有查询到天气信息
			if error_code==0:
				#从字典中取出数据
				results=rs_dict['results']
				#根据索引取出城市天气信息字典
				info_dict=results[0]
				#根据字典的key 取出城市名称
				city_name=info_dict['currentCity']
				pm25=info_dict['pm25']
				print('当前城市:%s pm值:%s'%(city_name,pm25))
				#取出天气信息列表
				weather_data=info_dict['weather_data']
				#for循环取出每一天天气的小字典
				for weather_dict in weather_data:
					#取出日期、天气、风级、温度
					date=weather_dict['date']
					weather=weather_dict['weather']
					wind=weather_dict['wind']
					temperature=weather_dict['temperature']
					print('%s %s %s %s'%(date,weather,wind,temperature))
			else:
				print('没有查询到天气信息！')


def sum(a,b):
	return a+b

def hord(c):
    return hex(ord(c))


if __name__== "__main__":
    '''
    ser = serial.Serial("COM1",9600)
    cmd = [0x31,0x32]
    serialwritedata(ser,cmd)
    ser.close()
    '''
    #matplotlib.use("Pdf")
    getcloseprice('300136')

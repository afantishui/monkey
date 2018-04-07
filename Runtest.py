# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
sys.path.append("..")
from base.readconfig import getdata_excel

filepath = 'config\\monkey.xlsx'
case = getdata_excel(filepath)
cmd = 'ipconfig > c:\monkey\1.txt'
# b = os.popen('adb devices')
# print(b.read())

def start():

	path = os.getcwd()
	day = time.strftime("%Y%m%d%H%M", time.localtime(time.time())) # 获取日期
	info_filename = '%s-info.txt'%day
	logpath1 = path+'\\log\\'+info_filename
	logpath2 = path+'\\log\\%s-error.txt'%day
	cmd = 'adb shell monkey -p'+' '+case + ' 2>' + logpath2 + ' 1>' + logpath1
	print(cmd)
	
	os.popen(cmd)
	print('ok')
	time.sleep(2)
	while True:
		with open(logpath1, encoding='utf-8') as monkeylog:
			time.sleep(1)  # 每1秒采集检查一次
			if monkeylog.read().count('Monkey finished') > 0:
				print("测试完成")
				break

if __name__ == '__main__':
	start()		

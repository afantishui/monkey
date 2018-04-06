# -*- coding:utf-8 -*-
import sys
import xlrd
import xlsxwriter
import os
import time
import datetime
import yaml

def getdata_excel():
	filepath = '..\\config\\monkey.xlsx'
	file	 = xlrd.open_workbook(filepath) # 打开Excel
	excel 	 = file.sheets()[0]     # 实例Excel表
	ncols 	 = excel.ncols			# 获取表列数
	case_list= []				# 存放命令行数组
	
	# 读取Excel的配置
	for i in range(1,ncols):
		case = excel.cell(1,i).value
		if case != 'null':
			case_list.append(case)
		else:
			continue

	# 拼接语句
	case1 = case_list[1]
	for i in range(2,len(case_list)-1):
		case1 = str(case1) +' '+ str(case_list[i])
	case1 = case1 +' '+str(int(case_list[len(case_list)-1]))  # 这里单独写是因为Excel的数字读出来是浮点型，在for循环不好处理
	return case1  # 返回完整语句

def get_conf(config):
    # 读取配置
    filepath = open(r'..\config\%s'%(config), encoding='utf-8')
    f_config = yaml.load(filepath)
    case = f_config['adb'][0]
    for i in range(1,len(f_config['adb'])-1):
    	case = case + f_config['adb'][i]
    case = case + str(int(f_config['adb'][len(f_config['adb'])-1]))
    print(case)	
    return case



def run_shell(config):
	case = get_conf(config)
	path = os.path.dirname(os.path.abspath('.')) # 保存报告的相对路径
	day  = time.strftime("%Y%m%d%H%M", time.localtime(time.time())) # 获取日期
	info_log = '%s-monkey-info.txt'%day
	logpath1 = path+'\\logs\\'+ info_log
	cmd = case + ' 1>' + logpath1 + ' 2>&1 &' 
	return cmd,logpath1,info_log
#get_conf('monkey.yml')
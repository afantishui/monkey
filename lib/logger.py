# -*- coding:utf-8 -*-
import logging
import os.path
import time

class Logger(object):
	"""docstring for Logger"""
	def __init__(self, logger):
		#指定保存日志的文件路径，日志基本，一级调用文件
		#将日志存入到指定文件中

		#创建一个logger
		self.logger = logging.getLogger(logger)
		self.logger.setLevel(logging.DEBUG)


		#创建一个handler,用于写入日志文件
		rq = time.strftime('%Y%m%d%H%M',time.localtime(time.time())) #获取当前时间
		#path = os.path.abspath('..') #如果把运行文件InterfaceRuntest放到外面，改为获取绝对路径，如果改回之前放在文件夹内则改回下面的相对路径
		log_path = os.path.dirname(os.path.abspath('.')) + '\\logs\\'  #项目根目录下/logs保存日志
		#log_path = path + '\\logs\\'
		log_name = log_path + rq + '.log'  #设置日志文件名
		fh = logging.FileHandler(log_name) #日志输出到文件
		fh.setLevel(logging.INFO)  #设置日志显示等级CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

		#创建一个handler，用于输出到控制台
		ch = logging.StreamHandler()
		ch.setLevel(logging.INFO)

		#定义handler的输出格式
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)

		#给logger添加handler
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

	def getlog(self):
		return self.logger

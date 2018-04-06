# -*- coding: utf-8 -*-
import sys,os,time,datetime
sys.path.append("..")
from Base.readconfig import run_shell
from Base.analysis import AnalysisLog
from Base.monkeyBase import AndroidBaseOperation
from lib.Excel_reportx import create_monkey_report

def start():
	phoneMsg = AndroidBaseOperation()
	print("开始")
	cmd,logpath,info_log = run_shell('monkey.yml') #获得执行语句
	starttime = time.strftime("%Y-%m-%d %X",time.localtime())
	os.popen(cmd) #执行语句
	time.sleep(2) #延时
	#判断是否完成
	while True:
		with open(logpath, encoding='utf-8') as monkeylog:
			time.sleep(1)  # 每1秒采集检查一次
			if monkeylog.read().count('Monkey finished') > 0:
				print("测试完成")
				break
	And_version,phone_name = phoneMsg.getModel() #安装系统版本 手机品牌 手机名
	AnrMsg,CrashMsg,ExceptionMsg,process_name,run_count,run_time,ANR_count,CRASH_count,Exception_count = AnalysisLog(logpath) #返回分析日志信息，错误信息，进程名，运行次数，运行时间，错误统计
	filetime  = datetime.datetime.now().strftime("%Y%m%d%H%M%S") #记录时间
	basdir   = os.path.dirname(os.path.abspath('.')) #保存报告的相对路径
	filepath  = os.path.join(basdir + '\\test_report\\%s-monkey_Stressresult.xls' %filetime) #设置保存路径
	#生成Excel报告
	create_monkey_report(filename = filepath, test_time = starttime, test_machine = phone_name,
				process_name = process_name, run_count = run_count, run_time = run_time, 
				ANR_count = ANR_count, CRASH_count = CRASH_count, Exception_count = Exception_count, 
				cmd = cmd, AnrMsg = AnrMsg, CrashMsg = CrashMsg, ExceptionMsg = ExceptionMsg)
	print("OK")

if __name__ == '__main__':
	start()

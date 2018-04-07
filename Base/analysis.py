# -*- coding: utf-8 -*-
'''
	分析monkey日志
'''
import re
log = "..\\logs\\201709301756-monkey-info.txt"  # 测试调试使用
def AnalysisLog(log):
	log_msg 	 = []
	AnrMsg       = []
	CrashMsg     = []
	ExceptionMsg = []

	with open(log,encoding = "utf-8") as log:
		lines = log.readlines()
		for line in lines:
			if re.findall(":Monkey:",line):
				a = line.split("=")
				run_count = a[2]

			if re.findall(":AllowPackage:",line):
				b = line.split(" ")
				process_name = b[1]

			if re.findall("//   0:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[0]) 

			if re.findall("//   1:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[1]) 

			if re.findall("//   2:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[2]) 

			if re.findall("//   3:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[3])

			if re.findall("//   4:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[4]) 

			if re.findall("//   5:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[5]) 

			if re.findall("//   6:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[6]) 

			if re.findall("//   7:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[7])

			if re.findall("//   8:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[8]) 

			if re.findall("//   9:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[9]) 

			if re.findall("//   10:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[10]) 

			if re.findall("//   11:",line):
				a = line.split(" ")
				log_msg.append(a[4])
				print(log_msg[11])

			if re.findall("ANR",line):
				AnrMsg.append(line)
				print("存在ANR错误:" + line)

			if re.findall("CRASH",line):
				CrashMsg.append(line)
				print("存在CRASG错误:" + line)	

			if re.findall("Exception",line):
				ExceptionMsg.append(line)
				print("存在Exception错误:" + line)

			if re.findall("## Network",line):
				c = line.split(" ")
				time = c[9]
				time1 = time.split('m')
				run_time = int(int(time1[0])/1000)
				print(run_time)


	ANR_count 		= len(AnrMsg)
	CRASH_count 	= len(CrashMsg)
	Exception_count = len(ExceptionMsg)

	return AnrMsg,CrashMsg,ExceptionMsg,process_name,run_count,run_time,ANR_count,CRASH_count,Exception_count
#AnalysisLog(log)
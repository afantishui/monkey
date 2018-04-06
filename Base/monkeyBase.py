#-*- coding: utf-8 -*-
'''
	get_devices() 获取devices		
	get_pid() 获取pid		
	get_package_and_activity() 获取当前应用的包名与activity
	getModel() 获取设备信息			
	getDisplay() 获取分辨率 	
	getipconf() 获取ip mac
	getMeminfo() 内存
	getCPUMsg()	 CPU
	get_battery() 电量
	get_flow()	流量
	fps()	fps
	timestamp() 时间戳
	install_apk()
	uninstall_apk()
	start_activity(activity)
	stop_app(apk_name)
	input(text)
	screenshot(savepath,pic_name)
'''
import os
import time
import re
import subprocess

class AndroidBaseOperation(object):

	# 获取devices
	def get_devices(self):
		devices =[]
		cmd = "adb devices"
		output = subprocess.check_output(cmd).decode()
		a = output.split()
		if len(a) < 0:
			print('not found devices')
		else:	
			for i in range(0,len(a)):
				
				if a[i] == "device":
					devices.append(a[i-1])
		#print(devices)
		return devices


	# 获取pid
	def get_pid(self,apk_name):
		cmd = "adb shell ps | grep " + apk_name
		output = subprocess.check_output(cmd).decode()
		#print(output)
		if output == "":
			return "the process doesn't exist"
		result = output.split()
		return result[1]

	# 获取设备上当前应用的包名与activity
	def get_package_and_activity(self):
		cmd  = 'adb shell "dumpsys window w | grep \/ | grep name= | cut -d = -f 3 | cut -d \) -f 1"'
		cmd1 = 'adb shell "dumpsys window w | grep \/ | grep name= | cut -d = -f 3 | cut -d / -f 1"'
		output   = subprocess.check_output(cmd).decode()
		output1  = subprocess.check_output(cmd1).decode()
		activity = output.split()[0]
		apk_name = output1.split()[0]
		print(activity)
		print(apk_name)
		return apk_name,activity

	# 获取设备信息 系统版本号 手机品牌 手机名
	def getModel(self):	
		cmd = "adb shell cat /system/build.prop"
		cmd1 = "adb shell getprop ro.product.model"
		output = subprocess.check_output(cmd).decode()
		And_version1 = re.findall("version.release=([\d+\.+]*)",output,re.S)[0] #  Android 系统  #re.S  表示“.”的作用扩展到整个字符串，包括“\n”
		And_version2 = re.findall("version.sdk=(\d+)*",output,re.S)[0]
		phone_model1 = re.findall("ro.product.brand=(\S+)*",output,re.S)[0] # 手机品牌
		phone_model2 = os.popen(cmd1).read().strip(':')
		And_version = And_version1 + '(SDK:' + And_version2 +')'
		phone_name  = phone_model1 + '-' + phone_model2
		print(And_version)
		print(phone_name)
		return And_version,phone_name
		#这里取设备信息使用了两种不同的方法，是因为用subprocess拿设备名时拿不到空格后面的名称，
		#改用os.popen后续可优化正则进行匹配

	# 获取屏幕分辨率
	def getDisplay(self):
		cmd = 'adb shell wm size'
		output = subprocess.check_output(cmd).decode()
		Display =  re.findall("Physical size: (\d+\S\d+)*",output,re.S)[0]
		print(Display)
		return Display

	# 获取IP MAC地址
	def getipconf(self):
		cmd = 'adb shell ifconfig'
		output = subprocess.check_output(cmd).decode()
		ip =  re.findall("inet addr:([\d+.]+)*",output,re.S) # ip
		if len(ip)<2:
			if ip[0] == "127.0.0.1":
				print('没有连接网络')
		else:
			IP = ip[1]
			print(IP)
			return IP

		#mac = re.findall("inet6 addr: ([\w+\s+(\w+)]*)",output,re.S)[0] # mac
		print(ip)
		#print(mac)
		print(output)

	# 获取CPU信息
	def getCPUMsg(self):
		cmd = "adb shell cat /proc/cpuinfo"
		output = subprocess.check_output(cmd).decode()
		cpu_msg =  re.findall("Processor	: ([\w+\s+(\w+)]*)",output,re.S)[0] # CPU
		cpu_kel = len(re.findall("processor",output)) # cpu核数
		print('--------CUP----------')
		print(output)
		print(cpu_msg)
		return cpu_msg,cpu_kel

	# 获取内存信息
	def getMeminfo(self,apk_name):
		cmd = "adb shell dumpsys meminfo %s" %(apk_name)
		output = subprocess.check_output(cmd).split()
		s_mem = ".".join([x.decode() for x in output]) #转换为string
		s_mem2 = int(re.findall("TOTAL.(\d+)*",s_mem,re.S)[0])
		print('---------men----------')
		print(s_mem2)
		return s_mem2

	# 获取CPU核数
	def get_cpu_kel(self,devices):
		cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
		#print(cmd)
		output = subprocess.check_output(cmd).split()
		sitem = ".".join([x.decode() for x in output])
		cpu_kel = len(re.findall("processor",sitem))
		#print(cpu_kel)
		return cpu_kel

	# 获取CPU使用情况
	'''获取cpu快照'''
	def totalCpuTime(self,devices):
		user = nice = system = idle = iowait = irq = softirq = 0
		'''
		user:从系统启动开始累计到当前时刻，处于用户态的运行时间，不包含 nice值为负进程。
    	nice:从系统启动开始累计到当前时刻，nice值为负的进程所占用的CPU时间
    	system 从系统启动开始累计到当前时刻，处于核心态的运行时间
    	idle 从系统启动开始累计到当前时刻，除IO等待时间以外的其它等待时间
    	iowait 从系统启动开始累计到当前时刻，IO等待时间(since 2.5.41)
    	irq 从系统启动开始累计到当前时刻，硬中断时间(since 2.6.0-test4)
    	softirq 从系统启动开始累计到当前时刻，软中断时间(since 2.6.0-test4)
    	stealstolen  这是时间花在其他的操作系统在虚拟环境中运行时（since 2.6.11）
    	guest 这是运行时间guest 用户Linux内核的操作系统的控制下的一个虚拟CPU（since 2.6.24）
		'''
		cmd = "adb -s " + devices + " shell cat /proc/stat"
		# print(cmd)
		p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
		(output, err) = p.communicate()
		res = output.split()

		for info in res:
			if info.decode() == "cpu":
				user    = res[1].decode()
				nice    = res[2].decode()
				system  = res[3].decode()
				idle    = res[4].decode()
				iowait  = res[5].decode()
				irq     = res[6].decode()
				softirq = res[7].decode()
				#print("user=" + user)
				#print("nice=" + nice)
				#print("system=" + system)
				#print("idle=" + idle)
				#print("iowait=" + iowait)
				#print("irq=" + irq)
				#print("softirq=" + softirq)
				result = int(user) + int(nice) + int(system) + int(idle) + int(iowait) + int(irq) + int(softirq)
				#print("totalCpuTime: " + str(result))
				return result

	'''
	每一个进程快照
	'''
	def processCpuTime(self,pid,devices):
		'''
		pid 	进程号
		utime   该任务在用户态运行的时间，单位为jiffies
    	stime   该任务在核心态运行的时间，单位为jiffies
    	cutime  所有已死线程在用户态运行的时间，单位为jiffies
    	cstime  所有已死在核心态运行的时间，单位为jiffies
		'''
		utime = stime = cutime = cstime = 0
		cmd = "adb -s " + devices + " shell cat /proc/" + pid + "/stat"
		# print(cmd)
		p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
		(output,err) = p.communicate()
		res = output.split()
		utime = res[13].decode()
		stime = res[14].decode()
		cutime = res[15].decode()
		cstime = res[16].decode()
		# print("utime="+ utime)
		# print("stime="+ stime)
		# print("cutime="+ cutime)
		# print("cstime="+ cstime)
		result = int(utime) + int(stime) + int(cutime) + int(cstime)
		# print("ProcessCpuTime=" + str(result))
		return result
	'''
	计算某进程的cpu使用率
	100*( processCpuTime2 – processCpuTime1) / (totalCpuTime2 – totalCpuTime1) (按100%计算，如果是多核情况下还需乘以cpu的个数);
	cpukel cpu几核
	pid 进程id
	'''
	def cup_rate(self,pid,cpukel,devices):
		processCpuTime1 = self.processCpuTime(pid,devices)
		totalCpuTime1   = self.totalCpuTime(devices)
		time.sleep(20)
		processCpuTime2 = self.processCpuTime(pid,devices)
		processCpuTime3 = processCpuTime2 - processCpuTime1
		print("processCpuTime3:%s"%processCpuTime3)


		# time.sleep(5)
		totalCpuTime2 = self.totalCpuTime(devices)
		totalCpuTime3 = (totalCpuTime2 - totalCpuTime1)*cpukel
		print("totalCpuTime3:%s" %totalCpuTime3)

		cpu = 100 * (processCpuTime3) / (totalCpuTime3)
		print(cpu)


	# 获取电池电量
	def get_battery(self,devices):
		cmd = "adb -s " + devices + " shell dumpsys battery"
		#print(cmd)
		output      = subprocess.check_output(cmd).split()
		st          = ".".join([x.decode() for x in output]) # 转换为string
		usb_power   = str(re.findall("USB.powered:.(\w+)*", st, re.S)[0]) # 是否连接usb充电
		voltage     = int(re.findall("voltage:.(\d+)*", st, re.S)[0]) # 电压
		temperature = int(re.findall("temperature:.(\d+)*", st, re.S)[0])/10 # 温度
		battery2    = int(re.findall("level:.(\d+)*", st, re.S)[0]) #电量
		print("------温度---------")
		print(temperature)
		print("------电量---------")
		#print(st)
		#print(usb_power)
		#print(voltage)
		#print(temperature)
		print(battery2)
		return usb_power,voltage,temperature,battery2

	# 获取上下行流量
	def get_flow(self,pid, type, devices):
		# pid = get_pid(pkg_name)
		_flow1 = [[], []]
		if pid is not None:
			cmd = "adb -s " + devices + " shell cat /proc/" + pid + "/net/dev"
			print(cmd)
			_flow = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
										stderr=subprocess.PIPE).stdout.readlines()
			for item in _flow:
				if type == "wifi" and item.split()[0].decode() == "wlan0:":  # wifi
					# 0 上传流量，1 下载流量
					_flow1[0].append(int(item.split()[1].decode()))
					_flow1[1].append(int(item.split()[9].decode()))
					up_flow = [tuple(m) for m in _flow1] 
					#up_flow = up_flow[1,-1]
					#up_flow = int(str(_flow1[0]))/1024
					#dowm_flow = int(str(_flow1[1]))/1024
					print("------flow---------")
					print(up_flow)
					#print(dowm_flow)
					break
				if type == "gprs" and item.split()[0].decode() == "rmnet0:":  # gprs
					print("-----flow---------")
					_flow1[0].append(int(item.split()[1].decode()))
					_flow1[1].append(int(item.split()[9].decode()))
					up_flow = int(_flow1[0])/1024
					dowm_flow = int(_flow1[1])/1024
					print("------flow---------")
					print(up_flow)
					print(dowm_flow)
					break
					print(_flow1)
					break
		else:
			_flow1[0].append(0)
			_flow1[1].append(0)

	#获取fps值
	def fps(self,apk_name, devices):
		_adb = "adb -s " + devices +" shell dumpsys gfxinfo %s" % apk_name
		#print(_adb)
		results = os.popen(_adb).read().strip()
		frames = [x for x in results.split('\n')]
		#print(frames)
		frame_count = len(frames)
		#print(frame_count)
		jank_count = 0
		vsync_overtime = 0
		render_time = 0
		for frame in frames:
			time_block = re.split(r'\s+', frame.strip())
			if len(time_block) == 3:
				try:
					render_time = float(time_block[0]) + float(time_block[1]) + float(time_block[2])
				except Exception as e:
					render_time = 0

			'''
			当渲染时间大于16.67，按照垂直同步机制，该帧就已经渲染超时
			那么，如果它正好是16.67的整数倍，比如66.68，则它花费了4个垂直同步脉冲，减去本身需要一个，则超时3个
			如果它不是16.67的整数倍，比如67，那么它花费的垂直同步脉冲应向上取整，即5个，减去本身需要一个，即超时4个，可直接算向下取整

			最后的计算方法思路：
			执行一次命令，总共收集到了m帧（理想情况下m=128），但是这m帧里面有些帧渲染超过了16.67毫秒，算一次jank，一旦jank，
			需要用掉额外的垂直同步脉冲。其他的就算没有超过16.67，也按一个脉冲时间来算（理想情况下，一个脉冲就可以渲染完一帧）

			所以FPS的算法可以变为：
			m / （m + 额外的垂直同步脉冲） * 60
			'''
			if render_time > 16.67:
				jank_count += 1
				if render_time % 16.67 == 0:
					vsync_overtime += int(render_time / 16.67) - 1
				else:
					vsync_overtime += int(render_time / 16.67)

		_fps = int(frame_count * 60 / (frame_count + vsync_overtime))

		# return (frame_count, jank_count, fps)
		#print(frame_count)
		#print(jank_count)
		#print(vsync_overtime)
		print("-----fps------")
		print(_fps)


	# 时间戳
	def timestamp(self):
		return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

	# adb命令
	def adb(self,args):
		global serialno_num
		if serialno_num == "":
			devices = get_device_list()
			if len(devices) == 1:
				# global serialno_num
				serialno_num = devices[0]
			else:
				root = tk.Tk()
				window = Window(devices, root)
				window.show_window()    
		cmd = "%s -s %s %s" %(command, serialno_num, str(args))
		return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# adb shell命令
	def shell(self,args):  
		cmd = "adb shell %s" %(str(args))
		print(cmd)
		return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	# --------------------apkmanager-----------------#
	# 安装应用
	def install_apk(self):
		pass

	# 卸载应用
	def uninstall_apk(self):
		pass

	# 调起应用界面
	def start_activity(self,activity):
		cmd = "adb shell am start -n %s" %(activity)
		print(cmd)
		subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print('start --%s'%activity)

	# 关闭应用
	def stop_app(self,apk_name):
		cmd = "adb shell am force-stop %s" %(apk_name)
		print(cmd)
		subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print('stop --- %s'%apk_name)

	# --------------------mouse&keyboard-----------------#
	# 点击事件
	def click(self,x,y,timeout):
		cmd = 'adb shell input tap %s %s'%(x,y)
		#print(cmd)
		os.system(cmd)
		time.sleep(timeout)

	# 双击
	def doubleclick(self,x,y,timeout):
		self.click(x, y, timeout)
		self.click(x, y, timeout)

	# 输入文本
	def input(text):
		cmd = "adb shell input text %s"%(text)
		subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print('input --- %s'%text)

	# 截图方式1
	def screenshot(self,savepath,pic_name):
		screen_save_path =pic_name + '.png'
		# 截图到SD卡上
		cmd1 = "adb shell screencap -p /sdcard/monkey/%s"%(screen_save_path)
		# 导出到电脑
		cmd2 = "adb pull /sdcard/monkey/%s %s"%(screen_save_path,savepath)
		# 删除SD卡图片
		cmd2 = "adb shell rm /sdcard/monkey/%s"%(screen_save_path)
		subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(3)
		subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		time.sleep(2)
		subprocess.Popen(cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		print('screenshot --- %s'%screen_save_path)

	# 截图方式2
	def get_screenshot(self,path):
		# 获取截图 auto.png
		# 把截图保存路径设成可配置
		#imgpath = os.path.abspath('..')
		#path = imgpath + '\\img\\sceneImg\\auto.png'
		process = subprocess.Popen('adb shell screencap -p', shell = True, stdout = subprocess.PIPE)
		screenshot = process.stdout.read()
		# 图片二进制转码
		screenshot = screenshot.replace(b'\r\r\n', b'\n')
		with open(path,'wb') as f:
			f.write(screenshot)
		time.sleep(0.5)
		print('screenshot --- ok')


if __name__ == '__main__':
	#pass
	a = AndroidBaseOperation()
	device = str(a.get_devices())
	devices = device[2:-2]
	#print(devices)
	apk_name, activity = a.get_package_and_activity()
	#pid = a.get_pid(apk_name)
	#print(device)
	#a.get_battery(device[2:10])
	#a.get_flow("758","wifi",device)
	#cpukel = a.get_cpu_kel(device[2:10])
	#a.totalCpuTime(device[2:10])
	#pid = a.get_pid("bayechuanqi")
	#a.cup_rate(pid,cpukel,"c5306b75")
	#a.get_devices()
	#a.get_package_and_activity()
	#a.fps('com.game37.bayechuanqi',"c5306b75")
	#a.getModel()
	#a.getCPUMsg()
	#a.getDisplay()
	#a.getipconf()
	# a.getMeminfo(apk_name)
	#a.getCPUMsg()
	#bb =a.get_battery(devices)[3]
	#print(bb)
	#a.get_flow(pid, 'wifi', devices)
	#a.fps(apk_name, devices)

	#a.get_screenshot()
	a.click(10,20,1)
	print('ok')

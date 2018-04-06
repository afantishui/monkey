#-*- coding: utf-8 -*-
'''
1.接口报告模板
2.monkey报告模板
'''
import xlsxwriter
import yaml

#添加一个加粗格式
def get_format(wd,option = {}):
	return wd.add_format(option)

#设置居中
def get_format_center(wd,num = 1):
	return wd.add_format({'align':'center','valign': 'vcenter','border':num})

def set_border_(wd,num = 1):
	return wd.add_format({}).set_border(num)

#写数据
def write_center(worksheet,cl,data,wd):
	return worksheet.write(cl, data, get_format_center(wd))

#生成饼形图
def pie(workbook,worksheet):
	#创建一个类型为饼状图表
	chart1 = workbook.add_chart({'type':'pie'})
	chart1.add_series({
			'name' : '接口测试统计',
			'categories' : '=测试总况!$D$4:$D$5',
			'values' :     '=测试总况!$E$4:$E$5',
		})

	chart1.set_title({'name':'接口测试统计'})
	chart1.set_style(10)
	worksheet.insert_chart('A9',chart1,{'x_offset':25,'y_offset':10})

#生成接口报告
def create_interface_report(filename,list_len,list_pass,list_fail,listids,listnames,listkeys,listconeents,listurls,listtypes,listexpects,list_json,listresult):
	filepath = open(r'..\\config\\report.yaml', encoding='utf-8')
	file_config = yaml.load(filepath)
	#创建Excel文件
	workbook = xlsxwriter.Workbook(filename)
	#指定Excel表
	worksheet = workbook.add_worksheet("测试总况")
	worksheet2 = workbook.add_worksheet("测试详情")
	#--------------------sheet1操作--------------------#
	#设置worksheet列行的宽高
	worksheet.set_column("A:A",15)
	worksheet.set_column("B:B",20)
	worksheet.set_column("C:C",20)
	worksheet.set_column("D:D",20)
	worksheet.set_column("E:E",20)
	worksheet.set_column("F:F",20)

	worksheet.set_row(1,30)
	worksheet.set_row(2,30)
	worksheet.set_row(3,30)
	worksheet.set_row(4,30)
	worksheet.set_row(5,30)

	define_format_H1 = get_format(workbook,{'bold':True,'font_size':18})
	define_format_H2 = get_format(workbook,{'bold':True,'font_size':14})

	define_format_H2.set_border(1)
	define_format_H1.set_align("vcenter")
	define_format_H1.set_align("center")
	define_format_H2.set_align("vcenter")	#设置垂直居中
	define_format_H2.set_align("center")	#设置水平居中
	define_format_H2.set_bg_color("blue")	#设置背景色
	define_format_H2.set_color("#ffffff")	#字体颜色

	worksheet.merge_range("A1:F1", "测试报告总概况", define_format_H1)
	worksheet.merge_range("A2:F2","测试概括",define_format_H2)
	worksheet.merge_range("A3:A6","pic",get_format_center(workbook))

	write_center(worksheet,"B3","项目名称", workbook)
	write_center(worksheet,"B4","接口版本", workbook)
	write_center(worksheet,"B5","提测人员", workbook)
	write_center(worksheet,"B6","测试人员", workbook)

	#data = {"test_name":"图灵接口测试","test_version":"v2.0.8","test_p1":"张三","test_p2":"李四"}
	write_center(worksheet,"C3",file_config['project_name'],workbook)
	write_center(worksheet,"C4",file_config['interface_version'],workbook)
	write_center(worksheet,"C5",file_config['submit_person'],workbook)
	write_center(worksheet,"C6",file_config['test_person'],workbook)

	write_center(worksheet,"D3","接口总数",workbook)
	write_center(worksheet,"D4","通过总数",workbook)
	write_center(worksheet,"D5","失败总数",workbook)
	write_center(worksheet,"D6","测试日期",workbook)

	#data1 = {"test_sum":100,"test_success":80,"test_failed":20,"test_data":"2017-09-18"}
	write_center(worksheet,"E3",list_len,workbook)
	write_center(worksheet,"E4",list_pass,workbook)
	write_center(worksheet,"E5",list_fail,workbook)
	write_center(worksheet,"E6",file_config["test_time"],workbook)

	write_center(worksheet,"F3","通过率",workbook)
	#百分数处理'%.2f%%' % 后面有连个小数，'%d%%' %后面没有两个小数
	worksheet.merge_range('F4:F6',('%d%%'%(((list_pass)/(list_len))*100)),get_format_center(workbook))
	pie(workbook,worksheet)

	#--------------sheet2操作--------------#
	#设置sheet2列行的宽高
	worksheet2.set_column("A:A",6)
	worksheet2.set_column("B:B",15)
	worksheet2.set_column("C:C",10)
	worksheet2.set_column("D:D",40)
	worksheet2.set_column("E:E",20)
	worksheet2.set_column("F:F",35)
	worksheet2.set_column("G:G",20)
	worksheet2.set_column("H:H",10)

	worksheet2.set_row(1,30)
	worksheet2.set_row(2,30)
	worksheet2.set_row(3,30)
	worksheet2.set_row(4,30)
	worksheet2.set_row(5,30)
	worksheet2.set_row(6,30)
	worksheet2.set_row(7,30)

	worksheet2.merge_range('A1:H1', '测试详情', get_format(workbook, 
		{'bold': True, 
		'font_size': 18 ,
		'align': 'center',
		'valign': 'vcenter',
		'bg_color': 'blue', 
		'font_color': '#ffffff'}))
	write_center(worksheet2, "A2", '用例ID', workbook)
	write_center(worksheet2, "B2", '接口名称', workbook)
	write_center(worksheet2, "C2", '接口协议', workbook)
	write_center(worksheet2, "D2", 'URL', workbook)
	write_center(worksheet2, "E2", '参数', workbook)
	write_center(worksheet2, "F2", '预期值', workbook)
	write_center(worksheet2, "G2", '实际值', workbook)
	write_center(worksheet2, "H2", '测试结果', workbook)

	temp = 2
	for i in range(list_len):
		temp += 1
		write_center(worksheet2, "A"+str(temp), listids[i], workbook)
		write_center(worksheet2, "B"+str(temp), listnames[i], workbook)
		write_center(worksheet2, "C"+str(temp), listtypes[i], workbook)
		write_center(worksheet2, "D"+str(temp), listurls[i], workbook)
		write_center(worksheet2, "E"+str(temp), listkeys[i], workbook)
		write_center(worksheet2, "F"+str(temp), listexpects[i], workbook)
		write_center(worksheet2, "G"+str(temp), str(list_json[i]), workbook)
		write_center(worksheet2, "H"+str(temp), listresult[i], workbook)

	workbook.close()

#------------------------Interface报告分割线--------------------------------------------


#------------------------Monkey报告模板分割线-------------------------------------------
def create_monkey_report(filename,test_time,test_machine,process_name,run_count,run_time,ANR_count,CRASH_count,Exception_count,cmd,AnrMsg,CrashMsg,ExceptionMsg):
	#创建Excel文件
	workbook = xlsxwriter.Workbook(filename)
	#指定Excel表
	worksheet = workbook.add_worksheet("测试总况")
	worksheet2 = workbook.add_worksheet("ANR报错")
	worksheet3 = workbook.add_worksheet("CRASH报错")
	worksheet4 = workbook.add_worksheet("Exception报错")
	#--------------------sheet1操作--------------------#
	#设置worksheet列长
	worksheet.set_column("A:A",20)
	worksheet.set_column("B:B",10)
	worksheet.set_column("C:C",23)
	worksheet.set_column("D:D",10)
	worksheet.set_column("E:E",10)
	worksheet.set_column("F:F",10)
	worksheet.set_column("G:G",10)
	worksheet.set_column("H:H",15)
	worksheet.set_column("I:I",15)
	worksheet.set_column("J:J",16)
	worksheet.set_column("K:K",16)
	worksheet.set_column("L:L",10)
	worksheet.set_column("M:M",20)

	#设置worksheet行高
	worksheet.set_row(1,30)
	worksheet.set_row(2,30)
	worksheet.set_row(3,30)
	worksheet.set_row(4,30)
	worksheet.set_row(5,30)
	worksheet.set_row(6,30)
	worksheet.set_row(7,30)
	worksheet.set_row(8,30)
	worksheet.set_row(9,30)
	worksheet.set_row(10,30)
	worksheet.set_row(11,30)
	worksheet.set_row(12,30)
	worksheet.set_row(13,30)

	define_format_H1 = get_format(workbook,{'bold':True,'font_size':18})
	define_format_H2 = get_format(workbook,{'bold':True,'font_size':14})
	define_format_H3 = get_format(workbook,{'bold':True,'font_size':11})

	define_format_H2.set_border(1)
	define_format_H3.set_border(1)
	define_format_H1.set_align("vcenter")
	define_format_H1.set_align("center")
	define_format_H2.set_align("vcenter")	#设置垂直居中
	define_format_H2.set_align("center")	#设置水平居中
	define_format_H2.set_bg_color("yellow")	#设置背景色
	define_format_H2.set_color("#ffffff")	#字体颜色
	define_format_H3.set_align("vcenter")
	define_format_H3.set_align("center")

	worksheet.merge_range("A1:M1", "Monkey压力测试报告", define_format_H1)
	write_center(worksheet,"A2","测试时间", workbook)
	write_center(worksheet,"B2","测试设备", workbook)
	write_center(worksheet,"C2","进程名", workbook)
	write_center(worksheet,"D2","执行次数", workbook)
	write_center(worksheet,"E2","测试用时", workbook)
	write_center(worksheet,"F2","ANR报错", workbook)
	write_center(worksheet,"G2","CRASH报错", workbook)
	write_center(worksheet,"H2","Exception报错", workbook)
	worksheet.merge_range("I2:M2", "执行语句", define_format_H3)

	write_center(worksheet,"A3",test_time, workbook)
	write_center(worksheet,"B3",test_machine, workbook)
	write_center(worksheet,"C3",process_name, workbook)
	write_center(worksheet,"D3",run_count, workbook)
	write_center(worksheet,"E3",run_time, workbook)
	write_center(worksheet,"F3",ANR_count, workbook)
	write_center(worksheet,"G3",CRASH_count, workbook)
	write_center(worksheet,"H3",Exception_count, workbook)
	worksheet.merge_range("I3:M3", cmd, define_format_H3)

	worksheet2.set_column("A:A",130)
	worksheet3.set_column("A:A",130)
	worksheet4.set_column("A:A",130)
	
	worksheet2.set_row(1,30)
	worksheet3.set_row(1,30)
	worksheet4.set_row(1,30)

	write_center(worksheet2,"A1","ANR报错", workbook)
	write_center(worksheet3,"A1","CRASH报错", workbook)
	write_center(worksheet4,"A1","Exception报错", workbook)

	temp = 2
	if len(AnrMsg) > 0:        
		for i in range(len(AnrMsg)):
                        write_center(worksheet2, "A"+str(temp+i), AnrMsg[i], workbook)
	else:
		write_center(worksheet2, "A2","null", workbook)
                
                
	if len(CrashMsg) > 0:               
		for i in range(len(CrashMsg)):
                        write_center(worksheet3, "A"+str(temp+i), CrashMsg[i], workbook)
	else:
		write_center(worksheet3, "A2", "null", workbook)
                
                
	if len(ExceptionMsg) > 0:                
		for i in range(len(ExceptionMsg)):
                        write_center(worksheet4, "A"+str(temp+i), ExceptionMsg[i], workbook)
	else:
		write_center(worksheet4, "A2", "null", workbook)


	#write_center(worksheet2,"A2",info_log, workbook)
	#write_center(worksheet2,"B2",error_log, workbook)

	workbook.close()



#------------------------Monkey报告模板分割线-------------------------------------------
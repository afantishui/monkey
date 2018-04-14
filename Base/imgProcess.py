# -*- coding:utf-8 -*-
import sys
import getopt
import cv2
import aircv as ac
import os
import numpy as np
#print(cv2.__version__)
def getImgCordinate(filePath,sceneFilePath):
	# 载入图片
	img1 = cv2.imread(filePath)
	img2 = cv2.imread(sceneFilePath)

	# 特征识别初始化
	detector = cv2.AKAZE_create()
	norm = cv2.NORM_HAMMING
	matcher = cv2.BFMatcher(norm)

	if img1 is None:
		print('Failed to load %s'%filePath)
		sys.exit(1)

	if img2 is None:
		print('Failed to load %s'%sceneFilePath)
		sys.exit(1)

	if detector is None:
		print('unknown feature:%s'%feature_name)
		sys.exit(1)

	print('using akaze')
	# 计算特征值
	kp1,desc1 = detector.detectAndCompute(img1,None)
	kp2,desc2 = detector.detectAndCompute(img2,None)
	print('matching...')
	# 特征值匹配
	raw_matches = matcher.knnMatch(desc1,trainDescriptors = desc2, k = 2)
	p1,p2,kp_pairs = filter_matches(kp1, kp2, raw_matches)
	#print(p1,p2,kp_pairs)

	if len(p1) > 4:
		# 获取转换矩阵
		H,status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
		print("%d/%d inliers/matched"%((np.sum(status)), len(status)))
	else:
		H,status = None, None
		print("%d matches found,not enough for findHomography estimation" %len(p1))
	# 获得图像尺寸
	h1, w1 = img1.shape[:2]
	h2, w2 = img2.shape[:2]
	obj_corners = np.float32([[0,0],[w1,0],[w1,h1],[0,h1]])
	obj_corners = obj_corners.reshape(1,-1,2)
	# 映射坐标
	try:
		scene_corners = cv2.perspectiveTransform(obj_corners,H)
		scene_corners = scene_corners.reshape(-1,2)

		# 计算中心坐标
		mid_cordinate_x = int(round((scene_corners[3][0]+scene_corners[1][0])/2))
		mid_cordinate_y = int(round((scene_corners[3][1]+scene_corners[1][1])/2))
		return mid_cordinate_x, mid_cordinate_y
	except:
		print("not found")


# 特征值匹配
def filter_matches(kp1,kp2,matches,ratio = 0.75):
	mkp1,mkp2 = [],[]
	for m in matches:
		if len(m) == 2 and m[0].distance < m[1].distance*ratio:
			m = m[0]
			mkp1.append(kp1[m.queryIdx])
			mkp2.append(kp2[m.trainIdx])
	p1 = np.float32([kp.pt for kp in mkp1])
	p2 = np.float32([kp.pt for kp in mkp2])
	kp_pairs = zip(mkp1,mkp2)
	#return p1,p2,kp_pairs

'''
queryImgPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".")) + '\\img\\queryImg\\'
sceneFilePath = "D:\\py\\Appium\\game\\img\\sceneImg\\loginui1.png"
# 获取控件坐标
mid_cordinate_x,mid_cordinate_y = getImgCordinate(os.path.join(queryImgPath,'login_button.png'),sceneFilePath,'login')
print(mid_cordinate_x,mid_cordinate_y)
# 点击坐标
#self.driver.tap([(mid_cordinate_x,mid_cordinate_y)])


我们从[0,175)的范围以跨度为25进行循环来取圆的半径，
cv2.circle(canvas, (centerX, centerY), r, white)  #26
然后在第26行通过cv2.circle()来进行画圆，
第一个参数表示在canvas上进行绘画，
第二个参数表示圆心，
第三个参数表示半径，
第四个参数表示颜色。
然后将结果显示出来，并等待按下任意按键。
'''
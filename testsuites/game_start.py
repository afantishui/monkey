import os
import sys
import time
sys.path.append("..")
from Base.imgProcess import *
from Base.Init import *
from Base.monkeyBase import AndroidBaseOperation

'''
# 判断是否存在图片
def exist_pic(queryImgPath,pic,sceneFilePath):
    while 1:
        base.get_screenshot(sceneFilePath)
        # 获取控件坐标
        x,y = getImgCordinate(os.path.join(queryImgPath,pic),sceneFilePath)
        if x is not None:
            return x,y
            print('%s is exist'%pic)
            break
        else:
            print('finding...')

# 匹配图片并点击
def find_click(queryImgPath,pic,sceneFilePath,time):
    x,y = exist_pic(queryImgPath,pic,sceneFilePath)
    base.click(x,y,time)

'''
# 读取配置 配置表、匹配图片、截图
f_config, queryImgPath, sceneFilePath = conf_Init('config.yml')
base = AndroidBaseOperation() # 实例化

base.start_activity(f_config['activity']) # 启动游戏
time.sleep(3)
base.click(100,100,1)  # 跳过动画
base.click(100,100,1)
base.click(100,100,1)
time.sleep(3)
if f_config['loginType'] == 'WX':
    find_click(queryImgPath, f_config['loginButton'], sceneFilePath, 0.5)


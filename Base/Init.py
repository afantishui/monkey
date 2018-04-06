import os
import yaml
import sys
sys.path.append("..")
from Base.imgProcess import *
from Base.Init import *
from Base.monkeyBase import AndroidBaseOperation
base = AndroidBaseOperation()

def conf_Init(config):
    # 读取配置
    filepath = open(r'..\config\%s'%(config), encoding='utf-8')
    f_config = yaml.load(filepath)
    #print(filepath)
    imgpath = os.path.abspath('..')
    #print(imgpath)
    queryImgPath = imgpath + '\\img\\queryImg\\'
    sceneFilePath = imgpath + '\\img\\sceneImg\\auto.png'
    #print(queryImgPath,sceneFilePath)
    return f_config,queryImgPath,sceneFilePath

# 判断是否存在图片
def exist_pic(queryImgPath,pic,sceneFilePath):
    while 1:
        base.get_screenshot(sceneFilePath)
        # 获取控件坐标
        x,y = getImgCordinate(os.path.join(queryImgPath,pic),sceneFilePath)
        if x is not None:
            return x,y
            # print('%s is exist'%pic)
            break
        else:
            print('finding...')

# 匹配图片并点击
def find_click(queryImgPath,pic,sceneFilePath,time):
    x,y = exist_pic(queryImgPath,pic,sceneFilePath)
    base.click(x,y,time)

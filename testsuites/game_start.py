import os
import sys
import time
sys.path.append("..")
from Base.imgProcess import *
from Base.Init import *
from Base.monkeyBase import AndroidBaseOperation

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


''''''
Wrintten by Yao Yuan
''''''

import os
import subprocess

#dir为数据存放路径
dir = os.path.abspath('/home/yaoyuan/Desktop/data/ZSY_cut/ZSY2016_Templates')
print(dir)
datanum = 0
for dirpath, dirname, filenames in os.walk(dir):
    if len(dirpath) == 70:
        datanum += 1
        data = dirpath
        print("data=",data)
        print("datanum=",datanum)
        # sac ppk
        p = subprocess.Popen(['sac'], stdin=subprocess.PIPE)
        s = "wild echo off \n"
        s += "cd %s \n" % (data)
        s += "r * \n"
        s += "rmean;rtr;taper \n" ##
        s += "bp n 4 c 2 8 \n"  ##sac中带通滤波，可根据自己需求更改
        s += "ppk p 3 a m \n"
        s += "wh \n"
        s += "q \n"
        p.communicate(s.encode())



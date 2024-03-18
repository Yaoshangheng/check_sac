''''''
Wrintten by Yao Yuan
''''''

import os
import subprocess
from tqdm import tqdm

# 设置数据存放的基础路径
base_dir = '/mnt/E9D76AE7017538D3/TC_data_one/BLJ'

# 遍历基础路径下的所有子文件夹和文件
for dirpath, _, filenames in os.walk(base_dir):
    # 如果当前路径是文件夹
    if os.path.isdir(dirpath):
        # 遍历当前文件夹下的所有文件
        for filename in filenames:
            # 如果文件是 SAC 文件
            if filename.endswith('.SAC') or filename.endswith('.sac'):
                # 构造文件的完整路径
                sac_file_path = os.path.join(dirpath, filename)

                # 构造 SAC 命令
                sac_commands = "wild echo off\n"
                sac_commands += "r {}\n".format(sac_file_path)  # 读取当前文件
                sac_commands += "rmean;rtr;taper \n"  # 预处理
                sac_commands += "bp n 4 c 2 8 \n"  # 带通滤波
                #sac_commands += "ppk p 3 a m \n"  # 计算 P 波到时
                sac_commands += "ch knetwk TC kstnm BLJ \n"  # 设置台站信息
                sac_commands += "ch stla 25.3575 stlo 98.99231 stel 1706 \n"  # 设置经纬度和海拔信息
                sac_commands += "wh \n"  # 将修改写入文件
                sac_commands += "q \n"  # 退出 SAC

                # 执行 SAC 命令
                p = subprocess.Popen(['sac'], stdin=subprocess.PIPE)
                p.communicate(sac_commands.encode())

                # 显示进度条
                tqdm.write("Processed: {}".format(sac_file_path))

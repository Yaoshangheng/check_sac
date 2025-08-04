"""
Written by Yao Yuan
@KMS-20250804
功能：
- 遍历事件目录（目录名为发震时刻，格式如 20231114104625.64）
- SAC 预处理 + ppk 拾取（ppk p 4 s，P 波写 t0，S 波写 t1）
- 读取 SAC 文件 t0（P 波）、t1（S 波），解释为当天 00:00:00 起的秒数
- 输出格式统一为 2023-11-14T10:46:25.640000Z
- 缺失值用 '#' 占位，长度一致
- 输出文本第一列事件时间也统一为 UTC 时间字符串
"""

import os
import subprocess
from datetime import datetime, timedelta

# ======== 配置路径 ========
base_dir = os.path.abspath('/home/yaoyuan/Desktop/myprogram/cut_sac/cut')
output_file = os.path.join(base_dir, "picked_P_S_abs.txt")
print(f"📁 工作目录: {base_dir}")

# ======== 时间格式和占位符 ========
time_format = "%Y-%m-%dT%H:%M:%S.%fZ"
placeholder = "#" * len(datetime.utcnow().strftime(time_format))

# ======== 写入表头 ========
with open(output_file, "w") as fout:
    fout.write("# event_utc_time\tstation\tT0_P_arrival\tT1_S_arrival\n")

datanum = 0

# ======== 遍历事件目录 ========
for dirpath, _, filenames in os.walk(base_dir):
    basename = os.path.basename(dirpath)

    if basename.replace('.', '').isdigit():
        try:
            # === 解析目录名为本地时间（东八） ===
            parts = basename.split('.')
            local_time = datetime.strptime(parts[0], "%Y%m%d%H%M%S")
            microsec = int(float("0." + parts[1]) * 1e6) if len(parts) > 1 else 0
            local_time = local_time.replace(microsecond=microsec)

            # === 转 UTC 时间作为事件时间 ===
            origin_time = local_time - timedelta(hours=8)
            origin_time_str = origin_time.strftime(time_format)

            # === 事件当日 UTC 00:00:00 时间，用于加 t0/t1 秒数 ===
            day_start_utc = origin_time.replace(hour=0, minute=0, second=0, microsecond=0)

        except Exception as e:
            print(f"⚠️ 时间解析失败: {basename}, 错误: {e}")
            continue

        # === 仅处理 Z 分量 SAC 文件 ===
        z_files = [f for f in filenames if f.endswith(('.BHZ.SAC', '.HHZ.SAC', '.SHZ.SAC'))]
        if not z_files:
            continue

        datanum += 1
        print(f"\n📂 处理事件: {basename} (#{datanum})")

        # ===== SAC 预处理 + 拾取 =====
        sac_script = (
            "wild echo off\n"
            f"cd {dirpath}\n"
            "r *.[BSH]HZ.SAC\n"
            "sort gcarc descend\n"
            "rmean\n"
            "rtr\n"
            "taper\n"
            "bp n 4 c 2 8\n"
            "ppk p 4 s\n"
            "wh\n"
            "q\n"
        )
        p = subprocess.Popen(['sac'], stdin=subprocess.PIPE)
        p.communicate(sac_script.encode())

        # ===== 读取 t0、t1 =====
        for sac_file in z_files:
            sac_path = os.path.join(dirpath, sac_file)
            cmd = f"saclst t0 t1 f {sac_path}"
            try:
                output = subprocess.check_output(cmd, shell=True, universal_newlines=True).strip()
                parts = output.split()
                if len(parts) != 3:
                    print(f"⚠️ saclst 输出异常: {output}")
                    continue

                _, t0_str, t1_str = parts

                # === T0 - P 波 ===
                if t0_str != "-12345":
                    try:
                        t0_abs = (day_start_utc + timedelta(seconds=float(t0_str))).strftime(time_format)
                    except:
                        t0_abs = placeholder
                else:
                    t0_abs = placeholder

                # === T1 - S 波 ===
                if t1_str != "-12345":
                    try:
                        t1_abs = (day_start_utc + timedelta(seconds=float(t1_str))).strftime(time_format)
                    except:
                        t1_abs = placeholder
                else:
                    t1_abs = placeholder

                # === 提取台站名 ===
                station = sac_file.split('.')[1]

                # === 写入结果 ===
                with open(output_file, "a") as fout:
                    fout.write(f"{origin_time_str}\t{station}\t{t0_abs}\t{t1_abs}\n")

            except subprocess.CalledProcessError as e:
                print(f"⚠️ saclst 失败: {sac_path}, {e}")

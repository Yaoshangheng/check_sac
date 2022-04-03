import os
import shutil
project_dir = r'/home/yaoyuan/Desktop/data/ZSY_cut/ZSY2017_Templates'
file_name = '/home/yaoyuan/Desktop/myprogram/check_sac/example_pal_hyp.pha'
output_dir = r'/home/yaoyuan/Desktop/data/XC' #复制出的目录路径
def main(copy_dir_count = 1):
    count = 0
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok = True)
    f = open(os.path.join(project_dir, file_name), 'r')
    for line in f.readlines():
        from_dir = line.split(',')[0]
        if not from_dir.replace('.', '').isdigit() or not os.path.exists(os.path.join(project_dir, from_dir)):
            continue
        #复制目录
        os.makedirs(os.path.join(output_dir, from_dir), exist_ok = True)
        to_dir = os.path.join(output_dir, from_dir)
        from_dir = os.path.join(project_dir, from_dir)
        print('copy {} to {}'.format(os.path.abspath(from_dir), os.path.abspath(to_dir)))
        for file in os.listdir(from_dir):
            shutil.copy(os.path.join(from_dir, file), os.path.join(to_dir, file))
        #复制指定个数目录后结束
        count += 1
        if copy_dir_count > 0 and count >= copy_dir_count:
            break;
    f.close()
main(copy_dir_count = -1) #copy_dir_count指定复制目录个数

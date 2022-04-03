import os
value_range = [0, 30] #设置筛选范围
ctlg_in = './example_pal_hyp.ctlg' #输入文件
pha_in = r'example_pal_hyp.pha'
ctlg_out = './ctlg.txt' #输出文件
pha_out = r'./pha.txt'
def main(in_name, out_name, v_range):
    fin = open(in_name, 'r')
    fout = open(out_name, 'w')
    i = 0
    lines = fin.readlines()
    while i < len(lines):
        values = lines[i].split(',')
        if values[0].replace('.', '').isdigit():
            # 满足条件时保存到文件
            col4_value = eval(values[3])
            if col4_value >= v_range[0] and col4_value <= v_range[1]:
                fout.write(lines[i])
                i += 1
                while i < len(lines) and not lines[i].split(',')[0].replace('.', '').isdigit():
                    fout.write(lines[i])
                    i += 1
            else:
                i += 1
        else:
            i += 1
    fin.close()
    print('save to:', os.path.abspath(out_name))
main(ctlg_in, ctlg_out, value_range)
main(pha_in, pha_out, value_range)    


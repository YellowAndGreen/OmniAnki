import re
def extract():
    with open("C://Users//60234//Desktop/kCY1.gid", 'r', encoding="utf-8") as f:
        read_data = f.readlines()
    list_name_and_unit = [re.findall(r"'.*?'", line)[0][1:-1] for line in read_data if re.findall(r"'.*?'", line)]
    val_list_line = [re.findall(r"0.[0-9]{8}E[+|-][0-9]{3}", i) for i in read_data if re.findall(r"0.[0-9]{8}E[+|-][0-9]{3}", i)!=[]]
    len_list_name = int(len(list_name_and_unit) / 2)
    val_list = list(zip(*val_list_line))
    data = dict([(list_name_and_unit[i], {'unit': list_name_and_unit[len_list_name:][i], 'value': val_list[i]}) for i in range(0, len_list_name)])
    return data

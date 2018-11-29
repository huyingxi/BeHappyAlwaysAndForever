import codecs,re
from collections import defaultdict
#生成标准格式的词表,仅使用一次
#普通话词语<>川渝话词语
file1 = 'raw_data_1.txt'
file2 = 'raw_data_2.txt'

putonghua_dict = defaultdict(list)
chuanyu_dict = defaultdict(list)

def handlefile1(filename):
    lines = codecs.open(filename,'r','utf8').readlines()
    lines = [i.replace('\n','').strip()[0:-1] for i in lines]
    lines_tmp = []
    for idx,line in enumerate(lines):
        tmp = line.split('（')
        if len(tmp)<2:
            tmp = line.split('(')
            if len(tmp)<2:
                print(idx,tmp)
                break
        lines_tmp.append(tmp)
    lines = lines_tmp[:]
    pt = [re.split('/|，|、| ',i[0]) for i in lines]
    cy = [re.split('/|，|、| ',i[1]) for i in lines]
    print(pt[0:10])
    print(cy[0:10])
    for idx,pti in enumerate(pt):
        for ptii in pti:
            putonghua_dict[ptii].extend(cy[idx])
    for idx,cyi in enumerate(cy):
        for cyii in cyi:
            chuanyu_dict[cyii].extend(pt[idx])
#print(putonghua_dict)
#print(chuanyu_dict)

def handlefile2(filename):
    lines = codecs.open(filename,'r','utf8').readlines()
    lines = [i.replace('\n','').replace('；','').replace('：','').strip() for i in lines]
    #lines = [i.replace(' ','/') for i in lines]
    lines_tmp = []
    for idx,line in enumerate(lines):
        tmp = line.split('——')
        if len(tmp)<2:
            tmp = line.split('-')
            if len(tmp)<2:
                print(idx,tmp)
                break
        lines_tmp.append(tmp)
    lines = lines_tmp[:]
    pt = [re.split('/|，|、| ',i[0]) for i in lines]
    cy = [re.split('/|，|、| ',i[1]) for i in lines]
    for idx,pti in enumerate(pt):
        for ptii in pti:
            putonghua_dict[ptii].extend(cy[idx])
    for idx,cyi in enumerate(cy):
        for cyii in cyi:
            chuanyu_dict[cyii].extend(pt[idx])

handlefile1(file1)
handlefile2(file2)
for key in putonghua_dict:
    putonghua_dict[key] = list(set(putonghua_dict[key]))
for key in chuanyu_dict:
    chuanyu_dict[key] = list(set(chuanyu_dict[key]))

outfile1 = codecs.open('c2p.happy','w','utf8')
outfile2 = codecs.open('p2c.happy','w','utf8')
for key in putonghua_dict:
    outfile1.write(key+'<>'+','.join(putonghua_dict[key])+'\n')
for key in chuanyu_dict:
    outfile2.write(key+'<>'+','.join(chuanyu_dict[key])+'\n')

def read_data(filename):
    lines = codecs.open(filename,'r','utf8').readlines()
    lines = [i.replace('\n','').strip() for i in lines]
    lines = [i.split('<>') for i in lines]
    dict_out = dict()
    for idx,line in enumerate(lines):
        key = line[0]
        tmp = line[1].split(',')
        dict_out[key] = tmp[:]
    return dict_out
'''
p2c = read_data('p2c.happy')
c2p = read_data('c2p.happy')
print(p2c)
''' 
import SocialPsy.Analyse.SSA as SSA
import os
import matplotlib.pyplot as plt

import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random

def load_variavle(filename):
    f=open(filename,'rb')
    r=pickle.load(f)
    f.close()
    return r

def read_file(filename):
    with  open(filename, 'r',encoding='utf-8')as f:
        text=[[],[],[]]
        while 1:
            line = f.readline()
            if not line:
                break
            if "点赞数：" in line:
                text[1].append(int(line[4:line.index('\t')]))
            elif "时间：" in line:
                num=int(line[3:line.index('.')])
                num+=int(line[line.index('.')+1:line.index('\t')])/30
                text[0].append(num)
            elif "评论内容：" in line:
                tmp=line[5:]
                while 1:
                    line =f.readline()
                    if not line:
                        return text
                    if "---" in line:
                        break
                    tmp+=line[0:]
                text[2].append(tmp)
    return text

result = []
def get_all(cwd):
    get_dir = os.listdir(cwd)
    for i in get_dir:
        sub_dir = os.path.join(cwd, i)
        if os.path.isdir(sub_dir):
            get_all(sub_dir)
        else:
            result.append(sub_dir)

months=[[],[],[],[],[],[]]
month_score=[0,0,0,0,0,0]
if __name__ == '__main__':
    months = load_variavle('Temp/months.txt')

    ped = [[], []]
    for i in range(6):
        num=0
        for data in months[i]:
            if (data < 300 and data > -100):
                num+=data

        ped[0].append(i+1)
        ped[1].append(num/len(months[i]))

    print('Processing........')
    path=r'../Data/BComments'
    for i in range(50):
        result.append(r'../Data/BComments/BiliComments'+str(i+1)+'.txt')
    #get_all(path)

    x2=[1,2,3,4,5,6]
    y2=[-13,25,80,29,35,41]
    x=[1,2,3,4,5,6]
    y=[0,0,0,0,0,0]
    tmpx=[]
    tmpy=[]
    for filename in result:
        BComments = read_file(filename)

        allNice=0
        for item in BComments[1]:
            allNice+=item

        sentences = BComments[2]
        score_sum = 0
        for sent in range(len(sentences)):
            score = SSA.single_sentiment_score(sentences[sent])[0]
            score_sum += score*BComments[1][sent]/allNice

        tmpx.append(BComments[0][0])
        tmpy.append(score_sum)
        print(filename[18:]+'    succeed.......')

    num=[0,0,0,0,0,0]
    for i in range(len(tmpx)):
        if tmpx[i]<2:
            y[0]+=tmpy[i]
            num[0]+=1
        elif tmpx[i]<3:
            y[1]+=tmpy[i]
            num[1]+=1
        elif tmpx[i]<4:
            y[2]+=tmpy[i]
            num[2]+=1
        elif tmpx[i]<5:
            y[3]+=tmpy[i]
            num[3]+=1
        elif tmpx[i]<6:
            y[4]+=tmpy[i]
            num[4]+=1
        else:
            y[5]+=tmpy[i]
            num[5]+=1
    for i in range(6):
        y[i]=y[i]/num[i]

    plt.figure(figsize=(10, 5))
    plt.ylabel('Value of emtion', size=20, fontweight='bold')
    plt.title("Social Psychologic on Different platform", size=20, y=-0.2, fontweight='bold')
    Bi, = plt.plot(x, y, color='#F66A6A', linewidth=4.0, linestyle='-', marker="o", markersize=10)
    Ped,= plt.plot(ped[0], ped[1], color='#7C6781', linewidth=4.0, linestyle='-', marker="s", markersize=10)
    Weibo,=plt.plot(x2,y2,'#74C6C7',linewidth=4.0,linestyle='-',marker = "v",markersize=10)
    plt.legend(handles=[Bi,Ped,Weibo],
               labels=['Bilibili','PeopleDaily','Weibo'],
               prop={'size': 17})

    plt.show()
    plt.savefig('platform.pdf', format="pdf", bbox_inches='tight')
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

if __name__ == '__main__':
    months = load_variavle('Temp/months.txt')
    month_score = load_variavle('Temp/month_score.txt')

    colors = []
    sandian=[[],[]]
    for i in range(6):
        for data in months[i]:
            if(data<2000 and data>-500):
                sandian[0].append(i+random.randint(1,29)/30)
                sandian[1].append(data)

    for x, y in zip(sandian[0], sandian[1]):
        if y>1000:
            colors.append('red')
        elif x < 1:
            colors.append('blue')
        elif x<2:
            colors.append('purple')
        elif x<3:
            colors.append('green')
        elif x<4:
            colors.append('pink')
        elif x<5:
            colors.append('black')
        elif x<6:
            colors.append('yellow')

    plt.figure(figsize=(10,5))
    plt.ylabel("Value of emotion",size=20, fontweight='bold')
    plt.title("Social Psychologic From PeopleDaily", size=20, y=-0.2, fontweight='bold')

    plt.plot([1] * 2500, list(range(-500, 2000)), 'c--')  # 添加纵向分隔线
    plt.plot([2] * 2500, list(range(-500, 2000)), 'c--')  # 添加纵向分隔线
    plt.plot([3] * 2500, list(range(-500, 2000)), 'c--')  # 添加纵向分隔线
    plt.plot([4] * 2500, list(range(-500, 2000)), 'c--')  # 添加纵向分隔线
    plt.plot([5] * 2500, list(range(-500, 2000)), 'c--')  # 添加纵向分隔线

    plt.plot(list(range(0, 7)),[-150]*7,  'c--')
    plt.plot(list(range(0, 7)), [400] * 7, 'c--')
    plt.plot(list(range(0, 7)), [0] * 7, 'c--',linewidth=5)

    plt.scatter(sandian[0],sandian[1],c=colors)
    plt.savefig('./result/ResPD.pdf', format="pdf", bbox_inches='tight')
    plt.show()
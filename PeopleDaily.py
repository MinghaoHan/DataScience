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
            if data<2000:
                num+=data

        ped[0].append(i+1)
        ped[1].append(num/len(months[i]))

    plt.figure(figsize=(10, 5))
    plt.ylabel('Value of emtion', size=20, fontweight='bold')
    plt.title("Social Psychologic Jan~June(PeopleDaily)", size=20, y=-0.2, fontweight='bold')
    Ped,= plt.plot(ped[0], ped[1], color='#7C6781', linewidth=4.0, linestyle='-', marker="s", markersize=10)
    plt.legend(handles=[Ped],
               labels=['PeopleDaily'],
               prop={'size': 17})

    plt.show()
    plt.savefig('1~6.pdf', format="pdf", bbox_inches='tight')
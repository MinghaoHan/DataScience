import SocialPsy.Analyse.SSA as SSA
import os
import matplotlib.pyplot as plt

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
    print('Processing........')
    path=r'../Data/BComments'
    for i in range(50):
        result.append(r'../Data/BComments/BiliComments'+str(i+1)+'.txt')
    #get_all(path)

    x=[]
    y=[]
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

        x.append(BComments[0][0])
        y.append(score_sum)
        print(filename[18:]+'    succeed.......')

    plt.figure(figsize=(10, 5))
    plt.ylabel('Value of emtion', size=20, fontweight='bold')
    plt.title("Social Psychologic From Bilibili", size=20, y=-0.2, fontweight='bold')
    Bi,=plt.plot(x, y, color='#F66A6A', linewidth=4.0, linestyle='-', marker="o", markersize=10)
    plt.legend(handles=[Bi,],
               labels=['Bilibili'],
               prop={'size': 17})

    plt.show()
    plt.tight_layout()
    plt.savefig('./result/Bili.png', format="png", bbox_inches='tight')
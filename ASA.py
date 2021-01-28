import SocialPsy.Analyse.SSA as SSA
import os
import pickle
def save_variable(v,filename):
    f=open(filename,'wb')
    pickle.dump(v,f)
    f.close()
    return filename

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
    places = {'北京': 0, '天津': 0, '上海': 0, '重庆': 0, '河北': 0, '山西': 0, '香港': 0, '澳门': 0, '台湾': 0, '河北': 0, '山西': 0,
              '辽宁': 0, '吉林': 0, '黑龙江': 0, '江苏': 0, '浙江': 0, '安徽': 0, '福建': 0, '江西': 0, '山东': 0, '河南': 0, '湖北': 0,
              '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0, '陕西': 0, '甘肃': 0, '青海': 0, '内蒙古': 0, '广西': 0,
              '西藏': 0, '宁夏': 0, '新疆': 0}
    print('Processing........')
    path=r'../Data/data/PeopleDaily'
    #result.append('../Data/data/PeopleDaily/20200109/20200109-17-04.txt')
    get_all(path)

    for filename in result:
        sentences = SSA.read_file(filename)
        res = SSA.run_score(sentences)
        scores = res[0]
        for key in res[1].keys():
            places[key] += res[1][key]

        scores_sum=0    #总分
        for score in scores:
            scores_sum+=score[0]
        mon = int(filename[-14:-12])
        ariticle = [scores[0][1],mon,scores_sum]
        months[mon-1].append(scores_sum)
        month_score[mon-1]+=scores_sum

        print(filename[13:]+'    succeed.......')

    filename = save_variable(months, 'Temp/months.txt')
    filename = save_variable(month_score, 'Temp/month_score.txt')
    filename = save_variable(places, 'Temp/places.txt')
    print(filename)




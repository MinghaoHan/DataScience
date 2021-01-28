import SocialPsy.Analyse.SSA as SSA
import os
import SocialPsy.Analyse.Map_of_China.Map_of_China as Map
import pandas as pd

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

if __name__ == '__main__':


    M = Map.Get_Map()
    M.Get_country()  # 获取首页全国各省的地图数据

    places =[{},{},{},{},{},{}]
    places[0] = places[1] = places[2] = places[3] = places[4] = places[5] = \
        {'北京': 0, '天津': 0, '上海': 0, '重庆': 0, '河北': 0, '山西': 0, '香港': 0, '澳门': 0, '台湾': 0, '河北': 0, '山西': 0,
        '辽宁': 0, '吉林': 0, '黑龙江': 0, '江苏': 0, '浙江': 0, '安徽': 0, '福建': 0, '江西': 0, '山东': 0, '河南': 0, '湖北': 0,
        '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0, '陕西': 0, '甘肃': 0, '青海': 0, '内蒙古': 0, '广西': 0,
        '西藏': 0, '宁夏': 0, '新疆': 0}

    places = load_variavle('Temp/places.txt')

    for i in range(6):
        pd.DataFrame(places[i],index=[0]).to_csv('result/month_'+str(i)+'.csv')
        D = Map.Draw_Map()  # 创建绘制地图对象
        src = 'result/month_'+str(i)+'.csv'
        D.Show_data(src, FC='OrRd', title='2020年'+str(i)+'月份全国各省份心态情绪值', arg={'sea': True})  # 按数据的绝对大小显示
        D.Show_data(src, by_val=False, arg={'default_color': [0.6, 0.6, 0.6]})  # 按数据的相对大小(排名)显示
        print(str(i+1)+'月份OK')



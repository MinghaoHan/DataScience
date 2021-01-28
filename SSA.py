import jieba
import jieba.posseg as psg
import re
import numpy as np

def read_file(filename):
    with  open(filename, 'r',encoding='utf-8')as f:
        text = f.read()
        text = text.split('\n')
    return text

def write_data(filename,data):
    with open(filename,'a',encoding='utf-8')as f:
        f.write(str(data))

#分句
def cut_sentence(paragraph):
    sentences = re.split('(。|！|\!|\.|？|\?|\n)',paragraph)
    sentence_list = [ w for w in sentences]
    return sentence_list

#分词
def tokenize(sentence):
    words = jieba.lcut(sentence)
    return words

#词性标注
def postagger(sentence):
    postags = psg.cut(sentence)
    return postags

# 分词，词性标注，词和词性构成一个元组
def intergrad_word(words,postags):
    pos_list = zip(words,postags)
    pos_list = [ w for w in pos_list]
    return pos_list

#去停用词函数
def del_stopwords(words):
    stopwords = read_file(r"tools/stopwords-master/hit_stopwords.txt")
    new_words = []
    for word in words:
        if word not in stopwords:
            new_words.append(word)
    return new_words

# 获取六种权值的词，根据要求返回list，这个函数是为了配合Django的views下的函数使用
def weighted_value(request):
    result_dict = []
    if request == "one":
        result_dict = read_file(r"tools/sentiment/most.txt")
    elif request == "two":
        result_dict = read_file(r"tools/sentiment/very.txt")
    elif request == "three":
        result_dict = read_file(r"tools/sentiment/more.txt")
    elif request == "four":
        result_dict = read_file(r"tools/sentiment/ish.txt")
    elif request == "five":
        result_dict = read_file(r"tools/sentiment/insufficiently.txt")
    elif request == "six":
        result_dict = read_file(r"tools/sentiment/inverse.txt")
    elif request == 'pos':
        result_dict = read_file(r"tools/sentiment/positiveWords.txt")
    elif request == 'neg':
        result_dict = read_file(r"tools/sentiment/negativeWords.txt")
    else:
        pass
    return result_dict

print("reading sentiment dict .......")
#读取情感词典
posdict = weighted_value('pos')
negdict = weighted_value('neg')
# 读取程度副词词典
# 权值为2
mostdict = weighted_value('one')
# 权值为1.75
verydict = weighted_value('two')
# 权值为1.50
moredict = weighted_value('three')
# 权值为1.25
ishdict = weighted_value('four')
# 权值为0.25
insufficientdict = weighted_value('five')
# 权值为-1
inversedict = weighted_value('six')

#程度副词处理，对不同的程度副词给予不同的权重
def match_adverb(word,sentiment_value):
    #最高级权重为
    if word in mostdict:
        sentiment_value *= 8
    #比较级权重
    elif word in verydict:
        sentiment_value *= 6
    #比较级权重
    elif word in moredict:
        sentiment_value *= 4
    #轻微程度词权重
    elif word in ishdict:
        sentiment_value *= 2
    #相对程度词权重
    elif word in insufficientdict:
        sentiment_value *= 0.5
    #否定词权重
    elif word in inversedict:
        sentiment_value *= -1
    else:
        sentiment_value *= 1
    return sentiment_value

#对一条微博打分
def single_sentiment_score(text_sent):
    places={'北京':0,'天津':0,'上海':0,'重庆':0,'河北':0,'山西':0,'香港':0,'澳门':0,'台湾':0,'河北':0,'山西':0,
            '辽宁':0,'吉林':0,'黑龙江':0,'江苏':0,'浙江':0,'安徽':0,'福建':0,'江西':0,'山东':0,'河南':0,'湖北':0,'湖南':0,
            '广东':0,'海南':0,'四川':0,'贵州':0,'云南':0,'陕西':0,'甘肃':0,'青海':0,'内蒙古':0,'广西':0,'西藏':0,'宁夏':0,'新疆':0}

    sentiment_scores = []
    sentences = cut_sentence(text_sent)
    for sent in sentences:
        place=[]
        #分词
        words = tokenize(sent)
        #删除停用词
        seg_words = del_stopwords(words)
        #i，s 记录情感词和程度词出现的位置
        i = 0
        s = 0
        poscount = 0 #记录积极情感词数目
        negcount = 0 #记录消极情感词数目
        #逐个查找情感词
        for word in seg_words:
            if '省' in word:
                word=word[:-1]
            if word in places.keys():
                if word not in place:
                    place.append(word)
                continue
            #如果为积极词
            if word in posdict:
                poscount += 1  #情感词数目加1
            #在情感词前面寻找程度副词
                for w in seg_words[s:i]:
                    poscount = match_adverb(w,poscount)
                s = i+1 #记录情感词位置
            # 如果是消极情感词
            elif word in negdict:
                negcount +=1
                for w in seg_words[s:i]:
                    negcount = match_adverb(w,negcount)
                s = i+1
            #如果结尾为感叹号或者问号，表示句子结束，并且倒序查找感叹号前的情感词，权重+4
            elif word =='!' or  word =='！' or word =='?' or word == '？':
                for w2 in seg_words[::-1]:
                    #如果为积极词，poscount+2
                    if w2 in posdict:
                        poscount += 4
                        break
                    #如果是消极词，negcount+2
                    elif w2 in negdict:
                        negcount += 4
                        break
            i += 1 #定位情感词的位置
        #计算情感值
        sentiment_score = poscount - negcount
        sentiment_scores.append(sentiment_score)
        for i in place:
            places[i]+=0.2
            places[i]+=sentiment_score

    sentiment_sum = 0
    for s in sentiment_scores:
        sentiment_sum +=s
    return sentiment_sum,places

# 分析test_data.txt 中的每一句，返回一个列表，列表中元素为（分值，句子）元组
def run_score(contents):
    scores_list = []
    places = {'北京': 0, '天津': 0, '上海': 0, '重庆': 0,'河北': 0, '山西': 0, '香港': 0, '澳门': 0, '台湾': 0, '河北': 0, '山西': 0,
              '辽宁': 0, '吉林': 0, '黑龙江': 0, '江苏': 0, '浙江': 0, '安徽': 0, '福建': 0, '江西': 0, '山东': 0, '河南': 0, '湖北': 0,
              '湖南': 0, '广东': 0, '海南': 0, '四川': 0, '贵州': 0, '云南': 0, '陕西': 0, '甘肃': 0, '青海': 0, '内蒙古': 0, '广西': 0,
              '西藏': 0, '宁夏': 0, '新疆': 0}

    for content in contents:
        if content !='':
            tmp = single_sentiment_score(content)  # 对每句话调用函数求得打分
            score = tmp[0]
            for key in tmp[1].keys():
                places[key]+=tmp[1][key]
            scores_list.append((score, content)) # 形成（分数，句子）元组
    return scores_list,places

#主程序
if __name__ == '__main__':
    print('Processing........')

    sentences = read_file(r'../Data/data/PeopleDaily/20200121/20200121-01-01.txt')
    res = run_score(sentences)
    scores = res[0]
    places = res[1]
    print(places)

    al_sentiment = []
    for score in scores:
        print('情感分值：',score[0])
        if score[0] < 0:
            print('情感倾向：消极')
            s = '消极'
        elif score[0] == 0:
            print('情感倾向：中性')
            s = '中性'
        else:
            print('情感倾向：积极')
            s = '积极'
        al_sentiment.append(s)
        print('情感分析文本：',score[1])

    i = 0
    filename = r'result/result_data.txt'
    for score in scores:
        write_data(filename, '情感分析文本：{}'.format(str(score[1]))+'\n') #写入情感分析文本
        write_data(filename,'情感分值：{}'.format(str(score[0]))+'\n') #写入情感分值
        write_data(filename, '机器情感标注：{}'.format(str(al_sentiment[i]))+'\n') #写入机器情感标注
        write_data(filename,'\n')
        i +=1
    print('succeed.......')
import re

from .models import Dict


# import pandas as pd
# from readmdict import MDX


# def mdx_to_database():
#     filename = "flashcards/static/dict/剑桥高阶.mdx"
#     headwords = [*MDX(filename)]  # 单词名列表
#     items = [*MDX(filename).items()]  # 释义html源码列表
#     coca = pd.read_excel('flashcards/static/dict/COCA.xlsx', sheet_name='Sheet1')
#     coca_dict = {}
#     # 将信息一次性保存入字典，后面不需重复遍历
#     for row in coca.iterrows():
#         coca_dict[row[1][' word'].strip()] = row[1]['RANK #']
#     for i in range(len(headwords)):
#         wordindex = headwords.index(headwords[i])
#         word, html = items[wordindex]
#         word, html_result = word.decode(), html.decode()
#         dic = Dict(headword=word, item=html_result)
#         # 若存在coca字典中，则加入
#         if word.strip() in coca_dict:
#             dic.coca = coca_dict[word.strip()]
#         dic.save()


def find_example_from_database(queryword):
    # 查词，返回单词和html文件
    # 只查单词，使用正则过滤
    queryword = re.findall(r"[a-zA-Z]+", queryword)[0]
    html_result = ''
    dict_query = Dict.objects.filter(headword=queryword)
    if len(dict_query) == 0:
        dict_query = Dict.objects.filter(headword=queryword.lower())
        if len(dict_query) == 0:
            return [], []
    # 过滤出例句和翻译
    raw_examples = re.findall(r"<font color=#008080>.*?</font></div>", dict_query[0].item)
    examples, translations = [], []
    for raw_example in raw_examples:
        example_and_tran = re.sub(r"(<.*?>|</.*?>)", "", raw_example)
        # 分割英文和中文，以中文第一个字切割
        first_chinese = re.search(r"[\u4e00-\u9fa5]", example_and_tran).span()[0]
        example = example_and_tran[0:first_chinese]
        translation = example_and_tran[first_chinese:]
        examples.append(example)
        translations.append(translation)
        # print(example+translation)
    meanings = re.findall(r'<font style="color:navy;margin-left:12pt;" ?>(.*?)</font>', dict_query[0].item)
    return examples, translations, meanings


# def import_to_db():
#     data = pd.read_excel('C:\\Users\\Administrator\\Desktop\\Anki\\utils\\资源\\ank2.xlsx'
#                          '', sheet_name='Sheet1', header=0)
#
#     for i in range(data.shape[0]):
#         val_list = re.split(r"[ ]{3,}", data['答案'][i])
#
#         # 判断是否只有extra
#         if len(val_list) == 4:
#             extra = val_list[-1]
#             example = ""
#             translation = ""
#         else:
#             try:
#                 example = val_list[3]
#                 translation = val_list[4]
#                 try:
#                     extra = val_list[5]
#                 except IndexError:
#                     extra = ""
#             except IndexError:
#                 example = ""
#                 translation = ""
#                 extra = ""
#         # 解决question的不换行问题
#         example_temp = re.sub(r'(?P<attr>v.n.|n.|adj.|adv.|v.)', '\n\g<attr>', example)
#         example = example_temp if example_temp[0:1] != '\n' else example_temp[1:]
#
#         card = Card(group=val_list[0],
#                     question=re.sub(r"(<.*?>|\[.*?\]|&nbsp;)", "", re.sub(r"<div>", "\n", val_list[1])),
#                     answer=val_list[2].replace('；', '，'),
#                     example=example,
#                     translation=translation,
#                     extra=extra,
#                     due=data['到期'][i],
#                     forget_num=int(data['遗忘次数'][i]),
#                     review_num=int(data['复习'][i]),
#                     ratio=int(data['简易度'][i][0:-1]),
#
#                     )
#         card.save()
#     # 判断是否有标签，在上面执行后使用
#     # 同时初始化interval
#     i = 0
#     now = datetime.datetime.now()
#     for card in Card.objects.all():
#         card.interval = (card.due - now).days
#         if type(data['标签'][i]) == str:
#             for tag in re.split(r"[ ]{2,}", data['标签'][i]):
#                 if tag != ' ':
#                     card.tags.add(tag)
#         card.save()
#         i += 1


_MAPPING = (
    u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四', u'十五', u'十六', u'十七',
    u'十八', u'十九')
_P0 = (u'', u'十', u'百', u'千',)
_S4 = 10 ** 4


def to_chinese(num):
    assert (0 <= num < _S4)
    if num < 20:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
        return result[::-1]

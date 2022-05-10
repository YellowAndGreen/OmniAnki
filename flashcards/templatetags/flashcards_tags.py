from django import template
import re

register = template.Library()


@register.filter(name='youdao')
def youdao(text):
    # django默认不使用filter传入的HTML，需要标记为safe才能使用

    # 网址中的空格不会识别，以%20作为空格转义符
    return 'http://dict.youdao.com/dictvoice?audio=' + text.replace(" ", "%20")


@register.filter(name='pureword')
def pureword(text):
    # 如果有sound标签则进行处理，否则不处理（仅用safe来处理html标签）
    voc1 = re.search('sound', text)
    if voc1:  # 只有在匹配有结果的时候才将结果放入voc_list
        voc2list = re.split("\<\!\-\-anki\-\-\>|;|\<b\>|\<div\>|\[sound\:|\</b\>|&nbsp|\(|\)", text)
        for voc2 in voc2list:
            if voc2 != "" and voc2 != " ":
                return voc2
            else:
                return text
    else:
        return text


@register.filter(name='strftime')
def strftime(text):
    return text.strftime("%Y-%m-%d")




import requests
import re

# 全局变量
inbox = []
word = ""
# 短语inbox
phinbox = []
temp = []


def getResponse(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        t = r.text
        return t
    except:
        print("请求失败")


def searchtag(html):
    ilist = re.findall(r"<a class=\"search-js\" href=\".*?#keyfrom=dict.basic.wordgroup\">.*?</span>", html)
    return ilist


def searchre(html):
    refind = re.findall(r"<span class=\"text\">.*</span>", html)
    return refind


def searchsynonym(html):
    words = []
    refindn = re.search(r"n\.[\s|\u4e00-\u9fa5|，|；|\[|\]]*?<\/li>", html)
    if refindn:
        words.append(refindn.group(0))
    else:
        words.append("none")
    refindvt = re.search(r"vt\.[\s|\u4e00-\u9fa5|，|；|\[|\]]*?<\/li>", html)
    if refindvt:
        words.append(refindvt.group(0))
    else:
        words.append("none")
    refindvi = re.search(r"vi\.[\s|\u4e00-\u9fa5|，|；|\[|\]]*?<\/li>", html)
    if refindvi:
        words.append(refindvi.group(0))
    else:
        words.append("none")
    refindadj = re.search(r"adj\.[\s|\u4e00-\u9fa5|，|；|\[|\]]*?<\/li>", html)
    if refindadj:
        words.append(refindadj.group(0))
    else:
        words.append("none")
    return words


def formurlforsynonym(word):
    url = "http://www.thesaurus.com/browse/" + word
    return url

# 新-同义词
def find_synonym(word):
    url1 = formurlforsynonym(word)
    html1 = getResponse(url1)
    words = re.findall(r'href="/browse/.*?"', html1)
    words = list(map(lambda word: word.split("/browse/")[1].split('"')[0], words))
    return words[0:10]


def formurlforphrase(word):
    url = "http://dict.youdao.com/w/" + word + "/#keyfrom=dict2.top"
    return url


# 这是一个判断是查字典还是制卡的函数
def judge(word):
    if word[0:6] == "output":
        output()
        return False
    return True


# 一个输出为utf-8编码的txt文件
def output():
    global inbox  # 设置为全局变量
    typpe = "词汇-第四组|{}|{}"  # 以|作为分隔符

    with open(r"C:\Users\60234\Desktop\qwe.txt", "a", encoding="utf-8") as f:
        f.write(typpe.format(word, inbox[0]))


# 搜索的函数
def search(word):
    # 要先声明是全局变量
    global inbox
    global phinbox
    url1 = formurlforsynonym(word)
    url2 = formurlforphrase(word)
    html1 = getResponse(url1)
    html2 = getResponse(url2)
    words = searchre(html1)
    phrases = searchtag(html2)
    i = 0
    tplt = "{0:10}\t{1:15}\t{2:15}\t{3:15}\t{4:15}"
    print("Here are some synonyms !\n")
    for w in words:
        i = i + 1
        h1 = w.split(">")
        h2 = h1[1].split("<")
        htmlforsyn = getResponse(formurlforphrase(h2[0]))
        wordss1 = searchsynonym(htmlforsyn)
        wordss2 = []
        for wordsss in wordss1:
            wordsplit = wordsss.split("<")
            wordss2.append(wordsplit[0])
        print(tplt.format(h2[0], wordss2[0], wordss2[1], wordss2[2], wordss2[3]))
        if (i >= 12):
            break
    j = 0
    print("\nHere are phrases !\n")
    for n in phrases:
        j = j + 1
        h1 = n.split("wordgroup\">")
        h2 = h1[1].split("</a>")
        print(h2[0])
        phinbox.append(h2[0])
        if (j >= 10):
            inbox.append(phinbox)
            phinbox = []
            break
    print("\n")


# 主函数
def anki():
    global word
    word = input("please enter a word | command or push something：")
    find_synonym(word)


# anki()

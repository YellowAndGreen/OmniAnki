import datetime
import json
import logging
import os

import newspaper
from django.contrib.auth.models import User

from reader.models import Article
from .models import Card, WordList


# 更新到期卡片的due
def update_due():
    logger = logging.getLogger(__name__)
    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59)
    count = 0
    for card in Card.objects.all():
        # 若时间仍在今天或以前，则更新至明天
        if card.due <= deadline:
            card.due = datetime.datetime(year=now.year, month=now.month, day=now.day + 1)
            card.interval = -1
            card.save()
            count += 1
    logger.error(f"{now}:已更新{count}个到期单词")


# 生成新的每日列表
def update_due_list():
    logger = logging.getLogger(__name__)
    # 首先删除之前的due表
    WordList.objects.filter(name="due").delete()
    now = datetime.datetime.now()
    deadline = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59)
    cards = filter(lambda card: card.due <= deadline, Card.objects.all())
    id_list = [{'id': card.id} for card in cards]
    wordlist = WordList(owner=User.objects.all()[0], name="due", wordlist=json.dumps(id_list)
                        , len_list=len(id_list))
    wordlist.save()
    logger.error(f"{now}:新列表已生成！共有{len(id_list)}张卡片")


# 自动备份数据库
def backup_db():
    command = 'python manage.py dumpdata > db.json'
    status = os.system(command)
    if status != 0:
        raise Exception('执行系统命令失败, command=%s, status=%s' % (command, status))


def update_article():
    urls = ['https://www.cnn.com/', 'https://thenextweb.com/', 'https://www.cnbc.com/', 'https://www.wired.com/']
    # if 'url' in request.POST and request.POST['url'][0:4] == 'http':
    #     urls = [request.POST['url']]
    count_num = 0
    # 删除所有新闻，更新100篇新闻
    Article.objects.all().delete()
    # 循环urls列表，直到100篇新闻
    for url in urls:
        cnn = newspaper.build(urls[0], languange='en', memoize_articles=False)
        with open('./log.txt', 'a') as f:
            f.write(f"开始更新文章,来自{url}，共有{len(cnn.articles)}篇文章\n")
        for article in cnn.articles:
            try:
                article.download()
                article.parse()
            except Exception as e:
                with open('./log.txt', 'a') as f:
                    f.write(f'{e}\n')
                continue
            if article.text == "" or article.title == "" or len(article.text.strip()) < 2000:
                with open('./log.txt', 'a') as f:
                    f.write(f'太短！只有{len(article.text)}字符\n')
                continue
            else:
                count_num += 1
                with open('./log.txt', 'a') as f:
                    f.write(f'成功导入第{count_num}/100个，有{len(article.text)}个字符\n')
                art_model = Article(title=article.title, content=article.text)
                if article.top_image != '':
                    art_model.top_image_url = article.top_image
                art_model.save()

                if count_num == 100:
                    with open('./log.txt', 'a') as f:
                        f.write('全部导入!\n')
                    break
        if count_num == 100:
            break



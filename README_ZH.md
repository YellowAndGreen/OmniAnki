# OmniAnki
[README](./README.md)  - [详细说明](./detail.md)  -  [在线演示](http://yellowandgreen.xyz:7777)

英语卡片单词记忆工具

## 为什么要重新实现Anki?

> 虽然Anki提供了丰富的功能和插件系统，但对于开发者而已还需要额外了解PyQt和相关api，具有有一定的学习成本。且Anki的在线同步功能时好时坏，很难完全掌控自己的单词库，因此我作为一个django新手实现了一个简易的Anki。在其中也加入了自己对于单词记忆的想法。

理想的端到端单词记忆软件应该有简单易用的方法来学习英语：
1. 阅读语料
2. 收集信息并整理成单词例句格式
3. 为不同的牌组使用不同的记忆算法


## OmniAnki的单词记忆理念
### Anki的背诵记忆曲线
Anki能够自动按照每张卡片的记忆历史数据计算出背诵间隔时间，减少了重复学习的时间，使使用者无须考虑如何安排卡片的背诵顺序。

### 拆分简化
> OmniAnki的每张卡片只包含一个释义的例句，背诵时只需按照例句回想起该释义即可。

Anki的一个使用建议是尽可能简化卡片内容，减少背诵负担，便于短时记忆。因此OmniAnki贯彻了此理念。

### 基于语境
1. 正面卡片只包含单词和例句
2. 背面卡片在正面的基础上还增加单词释义和例句翻译

### 易于检索
卡片需要一个强大的检索功能，例如同词根词缀，或相同结构的单词在词汇数量比较多时格外有用。同时便捷的卡片内查词查例句能够让使用者更好的记忆或回想起单词释义。

## **功能:**
1. 实现了实时的新闻获取功能，同时也具有简易的书籍阅读功能（开发中）。
2. 自动从文章中获取例句并生成单词卡片
3. 和Anki相同的卡片使用方法

## Install requirements

```shell
pip install -r requirements.txt
```

## Run this project

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:80
```

## Deploy with Dockerfile(Recommended)

~~~shell
docker-compose up -d
~~~


## Deploy with Remote Docker Image

```shell
docker pull registry.cn-beijing.aliyuncs.com/yellowandgreen/anki_img:1.0
docker run -it -p 8000:80 --name anki_img anki_img:1.0
```

## Import from Anki xlsx file

1. 初始化数据库

   ```
   python manage.py makemigrations 
   python manage.py migrate
   ```

2. 从Anki导出前需要修改导出卡片的显示模板（只有这样才会在答案中正常显示）

3. 修改导出字段顺序后可以直接以xlsx格式导出（不包含媒体和html文件）

   > 排序字段	到期	标签	遗忘次数	简易度	复习	答案

4. 使用utils中的import_from_anki.py导入




## User

默认用户：admin 
密码: 1234

### Add User

```
python manage.py createsuperuser
```


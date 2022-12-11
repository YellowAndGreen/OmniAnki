# OmniAnki

卡片单词记忆工具
A card review tool that has built-in readers to provide an end-to-end language learning experience!

## 为什么要重新实现Anki?

> Anki provides extension plugins for the users to extend its functions, however, the over-complicated database design and the requirement for PyQt knowledge make it hard to develop new features.

The aim of OmniAnki is **to create a web-based end-to-end memory-card tool** that provides an easier method to get around the following processes:

1. Collect information.
2. Aggregate, and extract it into the memory-card format.
3. Select a proper algorithm for different decks.
4. Save it to the database and provide the review function which is identical to Anki.

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

## **Features:**

1. A real-time news fetch function is implemented, in addition, it also has a book-reading function(in progress).
2. An impressively automated card-making function to free learners from strenuous labor.
3. Use memory algorithms to manipulate card review intervals. (in progress)
4. Built-in tag system to leverage your card database.

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

## Deploy with Dockerfile

~~~shell
# 构建Anki镜像
docker build -t anki:1.0 .

# 将镜像作为容器运行
docker run -it -p 8000:80 --name Anki anki:1.0

# 初始化后端数据(第一次执行即可)
docker exec -ti Anki \bin\sh
python manage.py makemigrations 
python manage.py migrate
python manage.py init -y
exit
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

3. 修改导出字段顺序后可以直接导出

   > 排序字段	到期	标签	遗忘次数	简易度	复习	答案

4. 使用utils中的txt2db载入即可


## Import Dict From MDD Files

## User

默认用户：xu 密码 5500

### Add User

```
python manage.py createsuperuser
```

### Add User's setting
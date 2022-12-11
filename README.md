# OmniAnki - a parody of Anki

A card review tool that has built-in readers to provide an end-to-end language learning experience!

## **WHY?**

Why re-implement the Anki?

> Anki provides extension plugins for the users to extend its functions, however, the over-complicated database design and the requirement for PyQt knowledge make it hard to develop new features.

The aim of OmniAnki is **to create a web-based end-to-end memory-card tool** that provides an easier method to get around the following processes:

1. Collect information.
2. Aggregate, and extract it into the memory-card format.
3. Select a proper algorithm for different decks.
4. Save it to the database and provide the review function which is identical to Anki.

## **Features:**

1. A real-time news fetch function is implemented, in addition, it also has a book-reading function(in progress).
2. An impressively automated card-making function to free learners from strenuous labor. 
3. Built-in dictionary system for reading and easy-to-use word-add-from-dictionary function.
4. Use memory algorithms to manipulate card review intervals. (in progress)

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
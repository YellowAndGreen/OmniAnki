# Suki - a parody of Anki
A card review tool which has built-in readers to provide an end-to-end language learning experience!

## **Features:**
1. real-time news fetch function implemented, in addition, it also has a book-reading function(not working very well).
2. an impressively automated card-making function to free learners from strenuous labour.
3. use memory-algorithm to manipulate card review intervals.
4. built-in tag system to leverage your card database.

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
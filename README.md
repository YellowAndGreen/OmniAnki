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

## Run this project

```shell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:80
```

## Deploy with Dockerfile

~~~shell
docker-compose up -d
~~~

## Deploy with Remote Docker Image

```shell
docker pull registry.cn-beijing.aliyuncs.com/yellowandgreen/anki_img:1.0
docker run -it -p 8000:80 --name anki_img anki_img:1.0
```


## Account

user：xu 
password: 5500

### Add User

```
python manage.py createsuperuser
```


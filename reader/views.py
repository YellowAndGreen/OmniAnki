import newspaper
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import *


def article_detailview(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request,
                  'reader/read_article.html',
                  {'article': article
                   })


def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)  # 20 articles in each page
    page = request.GET.get('page')  # 当前页数

    try:
        current_page_articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        current_page_articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        current_page_articles = paginator.page(paginator.num_pages)
    return render(request,
                  'reader/article_list.html',
                  {'articles': current_page_articles,
                   'page': page,
                   })


def update_article(request):
    urls = ['https://www.cnbc.com/', 'https://thenextweb.com/', 'https://www.cnn.com/', 'https://www.wired.com/']
    # 若是主动提交且含有地址，则只要这个url
    if 'url' in request.POST and request.POST['url'][0:4] == 'http':
        urls = [request.POST['url']]
    count_num = 0
    # 删除所有新闻，更新100篇新闻
    Article.objects.all().delete()
    # 循环urls列表，直到50篇新闻
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

    messages.success(request, f"更新{count_num}篇文章")
    return JsonResponse({'status': 'ok'})


def read_book(request):
    books = Book.objects.all()
    paginator = Paginator(books, 10)  # 20 articles in each page
    page = request.GET.get('page')  # 当前页数

    try:
        current_page_books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        current_page_books = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        current_page_books = paginator.page(paginator.num_pages)
    return render(request,
                  'reader/book_list.html',
                  {'books': current_page_books,
                   'page': page,
                   }
                  )


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # 字节码转换
    book.content = book.content.decode()
    return render(request,
                  'reader/book_detail.html',
                  {'book': book,
                   })


def book_progress(request):
    progress = request.POST.get('progress')
    book_id = request.POST.get('book_id')
    book = get_object_or_404(Book, id=book_id)
    if progress and book_id:
        book.progress = progress
        book.save()
        return JsonResponse({'status': '保存成功'})
    return JsonResponse({'progress': book.progress})

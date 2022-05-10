import newspaper
from .models import Article

url = 'https://www.cnbc.com/'
cnbc = newspaper.build(url, memoize_articles=False)

# 只需要100个，且不能为空
count_num = 0
for article in cnbc.articles:
    article.download()
    article.parse()
    if article.text == "" or article.title == "":
        continue
    else:
        count_num += 1
        art_model = Article(title=article.title, content=article.text)
        art_model.save()
        if count_num == 100:
            break

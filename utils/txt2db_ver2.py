import pandas as pd
import re
from flashcards.models import Card
import datetime

data = pd.read_excel('C:\\Users\\Administrator\\Desktop\\Anki\\utils\\anki.xlsx'
                     '', sheet_name='Sheet1', header=0)

for i in range(data.shape[0]):
    val_list = re.split(r"[ ]{3,}", data['答案'][i])

    # 判断是否只有extra
    if len(val_list) == 4:
        extra = val_list[-1]
        example = ""
        translation = ""
    else:
        try:
            example = val_list[3]
            translation = val_list[4]
            try:
                extra = val_list[5]
            except IndexError:
                extra = ""
        except IndexError:
            example = ""
            translation = ""
            extra = ""

    card = Card(group=val_list[0],
                question=re.sub(r"(<.*?>|\[.*?\]|&nbsp;)", "", re.sub(r"<div>", "\n", val_list[1])),
                answer=val_list[2],
                example=example,
                translation=translation,
                extra=extra,
                due=data['到期'][i],
                forget_num=int(data['遗忘次数'][i]),
                review_num=int(data['复习'][i]),
                ratio=int(data['简易度'][i][0:-2]),
                )
    card.save()
# 判断是否有标签，在上面执行后使用
# 同时初始化interval
i = 0
now = datetime.datetime.now()
for card in Card.objects.all():
    card.interval = (card.due - now).days
    if type(data['标签'][i]) == str:
        for tag in re.split(r"[ ]{2,}", data['标签'][i]):
            if tag != ' ':
                card.tags.add(tag)
    card.save()
    i += 1

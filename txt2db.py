import re
from flashcards.models import Card

with open("E:\\vocabulary.txt", 'r', encoding="utf-8") as f:
    read_data = f.readlines()
num = 0
for raw_data in read_data:
    data = raw_data.split('\t')
    card = Card(cid=num, group=data[0], question=data[1], answer=data[2],
                example=data[3], translation=data[4], extra=data[5])
    num += 1
    card.save()

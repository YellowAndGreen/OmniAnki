import collections
import json
import random
import re
from datetime import timedelta, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from taggit.models import Tag

from flashcards.utils import find_example_from_database
from .crontab import update_due_list
from .forms import *
from .models import *
from .utils import to_chinese
from .web_query import find_synonym


# 启动时执行的函数
def onstart():
    coca = {}
    # 将coca存入内存中
    with open('flashcards/static/dict/coca.txt', 'r', encoding='utf-8') as f:
        coca = json.loads(f.read())
    cache.set('coca', coca, timeout=None)


onstart()


# 首页
@login_required
def index(request):
    card_num = Card.objects.count()
    # 获取当前用户的单词列表
    wordlists = request.user.owner.all()
    # 获取过去七天的背诵数据
    now = timezone.now()
    # 七天前作为开始时间
    start = now - timedelta(days=7, hours=now.hour, minutes=now.minute, seconds=now.second)
    # 找到过去七天的背诵数据
    recitedata = Recitedata.objects.filter(date__gt=start)
    rank_count_by_day = []
    for i in range(1, 8):
        all_data = recitedata.filter(date__gt=start + timedelta(days=i), date__lt=start + timedelta(days=i + 1))
        counter = collections.Counter([data.rank for data in all_data])
        rank_count_by_day.append([counter[1], counter[2], counter[3], counter[4]])
    rank_count_by_rank = []
    for i in range(0, 4):
        rank_count_by_rank.append([rank_day[i] for rank_day in rank_count_by_day])
    # 仅返回有单词的tag
    tags = filter(lambda tag: len(Card.objects.filter(tags__in=[tag])), Tag.objects.all())
    return render(request, 'flashcards/anki.html',
                  {'len': card_num,
                   'lenlist': len(wordlists),
                   'wordlists': wordlists,
                   'tags': tags,
                   'recitedata': rank_count_by_rank,
                   })


# 单张卡片浏览
def card_detailview(request, card_id):
    # 从缓存中获取当前设置，若无则从数据库读取并存入缓存
    # random_example = request.user.settings.all()[0] if cache.get('random_example') is None else cache.get(
    #     'random_example')
    if cache.get('random_example') is None:
        # 判断该用户是否有setting
        settings = request.user.settings.all()
        if len(settings) == 0:
            add_setting = Settings(user=request.user)
            add_setting.save()
            random_example = add_setting
        else:
            random_example = request.user.settings.all()[0]
    else:
        random_example = cache.get('random_example')
    # 获取card实例
    card = get_object_or_404(Card, id=card_id)
    # 若当前设置为随机例句且是该卡片属于词汇分组
    if request.user.settings.all()[0].random_example and card.group[0:2] == "词汇":
        result = find_example_from_database(card.question)
        # 有可能查不到
        if len(result[0]) > 0:
            rand_index = random.randint(0, len(result[0]) - 1)
            card.example = result[0][rand_index]
            card.translation = result[1][rand_index]
    # 将例句中的此词标红
    if len(re.findall(r"[a-zA-Z]+", card.question)) > 0:
        reple = re.findall(r"[a-zA-Z]+", card.question)[0]
        card.example = card.example.replace(reple, "<span id='red'><b>" + reple + "</b></span>")
    return render(request,
                  'flashcards/card_detail.html',
                  {'object': card,
                   'tags': card.tags.all(),
                   'random_example': random_example
                   })


# 下一张卡片
@login_required
def nextcardview(request):
    # 有待改进，随机卡片操作十分耗时
    card = Card.objects.all()[random.randrange(1, Card.objects.count(), 1)]
    return redirect(card.get_absolute_url())


# 背诵
@login_required
def cardreciteview(request, card_id, rank):
    # 获取card实例
    card = get_object_or_404(Card, id=card_id)
    # 创建记忆数据并保存
    recitedata = Recitedata(rank=rank, card=card)
    recitedata.save()
    # 生成随机数并跳转至下一卡片
    card = Card.objects.all()[random.randrange(1, Card.objects.count(), 1)]
    return redirect(card.get_absolute_url())


# 展示背诵数据
@login_required
def recitedatadisplay(request):
    # 按rank排序，后续改进
    recitedata = Recitedata.objects.order_by("rank")
    # 使用set以防止card重复
    cards = set([data.card for data in recitedata])
    datas = [{'card': card, 'recitedata': card.recitedata.all()} for card in cards]
    return render(request,
                  'flashcards/recitedata.html',
                  {'datas': datas}
                  )


# 单张卡片背诵数据
def card_recitedata_view(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    all_recitedata = card.recitedata.all()
    return render(request,
                  'flashcards/card_recitedata_detail.html',
                  {'all_recitedata': all_recitedata
                   })


# 修改到此
@login_required
def search(request):
    cd = {"query": ''}
    form = SearchForm(request.GET)
    no_result = False   # 无搜索结果标识符
    if form.is_valid():
        cd = form.cleaned_data
        if cd['query'][0:2] == 'T:':
            tag = get_object_or_404(Tag, slug=cd['query'][2:])
            cards = Card.objects.filter(tags__in=[tag])
        elif cd['query'][0:2] == 'G:':
            cards = Card.objects.filter(group__startswith=cd['query'][2:])
        else:
            cards = Card.objects.filter(
                Q(question__icontains=cd['query']) | Q(example__icontains=cd['query']))
            if not len(cards):
                no_result = True
            else:
                # 将搜索字段替换为红色
                for card in cards:
                    card.question = card.question.replace(cd['query'], "<span id='red'><b>" + cd['query'] + "</b></span>")
                    card.example = card.example.replace(cd['query'], "<span id='red'><b>" + cd['query'] + "</b></span>")
    else:
        form = SearchForm()
        return render(request, 'flashcards/search.html', {'searchvalue': cd['query'],
                                                          'form': form, 'no_result': no_result})
    return render(request, 'flashcards/search.html', {'cards': cards, 'searchvalue': cd['query'],
                                                      'form': form, 'no_result': no_result})


# 撤回：删除背诵记录
@login_required
def undo(request, card_id):
    # 需要撤回的卡片和需要删除背诵记录的卡是一张卡
    card = get_object_or_404(Card, id=card_id)
    card.recitedata.latest('date').delete()
    return redirect(card.get_absolute_url())


# 列表的撤回：删除背诵记录
@login_required
def undo_list(request, list_id, progress):
    wordlist = get_object_or_404(WordList, id=list_id)
    id_list = list(map(lambda dic: dic['id'], json.loads(wordlist.wordlist)))
    card_id = id_list[progress - 1]
    # 需要撤回到的卡片和需要删除背诵记录的卡是一张卡
    card = Card.objects.filter(id=card_id)
    latest_recitedata = card[0].recitedata.latest('date')
    recitedata_params = json.loads(latest_recitedata.params)
    card.due = datetime.strptime(recitedata_params['due'], "%Y-%m-%d %H:%M:%S.%f")
    card.review_num = recitedata_params['review_num']
    card.forget_num = recitedata_params['forget_num']
    card.ratio = recitedata_params['ratio']
    card.interval = recitedata_params['interval']
    card.save()
    latest_recitedata.delete()
    # 修改进度
    return redirect('flashcards:recite_wordlist', list_id, progress - 1, 0)


# 网络搜索
@login_required
def websearch(request):
    cd = {"query": ''}
    form = SearchForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        words = find_synonym(cd['query'])
    else:
        form = SearchForm()
        words = []
    return render(request, 'flashcards/webquery.html',
                  {"words": words, 'searchvalue': cd['query'], 'form': form}, )


@login_required
def dict_search(request):
    cd = {"query": ''}
    form = SearchForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
        # 查词，返回单词和html文件
        html_result = ''
        queryword = cd['query']
        dict_query = Dict.objects.filter(headword=queryword)
        if len(dict_query) == 0:
            dict_query = Dict.objects.filter(headword=queryword.lower())
            if len(dict_query) == 0:
                html_result = 'No Match!'
        html_result = dict_query[0].item
    else:
        form = SearchForm()
        html_result = ''

    return render(request, 'flashcards/dict.html',
                  {'html_result': html_result, 'form': form, 'searchvalue': cd['query'],
                   })


@login_required
def create_wordlist_by_diff(request):
    cd = {"query": 'list'}
    form = SearchForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
    # 找到最近的三个复习data并累计，生成一个字典
    rank_sum_dict = map(lambda card: {'id': card.id, 'rank_sum': sum(
        sorted([Recitedata.rank for Recitedata in card.recitedata.order_by('-date')], reverse=True)[0:3])
    if len(card.recitedata.all()) > 2
    else sum([Recitedata.rank for Recitedata in card.recitedata.order_by('-date')])}
                        , Card.objects.all())
    # 按rank排序，取前五十个值
    # 不知道为什么id列表总为空
    # id_list = [dic['id'] for dic in sorted(list(rank_sum_dict), key=lambda dic: dic['rank_sum'], reverse=True)[0:50]]
    # id_list = list(
    #     map(lambda dic: dic['id'], sorted(list(rank_sum_dict), key=lambda dic: dic['rank_sum'], reverse=True)[0:50]))
    # print(id_list)
    sort_list = sorted(list(rank_sum_dict), key=lambda dic: dic['rank_sum'], reverse=True)[0:50]
    wordlist = WordList(owner=request.user, name=cd['query'], wordlist=json.dumps(sort_list)
                        , len_list=len(sort_list))
    wordlist.save()
    messages.success(request, '单词列表创建成功')
    return redirect('flashcards:dashboard')


@login_required
def create_wordlist_by_tag(request):
    cd = {"query": 'list', "tag": 'marked'}
    form = SearchForm(request.GET)
    if form.is_valid():
        cd = form.cleaned_data
    tag = get_object_or_404(Tag, slug=request.GET['tag'])
    cards = Card.objects.filter(tags__in=[tag])
    id_list = [{'id': card.id} for card in cards]
    wordlist = WordList(owner=request.user, name=cd['query'], wordlist=json.dumps(id_list)
                        , len_list=len(id_list))
    wordlist.save()
    messages.success(request, '单词列表创建成功')
    return redirect('flashcards:dashboard')


@login_required
def recite_wordlist(request, wordlist_id, progress, rank):
    wordlist = WordList.objects.filter(id=wordlist_id)[0]
    # 判断请求progress和数据库progress是否相等，若不同，则将后者覆盖（在重新复习的时候可能出现的问题）
    if progress == 0 and wordlist.progress != 0:
        wordlist.progress = progress

    # json解析单词列表id
    id_list = list(map(lambda dic: dic['id'], json.loads(wordlist.wordlist)))
    # 判断是刚进入还是进入后第一次提交卡片
    # 若提交，则更新进度
    # 若刚进入，则不更新进度

    if rank > 0:
        # 获取当前card实例
        current_card = get_object_or_404(Card, id=id_list[progress])
        # 获取当前时间
        current_time = datetime.datetime.now()
        # 创建并保存记忆数据
        recitedata = Recitedata(rank=rank, card=current_card)
        recitedata.save()

        # 计算完成度
        wordlist.progress = progress + 1
        percentage = int((wordlist.progress / wordlist.len_list) * 100)
        # 更新进度
        wordlist.save()

        # 若为due列表则还需要更新due参数
        if wordlist.name == 'due':
            # 将参数保存进recitedata
            recitedata_params = {'due': str(current_card.due), 'review_num': current_card.review_num,
                                 'forget_num': current_card.forget_num,
                                 'ratio': current_card.ratio, 'interval': current_card.interval}
            recitedata.params = json.dumps(recitedata_params)
            recitedata.save()
            if rank == 4:
                print(
                    f"{current_card.question}:更新前due为{current_card.due}，interval为{current_card.interval}，简易度为{current_card.ratio}。")
                # 卡片进入重新学习队列，简易度减少 20 个百分点
                current_card.due = current_time
                # 间隔设置为0，以便于区分
                current_card.interval = 0
                # 简易度最低为 130%
                if current_card.ratio >= 150:
                    current_card.ratio -= 20
                print(
                    f"{current_card.question}:更新后due为{current_card.due}，interval为{current_card.interval}，简易度为{current_card.ratio}。")

            elif rank == 3:
                # 卡片的简易度减少 15% ，当前的间隔乘以 1.2。
                current_card.interval = int(1.2 * current_card.interval)
                current_card.due = current_time + timedelta(days=current_card.interval)
                if current_card.ratio >= 145:
                    current_card.ratio -= 15
                # 困难惩罚，防止一直选3和2时的间隔增长
                if current_card.ratio <= 180:
                    current_card.interval = int(0.8 * current_card.interval)
                    current_card.due = current_time + timedelta(days=current_card.interval)
            elif rank == 2:
                if current_card.interval == 0:
                    current_card.interval = 3
                # 卡片的简易度减少 5% ，当前的间隔乘以 1.1。
                else:
                    current_card.interval = int(1.1 * current_card.interval)
                current_card.due = current_time + timedelta(days=current_card.interval)
                if current_card.ratio >= 135:
                    current_card.ratio -= 5
            elif rank == 1:
                print(
                    f"{current_card.question}:更新前due为{current_card.due}，interval为{current_card.interval}，简易度为{current_card.ratio}。")
                if current_card.interval == 0:
                    current_card.interval = 4
                # 当前间隔乘以当前简易度再乘以简单奖励，简易度增加 15 个百分点。
                else:
                    current_card.interval = int(0.01 * current_card.interval * current_card.ratio)
                current_card.due = current_time + timedelta(days=current_card.interval)
                if current_card.ratio >= 135:
                    current_card.ratio += 15
                print(
                    f"{current_card.question}:更新后due为{current_card.due}，interval为{current_card.interval}，简易度为{current_card.ratio}。")

            current_card.save()
    else:
        wordlist.progress = progress
        percentage = int((wordlist.progress / wordlist.len_list) * 100)

    # 进度更新后判断是否完成单词列表，若完成，则返回主页
    if wordlist.progress == wordlist.len_list:
        messages.success(request, '您已背完该单词列表！')
        # 若为due列表，则刷新此列表
        if wordlist.name == 'due':
            update_due_list()
        return redirect('flashcards:dashboard')
    # 获取下一个单词
    # 必须使用数据库中的wordlist.progress，否则使用progress会导致第一个不更新
    next_word = get_object_or_404(Card, id=id_list[wordlist.progress])
    if request.user.settings.all()[0].random_example and next_word.group[0:2] == "词汇":
        result = find_example_from_database(next_word.question)
        # 有可能查不到
        if len(result[0]) > 0:
            rand_index = random.randint(0, len(result[0]) - 1)
            next_word.example = result[0][rand_index]
            next_word.translation = result[1][rand_index]
    # 将例句中的此词标红
    reple = re.findall(r"[a-zA-Z]+", next_word.question)[0]
    next_word.example = next_word.example.replace(reple, "<span id='red'><b>" + reple + "</b></span>")

    return render(request, 'flashcards/card_list.html',
                  {
                      "percentage": percentage,
                      'object': next_word,
                      'progress': wordlist.progress,
                      'wordlist_id': wordlist_id,
                      'tags': next_word.tags.all(),
                      'section': 'list',
                  })


@login_required
def delete_wordlist(request, wordlist_id):
    get_object_or_404(WordList, id=wordlist_id).delete()
    messages.success(request, '单词列表删除成功')
    return redirect('flashcards:dashboard')


@login_required
def word_add_tags(request, word_id, tag, section):
    word = get_object_or_404(Card, id=word_id)
    word.tags.add(tag)
    messages.success(request, '标签添加成功')
    if section == 0:
        return redirect('flashcards:card_detail', card_id=word_id)
    else:
        return redirect('flashcards:recite_wordlist', wordlist_id=section,
                        progress=get_object_or_404(WordList, id=section).progress, rank=0)


@login_required
def word_delete_tags(request, word_id, tag_id, section):
    word = get_object_or_404(Card, id=word_id)
    word.tags.remove(Tag.objects.filter(id=tag_id)[0])
    messages.success(request, '标签删除成功')
    # 判断是否为单词列表
    if section == 0:
        return redirect('flashcards:card_detail', card_id=word_id)
    else:
        return redirect('flashcards:recite_wordlist', wordlist_id=section,
                        progress=get_object_or_404(WordList, id=section).progress, rank=0)


@login_required
def word_edit(request, word_id, section):
    word = get_object_or_404(Card, id=word_id)
    cd = request.POST
    word.group = cd['group']
    word.question = cd['question']
    word.answer = cd['answer']
    word.example = cd['example']
    word.translation = cd['translation']
    word.extra = cd['extra']
    if cd['tag'] != '':
        word.tags.add(cd['tag'])
    word.save()
    messages.success(request, '词汇编辑成功！')
    if section == 0:
        return redirect('flashcards:card_detail', card_id=word_id)
    else:
        return redirect('flashcards:recite_wordlist', wordlist_id=section,
                        progress=get_object_or_404(WordList, id=section).progress, rank=0)


@login_required
def word_add(request):
    # set = request.user.settings.all()[0]
    # set_group = json.loads(set.current_group)
    if request.POST:
        word = Card()
        cd = request.POST
        word.group = cd['group']
        word.question = cd['question']
        word.answer = cd['answer'].replace('；', '，')
        word.example = cd['example'].replace('\n', ' ').replace('"', '')
        word.translation = cd['translation'].replace('\n', ' ')
        word.extra = cd['extra']
        if cd['tag'] != '':
            word.tags.add(cd['tag'])
        # # 仅在前两字为词汇或者整个为空的时候进行检查
        # if word.group == '' or word.group[0:2] == '词汇':
        #     # 检查setting中数值是否大于等于50，若大于50，则group加1,数量初始化为1，最后保存set
        #     if set_group['max_word_num'] >= 50:
        #         set_group['max_word_group'] += 1
        #         set_group['max_word_num'] = 0
        #     # 转化为最大group并转为中文
        #     word.group = ''.join(['词汇-第', to_chinese(set_group['max_word_group']), '组'])
        #     # 最后num数加一
        #     set_group['max_word_num'] += 1
        #     set.current_group = json.dumps(set_group)
        #     set.save()
        word.save()
        return JsonResponse({'status': 'ok'})
    else:
        return render(request, 'flashcards/card_create.html')


@login_required
def word_delete(request, word_id):
    get_object_or_404(Card, id=word_id).delete()
    messages.success(request, '词汇删除成功！')
    return redirect('flashcards:next')


@login_required
def settings_view(request):
    settings = request.user.settings.all()[0]
    # 根据有无path来判断是GET还是POST
    if not ("path" in request.POST):
        return render(request, 'flashcards/settings.html', {'random_example': settings.random_example})
    # if not (bool(request.GET) and bool(request.POST)):
    #     return render(request, 'flashcards/settings.html', {'random_example': settings.random_example})
    if request.POST:
        if "random_example" in request.POST and request.POST['random_example'] == 'on':
            settings.random_example = True
            # 将其存入内存
            cache.set('random_example', True, timeout=600)
            settings.save()
        else:
            settings.random_example = False
            cache.set('random_example', False, timeout=600)
            settings.save()

    if request.POST['path'] == "/flashcards/settings/":
        # 防止多次跳转出错
        return render(request, 'flashcards/settings.html', {'random_example': settings.random_example})
    return redirect(request.POST['path'])


@login_required
@require_POST
def dict_query(request):
    re_filter = re.findall(r"[a-zA-Z]+", request.POST.get('query_word'))
    if len(re_filter) == 0:
        return JsonResponse({"query_word": request.POST.get('query_word'), 'html_result': 'No Match!'})
    query_word = re_filter[0]
    # print(query_word)

    # 备选列表
    query_list = [query_word, query_word.lower(), query_word[0:-1], query_word[0:-2], query_word[0:-3]]
    for query_list_word in query_list:
        query_result = Dict.objects.filter(headword__startswith=query_list_word)
        if len(query_result) != 0:
            # 查询缓存中的COCA
            rank = cache.get('coca', default=-1).get(query_result[0].headword, -1)
            return JsonResponse(
                {"query_word": query_result[0].headword, 'html_result': query_result[0].item, 'rank': rank})

    return JsonResponse({"query_word": query_word, 'html_result': 'No Result!'})


# get方式的字典请求
def dict_query_get(request, query_word):
    re_filter = re.findall(r"[a-zA-Z]+", query_word)
    if len(re_filter) == 0:
        return JsonResponse({"query_word": request.POST.get('query_word'), 'html_result': 'No Match!'})
    query_word = re_filter[0]
    # print(query_word)

    # 备选列表
    query_list = [query_word, query_word.lower(), query_word[0:-1], query_word[0:-2], query_word[0:-3]]
    for query_list_word in query_list:
        query_result = Dict.objects.filter(headword__startswith=query_list_word)
        if len(query_result) != 0:
            return JsonResponse({"query_word": query_list_word, 'html_result': query_result[0].item})

    return JsonResponse({"query_word": query_word, 'html_result': 'No Result!'})


@require_POST
def get_example(request):
    re_filter = re.findall(r"[a-zA-Z]+", request.POST.get('query_word'))
    if len(re_filter) == 0:
        return JsonResponse({"query_word": request.POST.get('query_word'), 'html_result': 'No Match!'})
    query_word = re_filter[0]
    # print(query_word)

    # 备选列表
    query_list = [query_word, query_word.lower(), query_word[0:-1], query_word[0:-2], query_word[0:-3]]
    for query_list_word in query_list:
        query_result = Dict.objects.filter(headword__startswith=query_list_word)
        if len(query_result) != 0:
            result = find_example_from_database(query_list_word)

            return JsonResponse({"example": json.dumps(list(zip(result[0], result[1]))),
                                 "meanings": json.dumps(result[2])
                                 })

    return JsonResponse({"example": json.dumps([[], []])})


@require_POST
def export_card_as_txt(request):
    settings = request.user.settings.all()[0]
    num = int(request.POST["num"])

    cards = Card.objects.all()[len(Card.objects.all()) - num:]
    try:
        with open("export.txt", 'w', encoding="utf-8") as f:
            for card in cards:
                card.answer = card.answer.replace('\n', '<br>')
                f.write(
                    f"{card.group}\t{card.question}\t{card.answer}\t{card.example}\t{card.translation}\t{card.extra}\n")
        messages.success(request, f'导出成功，共导出{len(cards)}张卡片')

        return FileResponse(open('export.txt', 'rb'), as_attachment=True)
    except Exception as e:
        messages.error(request, '导出失败')
        return redirect('flashcards:settings_view')


def export_db(request):
    return FileResponse(open('db.sqlite3', 'rb'), as_attachment=True)




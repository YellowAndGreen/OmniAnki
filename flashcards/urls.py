from django.urls import path

from flashcards.views import *

app_name = 'flashcards'
urlpatterns = [
    # 主页
    path('', index, name='dashboard'),
    # 单张卡片浏览
    path('<int:card_id>', card_detailview, name='card_detail'),
    # 下一张卡片
    path('next/', nextcardview, name='next'),
    # 背诵卡片
    path("recite/<int:card_id>/<int:rank>", cardreciteview, name="recite"),
    # 展示背诵数据
    path("recitedata/", recitedatadisplay, name="display"),
    # 展示单张卡片背诵数据
    path('card_recitedata_view/<int:card_id>/', card_recitedata_view, name='card_recitedata_view'),
    # 撤回：删除背诵数据
    path('undo/<int:card_id>', undo, name='undo'),
    # 列表的撤回：删除背诵记录
    path('undo_list/<int:list_id>/<int:progress>/', undo_list, name='undo_list'),
    # 查询某个单词
    path('search/', search, name='search'),
    # 网络搜索
    path('websearch/', websearch, name='websearch'),
    # 字典界面
    path('dict/', dict_search, name='dict'),
    path('create_wordlist_by_diff/', create_wordlist_by_diff, name='create_wordlist_by_diff'),
    path('create_wordlist_by_tag/', create_wordlist_by_tag, name='create_wordlist_by_tag'),
    path('delete_wordlist/<int:wordlist_id>/', delete_wordlist, name='delete_wordlist'),
    path('recite_wordlist/<int:wordlist_id>/<int:progress>/<int:rank>/', recite_wordlist, name='recite_wordlist'),
    path('word_add_tags/<int:word_id>/<slug:tag>/<int:section>/', word_add_tags, name='word_add_tags'),
    path('word_delete_tags/<int:word_id>/<int:tag_id>/<int:section>/', word_delete_tags, name='word_delete_tags'),
    path('word_edit/<int:word_id>/<int:section>/', word_edit, name='word_edit'),
    path('word_add/', word_add, name='word_add'),
    path('word_delete/<int:word_id>/', word_delete, name='word_delete'),
    path('settings/', settings_view, name='settings_view'),
    path('dict_query/', dict_query, name='dict_query'),
    path('get_example/', get_example, name='get_example'),
    path('export_card_as_txt/', export_card_as_txt, name='export_card_as_txt'),
    path('export_db/', export_db, name='export_db'),
    path('dict_query_get/<slug:query_word>/', dict_query_get, name='dict_query_get'),
    path('test',CourseEnrollView.as_view())
]

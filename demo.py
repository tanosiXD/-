# -*- coding: utf-8 -*-
# @company : PERFECT DATA
# @Author  : Eugenia
# @File    : demo.py
# @Time    : 2022/6/23 0023 11:42
# @schedule：
# sql = f"""replace into baidu_index_hx (word,startdate,enddate,descr,tgi,  word_rate, all_rate,flag ) values ({('%s,' * 8)[:-1]})"""
# print(sql)
# d= 'https://nanjing.esf.fang.com/loupan/office/1810179228.htm'.split('/')[-1].split('.')[0]
# print(d)
import re

import requests
from fang_tx import main_lp
headers= {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'cookie': 'global_cookie=rh37ob2fafvrczm0pl2bafxzd10l4p8s63b; csrfToken=3IkA5KX2pntGjKV8JlLFHhCB; __utma=147393320.1602981976.1655881024.1655881024.1655881024.1; __utmc=147393320; __utmz=147393320.1655881024.1.1.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=nanjing; lastscanpage=0; g_sourcepage=esf_xq%5Elb_pc; unique_cookie=U_rh37ob2fafvrczm0pl2bafxzd10l4p8s63b*57; __utmb=147393320.156.10.1655881024',
    'referer':'https://nanjing.esf.fang.com/housing/272__0_3_0_0_1_0_0_0/'
}
dict= {
    265:65,
    263:58,
    264:31,
    267:29,
    270:32,
    268:61,
    271:28,
    272:23,
    269:24,
    274:13,
    275:8
}

main_lp()

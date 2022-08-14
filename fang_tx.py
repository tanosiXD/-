# -*- coding: utf-8 -*-
# @company : PERFECT DATA
# @Author  : Master Doclux
# @File    : fang_tx.py
# @Time    : 2022/6/22 0022 15:00
# @schedule：


import pandas as pd

from lxml import etree
import pymysql
import requests
import re

headers= {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'cookie': 'global_cookie=rh37ob2fafvrczm0pl2bafxzd10l4p8s63b; csrfToken=3IkA5KX2pntGjKV8JlLFHhCB; __utma=147393320.1602981976.1655881024.1655881024.1655881024.1; __utmc=147393320; __utmz=147393320.1655881024.1.1.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=nanjing; lastscanpage=0; g_sourcepage=esf_xq%5Elb_pc; unique_cookie=U_rh37ob2fafvrczm0pl2bafxzd10l4p8s63b*57; __utmb=147393320.156.10.1655881024',
    'referer':'https://nanjing.esf.fang.com/housing/272__0_3_0_0_1_0_0_0/'
}






conn = pymysql.connect(host='192.168.2.30', user='lwl', passwd='lwl', db='datatest', port=3306,
                                    charset='utf8')
cursor = conn.cursor()

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


def jud(obj):
    return obj[0].replace('\t', '').replace('\r', '').replace('\n', '') if len(obj)>0 else None

def gsm(dict,key):
    try:
        return dict[key]
    except:
        return  None

# 楼盘信息
def get_project_msg(prjid):
    dict_lis = {}
    url = f'https://nanjing.esf.fang.com/loupan/{prjid}.htm'
    #print(url)
    lp_res= requests.get(url,headers=headers)

    if '访问验证-房天下' not in lp_res.text:
        tree = etree.HTML(lp_res.text)
        li_list= tree.xpath('/html/body/div[3]/div[4]/div[2]/div[2]/ul/li')

        for i in range(1,len(li_list)+1):
            key= jud(tree.xpath(f'/html/body/div[3]/div[4]/div[2]/div[2]/ul/li[{i}]/span/text()'))

            value= jud(tree.xpath(f'/html/body/div[3]/div[4]/div[2]/div[2]/ul/li[{i}]/p/a/text()'))

            if value is  None:
                 value= jud(tree.xpath(f'/html/body/div[3]/div[4]/div[2]/div[2]/ul/li[{i}]/p/text()'))


            if key is not None:
                dict_lis[key]=value




        kfs=gsm(dict_lis,'开发商')
        wy = gsm(dict_lis, '物业公司')
        #print(kfs,wy)
        sql = f"""update project set kfs_company='{kfs}',wy_company='{wy}'  where prjid='{prjid}'"""
        cursor.execute(sql)
        conn.commit()
        #print(prjid,wy_company,kfs_company)

        #print(type(esf_href))
    else:

        s=input('请手工验证：')
        get_project_msg(prjid)


# 房源信息
def get_house_msg(prjid):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'cookie': 'global_cookie=rh37ob2fafvrczm0pl2bafxzd10l4p8s63b; csrfToken=3IkA5KX2pntGjKV8JlLFHhCB; __utma=147393320.1602981976.1655881024.1655881024.1655881024.1; __utmc=147393320; __utmz=147393320.1655881024.1.1.utmcsr=search.fang.com|utmccn=(referral)|utmcmd=referral|utmcct=/; city=nanjing; lastscanpage=0; g_sourcepage=esf_xq%5Elb_pc; unique_cookie=U_rh37ob2fafvrczm0pl2bafxzd10l4p8s63b*57; __utmb=147393320.156.10.1655881024',
        'referer': 'https://nanjing.esf.fang.com/loupan/{prjid}.htm'
    }
    xm_res = requests.get(url=f'https://nanjing.esf.fang.com/house-xm{prjid}/', headers=headers)
    page_text= xm_res.text
    tree=etree.HTML(page_text)
    district= tree.xpath('')
    dl_list= tree.xpath('/html/body/div[4]/div[4]/div[4]/dl')
    for dl in dl_list:
        href= dl.xpath('./dd[1]/h4/a/@href/text()')[0]
        channel = dl.xpath('/dd[1]/h4/a/@data_channel/text()')[0]
        psid = dl.xpath('/dd[1]/h4/a/@ps/text()')[0]
        house_href= f'https://nanjing.esf.fang.com/{href}?channel={channel}&psid={psid}'
        print(house_href)
        house_res= requests.get(url=house_href,headers=headers)
        page_text = house_res.text
        tree = etree.HTML(page_text)
        price_all= tree.xpath('/html/body/div[4]/div[1]/div[4]/div[1]/div[1]/div[1]/i/text()')[0]
        type= tree.xpath('/html/body/div[4]/div[1]/div[4]/div[4]/div[1]/div[1]/text()')[0]
        price= tree.xpath('/html/body/div[4]/div[1]/div[4]/div[4]/div[3]/div[1]/text()')[0]
        forward= tree.xpath('/html/body/div[4]/div[1]/div[4]/div[5]/div[1]/div[1]/text()')[0]
        floor= tree.xpath('/html/body/div[4]/div[1]/div[4]/div[5]/div[2]/div[1]/a/text()')[0]
        zx_level=tree.xpath('/html/body/div[4]/div[1]/div[4]/div[5]/div[3]/div[1]/a/text()')[0]

#楼盘列表
def get_project_list(area,pNum):
    url = f'https://nanjing.esf.fang.com/housing/{area}__0_3_0_0_{pNum}_0_0_0/'
    # print(url)
    res = requests.get(url=url, headers=headers)

    prjids=re.findall('href="/loupan/(.*?).htm" target="_blank" class="plotTit">',res.text,re.I)

    for prjid in prjids:
        return prjid
     #     info = (lp_name, lp_id)
     #     # print(info)
     #     sql = f"""replace into project (projectname,prjid ) values ({('%s,' * 2)[:-1]})"""
     #     # cursor.execute(sql, info)
     #     # conn.commit()
     #     intp_loupan_data(t_href)


def main_lp():
    for area in dict.keys():
        for pNum in range(1, dict[area] + 1):
            get_project_list(area, pNum)

def main_dt():
    df=pd.read_sql('select prjid from project where wy_company is null',conn)
    print(df.shape[0])
    for prjid in df['prjid']:
        try:
            get_project_msg(prjid)
        except  Exception as e:
            print(prjid,e)



if __name__ == '__main__':
    main_dt()




                #print(t_href)
                #xq_res= requests.get(url= t_href,headers=headers)
                #print(xq_res)






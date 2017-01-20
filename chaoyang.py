#coding=utf-8
import urllib
import urllib.request
import re
import pymysql
import datetime
import time
import random

#链接 mysql 数据库
conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",passwd="root",db="kakamaifang",charset="utf8")
cur = conn.cursor()

#定义url 要爬的链接和商圈名
host = 'http://bj.lianjia.com'
area = [
            "/chengjiao/chaoyang/",
        ]
trade = [
            "chaoyang",
        ]
errorUrl = []
#筛选数据插入数据库函数
def procBuilding(_trade, html):
    #匹配标题
    match3 = re.search(r'<div class="title">.*?href="([^"]+?)".*?>([^>]+?)</a>.*?</div>', html)
    if match3 == None:
        return 'false'
    else:
        data_mysql = {'title': match3.group(2), 'url': match3.group(1)}
        match4 = re.match(r'http://bj.lianjia.com/chengjiao/(.*?).html', match3.group(1))
        data_mysql['sourceId'] = match4.group(1)
    #匹配朝向装修电梯
    match5 = re.search(r'<span class="houseIcon"></span>(.*?)</div>', html)
    if match5 == None:
        data_mysql['houseInfo'] = " "
    else:
        data_mysql['houseInfo'] = match5.group(1)
    #匹配成交日期
    match6 = re.search(r'<div class="dealDate">(.*?)</div>', html)
    if match6 == None:
        data_mysql['dealDate'] = " "
    else:
        data_mysql['dealDate'] = match6.group(1)
    #匹配成交总价
    match7 = re.search(r'class="totalPrice"><span class=\'number\'>(.*?)</span>(.*?)</div>', html)
    if match7 == None:
        data_mysql['totalPrice'] = " "
        data_mysql['totalPriceUnit'] = " "
    else:
        data_mysql['totalPrice'] = match7.group(1)
        data_mysql['totalPriceUnit'] = match7.group(2)
    #匹配楼层年代
    match8 = re.search(r'<span class="positionIcon"></span>(.*?)</div>', html)
    if match8 == None:
        data_mysql['positionInfo'] = " "
    else:
        data_mysql['positionInfo'] = match8.group(1)
    #匹配链家成交
    match9 = re.search(r'class="source">(.*?)</div>', html)
    if match9 == None:
        data_mysql['source'] = " "
    else:
        data_mysql['source'] = match9.group(1)
    #
    match10 = re.search(r'class="unitPrice"><span class="number">(.*?)</span>(.*?)</div>', html)
    if match10:
        data_mysql['unitPrice'] = match10.group(1)
        data_mysql['unitPriceUnit'] = match10.group(2)
    else:
        return 'false'
    match11 = re.search(r'class="dealHouseTxt">(.*?)</span></div>', html)
    if match11 == None:
        data_mysql['dealHouseTxt'] = " "
    else:
        match12 = re.search(r'<span>(.*?)</span><span>(.*?)</span>', match11.group(1))
        if match12 == None:
            match13 = re.search(r'<span>(.*?)</span>', match11.group(1))
            data_mysql['dealHouseTxt'] = match13.group(1)
        else:
            data_mysql['dealHouseTxt'] = match12.group(1) + ' ' + match12.group(2)
    cols = ""
    vals = ""
    for key, value in data_mysql.items():
        cols = cols + "`" + key + "`,"
        vals = vals + "'" + value + "',"
        # print (key,'corresponds to', value)
    sql = "select id from kk_house where `sourceid` = '" + str(data_mysql['sourceId']) + "'"
    title = data_mysql['title'].split()
    if data_mysql['houseInfo'] == " ":
        data_mysql['rowards'] = " "
        data_mysql['renovation'] = " "
        data_mysql['elevator'] = " "
    else:
        houseInfo = data_mysql['houseInfo'].split('|')
        if len(houseInfo) == 3:
            data_mysql['rowards'] = houseInfo[0]
            data_mysql['renovation'] = houseInfo[1]
            data_mysql['elevator'] = houseInfo[2]
        elif len(houseInfo) == 2:
            data_mysql['rowards'] = houseInfo[0]
            data_mysql['renovation'] = houseInfo[1]
            data_mysql['elevator'] = " "
        else:
            data_mysql['rowards'] = houseInfo[0]
            data_mysql['renovation'] = " "
            data_mysql['elevator'] = " "
    if data_mysql['dealHouseTxt'] == " ":
        data_mysql['ditie'] = " "
        data_mysql['ditiezhan'] = " "
        data_mysql['ditiejianju'] = " "
    else:
        dealHouseTxt = data_mysql['dealHouseTxt'].split()
        if len(dealHouseTxt) == 1:
            fangben = re.search(r'房本.*?',dealHouseTxt[0])
            if fangben == None:
                ditie = dealHouseTxt[0].split('号线')
                mi = re.findall(r'(.*?)([0-9]*?)米', ditie[1])
                data_mysql['ditie'] = ditie[0][1:] + '号线'
                data_mysql['ditiezhan'] = mi[0][0]
                data_mysql['ditiejianju'] = mi[0][1]
            else:
                data_mysql['zhengce'] = fangben.group()
                data_mysql['ditie'] = " "
                data_mysql['ditiezhan'] = " "
                data_mysql['ditiejianju'] = " "
        else:
            ditie = dealHouseTxt[1].split('号线')
            mi = re.findall(r'(.*?)([0-9]*?)米',ditie[1])
            data_mysql['zhengce'] = dealHouseTxt[0]
            data_mysql['ditie'] = ditie[0][1:] + '号线'
            data_mysql['ditiezhan'] = mi[0][0]
            data_mysql['ditiejianju'] = mi[0][1]
    if data_mysql['positionInfo'] == " ":
        data_mysql['buildings'] = " "
        data_mysql['age'] = " "
        data_mysql['number'] = " "
    else:
        positionInfo = data_mysql['positionInfo'].split()
        if len(positionInfo) == 1:
            louceng = re.search(r'楼层',positionInfo[0])
            louceng2 = re.search(r'地下',positionInfo[0])
            if louceng == None and louceng2 == None:
                age = positionInfo[0].split('建')
            elif louceng2 == None or louceng == None:
                data_mysql['number'] = positionInfo[0]
        else:
            data_mysql['number'] = positionInfo[0]
            age = positionInfo[1].split('建')
            if len(age) == 1:
                data_mysql['buildings'] = age[0]
                data_mysql['age'] = " "
            else:
                data_mysql['age'] = age[0]
                data_mysql['buildings'] = age[1]
    data_mysql['compound'] = title[0]
    data_mysql['layout'] = title[1]
    data_mysql['space'] = title[2]
    data_mysql['area'] = '朝阳'
    data_mysql['trade'] = _trade
    cur.execute(sql)
    result = cur.fetchone()
    if result != None:
        return 'false'
    sql = "insert into kk_house (%s) values(%s)" % (cols[:-1], vals[:-1])
    cur.execute(sql)
    conn.commit()
    print('插入成功')

#递归爬链接函数
def getHouseData (_trade, url, page = 1, end = 1):
    pgurl = url if page == 1  else url+'pg'+str(page)+'/' #拼接url
    print(pgurl)
    #最多爬取100页，然后下一个链接
    if page == 101:
        print(pgurl+'插入完成')
        return 'false'
    #定义headers头执行爬取
    req = urllib.request.Request(url = pgurl,headers= {
        'Connection':'keep-alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Host':'bj.lianjia.com',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/55.0.2883.87 Chrome/55.0.2883.87 Safari/537.36',
    })
    data = urllib.request.urlopen(req).read().decode('utf8')
    #爬取商圈链接加入待爬列表
    if url == 'http://bj.lianjia.com/chengjiao/chaoyang/':
        match = re.findall(r'<a href="(.*)" >(.*)</a>',data)
        match = match[2:-1]
        for uri in match:
            area.append(uri[0])
            trade.append(uri[1])
        area.append("/chengjiao/chaoyang/")
        return 'false'
    #kaishipipeishuju
    match1 = re.search(r'<ul class="listContent">(.*?)</ul>', data)
    #如果被屏蔽，15秒后重新尝试，3次还是不行，爬取下一个链接
    if match1 == None:
        if end > 3:
            errorUrl.append(pgurl)
            print(pgurl+'没有ul')
            return 'false'
        time.sleep(15)
        return getHouseData(_trade, url, page, end + 1)
    match2 = re.findall(r'<li>(.*?)</li>', match1.group(1))
    if match2 == None:
        print(pgurl+'没有li')

    # 循环本页数据插入数据库
    for html in match2:
        proRes = procBuilding(_trade,html)
        if proRes == 'false':
            errorUrl.append(pgurl)
            continue
    #30秒后爬取下一页数据
    time.sleep(30)
    return getHouseData(_trade, url, page + 1)

#循环爬取列表进行爬取
for index,uri in enumerate(area):
    ret = getHouseData(trade[index],host+uri)
    if ret == 'false':
        continue
#关闭数据库链接
cur.close()
conn.close()

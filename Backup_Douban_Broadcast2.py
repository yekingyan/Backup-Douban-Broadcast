import re
import requests
from bs4 import BeautifulSoup
import lxml
import time


def havetimes():
    times = re.findall('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
    return bool(times)

def haveStars():
    stars = re.findall('<span.*?stars.*?>(.*?)</span>', broadcast)
    return bool(stars)



#判断这条广播有没有书本的信息，<div class = 'bd book'>
def book():
    #如果这条广播有书本的信息，返回布尔值
    haveBook = re.search('bd\sbook', broadcast )
    return bool(haveBook)

def haveSayBook():
    sayBook = re.search('<p>(.*)</p>', broadcast)
    return bool(sayBook)


#判断这条广播是不是sns信息，<div class = 'bd sns'>
def sns():
    # 如果这条广播是sns信息，返回布尔值
    haveSns = re.search('bd\ssns', broadcast )
    return bool(haveSns)

#判断这条广播有没有电影的信息，<div class = 'bd movie'>
def movie():
    # 如果这条广播有电影的信息，返回布尔值
    haveMovie = re.search('bd\smovie', broadcast)
    subject = re.search('.*?block-subject.*?', broadcast)#上传图片到电影会有干扰
    return bool(haveMovie and subject)

def haveSayMovie():
    sayMovie = re.search('<p>(.*)</p>.*?</p>', broadcast, re.S)
    return (bool(sayMovie))

#判断这条广播有没有豆列的信息，<div class = 'bd doulist'>
def doulist():
    # 如果这条广播有豆列的信息，返回布尔值
    haveDoulist = re.search('bd\sdoulist', broadcast)
    return bool(haveDoulist)

def haveSaydoulit():
    Saydoulit = re.search('<p>(.*)</p>', broadcast)
    return bool(Saydoulit)

#判断这条广播有没有音乐的信息，<div class = 'bd music'>
def music():
    #如果这条广播有音乐的信息，返回布尔值
    haveMusic = re.search('bd\smusic', broadcast)
    return bool(haveMusic)

def haveSayMusic():
    sayMusic = re.search('<p>(.*)</p>', broadcast)
    return bool(sayMusic)

#伪装用户
headers = {
    'Uesr-Agent':'---------------------------------这段文字更替为所需的内容---------------------------',
    'Cookie':'-------------------------------------这段文字更替为所需的内容---------------------------'
}
def getData(page):
    #获取网页数据
    urlSave = "https://www.douban.com/people/yekingyan/statuses?p=%s" % page
    req = requests.get(urlSave,headers=headers)
    soup = BeautifulSoup(req.text,'lxml')
    # beautifulsoup解析后，获取所需的数据
    broadcasts = soup.select('div.mod')
    # 设置一个暂停时间，太快的话，豆瓣会锁号的（不是封号）。 一毛一条解锁短信：）
    time.sleep(2)

    global broadcast #broadcast变量需要全局化，整个脚本的信息都是利用它作正则表达式
    #遍历每条广播
    for broadcast in broadcasts:

        #转换数据类型，不然会报错
        broadcast = str(broadcast)

        #判断每条广播的类型，根据不同类型做正则表达式，输入正确的内容
        if sns():#文字广播相关
            times = re.findall('\d{4}\S\d{2}\S\d{2}\s\S{8}',broadcast)
            say = re.search('<p>(.*)</p>',broadcast,re.S)
            if havetimes():
                print(times[0])
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print(say.group(1))
            print('')
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(say.group(1))
                f.write('\n')
                f.seek(0)

        elif movie():#电影、电视剧相关
            times = re.findall('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
            movieName = re.search('<a\shref.*?blank.*?>(.*?)</a>',broadcast)
            stars = re.search('<span.*?>(.*?)</span>',broadcast)
            action = re.search('\s{6}([\u4e00-\u9fa5]{2})',broadcast)#想看还是看过
            Img = re.search('<img\ssrc="(.*?)"',broadcast)
            if havetimes():
                print(times[0])
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print(u"%s  %s  " % (action.group(1),movieName.group(1))),
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(u"%s  %s  " % (action.group(1),movieName.group(1))),
                f.seek(0)
            if haveStars():
                print(stars.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(stars.group(1))
                    f.write('\n')
                    f.seek(0)
            print(Img.group(1))
            with open('douban2.txt', 'a', encoding='utf-8') as f:
                f.write(Img.group(1))
                f.write('\n')
                f.seek(0)
            if haveSayMovie():
                sayMovie = re.search('<p>(.*)</p>.*?</p>', broadcast, re.S)
                print(sayMovie.group(1))
                with open('douban2.txt','a',encoding='utf-8') as f:
                    f.write(sayMovie.group(1))
                    f.write('\n')
                    f.seek(0)
                print('')

        elif book():#书籍相关
            times = re.findall('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
            bookName = re.search('<a\shref.*?blank.*?>(.*?)</a>',broadcast)
            stars = re.search('<span.*?stars.*?>(.*?)</span>', broadcast)
            action = re.search('\s{6}([\u4e00-\u9fa5]{2})', broadcast)  # 想看还是看过
            Img = re.search('<img\ssrc="(.*?)"', broadcast)
            if havetimes():
                print(times[0])
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print(u"%s  %s  " % (action.group(1), bookName.group(1))),
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(u"%s  %s  " % (action.group(1), bookName.group(1))),
                f.seek(0)
            if haveStars():
                print(stars.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(stars.group(1))
                    f.write('\n')
                    f.seek(0)
            print(Img.group(1))
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(Img.group(1))
                f.write('\n')
                f.seek(0)
            if haveSayBook():
                sayBook = re.search('<p>(.*)</p>', broadcast)
                print(sayBook.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(sayBook.group(1))
                    f.write('\n')
                    f.seek(0)
            print('')

        elif music():#音乐相关
            times = re.findall('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
            musicName = re.search('<a\shref.*?blank.*?>(.*?)</a>', broadcast)
            stars = re.search('<span.*?stars.*?>(.*?)</span>', broadcast)
            action = re.search('\s{6}([\u4e00-\u9fa5]{2})', broadcast)  # 想看还是看过
            Img = re.search('<img\ssrc="(.*?)"', broadcast)
            if havetimes():
                print(times[0])
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print(u"%s  %s  " % (action.group(1), musicName.group(1))),
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(u"%s  %s  " % (action.group(1), musicName.group(1))),
                f.seek(0)
            if haveStars():
                print(stars.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(stars.group(1))
                    f.write('\n')
                    f.seek(0)
            print(Img.group(1))
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(Img.group(1))
                f.write('\n')
                f.seek(0)
            if haveSayMusic():
                sayMusic = re.search('<p>(.*)</p>', broadcast)
                print(sayMusic.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(sayMusic.group(1))
                    f.write('\n')
                    f.seek(0)
            print('')

        elif doulist():#豆列
            times = re.search('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
            doulistName1 = re.search('<a\shref.*?doulist.*?blank.*?>(.*?)</a>', broadcast)
            doulistName2 = re.search('<a\shref.*?book.*?blank.*?>(.*?)</a>', broadcast)
            Img = re.search('<img\ssrc="(.*?)"', broadcast)
            if havetimes():
                print(times)
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print(u"向豆列 %s 中添加 " %  doulistName1.group(1)),
            print(doulistName2.group(1))
            print(Img.group(1))
            with open('douban2.txt','a',encoding='utf-8') as f:
                f.write(u"向豆列 %s 中添加 " %  doulistName1.group(1)),
                f.write(doulistName2.group(1))
                f.write('\n')
                f.write(Img.group(1))
                f.write('\n')
                f.seek(0)
            if haveSaydoulit():
                Saydoulit = re.search('<p>(.*)</p>', broadcast)
                print(Saydoulit.group(1))
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(Saydoulit.group(1))
                    f.write('\n')
                    f.seek(0)
            print('')

        else:#其实内容
            times = re.search('\d{4}\S\d{2}\S\d{2}\s\S{8}', broadcast)
            if havetimes():
                print(times)
                with open('douban2.txt', 'a', encoding='utf-8') as f:
                    f.write(times[0])
                    f.write('\n')
                    f.seek(0)
            print("这条广播没有关于「电影」、「豆列」、「书籍」、「音乐」的信息，因此没有获取\n",
                  "主要是因为作者的豆瓣广播只有上述的信息")
            with open('douban2.txt', 'a', encoding='utf-8') as f:
                f.write(u"这条广播没有关于「电影」、「豆列」、「书籍」、「音乐」的信息，因此没有获取。\n主要是因为作者的豆瓣广播只有上述的信息")
                f.write('\n')
                f.seek(0)

        print("-----------------------分隔线-----------------------------")
        print('')
        with open('douban2.txt', 'a', encoding='utf-8') as f:
            f.write('\n')
            f.write("-----------------------分隔线-----------------------------")
            f.write('\n')
            f.write('\n')
            f.seek(0)

#启动前清除历史数据
with open('douban2.txt','wt') as f:
    f.write("If you see a garbled file,make sure the file is encoded as utf-8.")
    f.write('\n')
    f.write('\n')
    f.seek(0)

#备份前1000页
for i in range(1,1000):
    page = i
    getData(page)

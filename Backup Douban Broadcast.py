#!/usr/bin/python3

from lxml import etree
import requests



#伪装用户数据，用户，cookie
headers = {
    'Uesr-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Cookie':'bid=HcniJSwDgjY; ll="118283"; _ga=GA1.2.698252912.1506060945; gr_user_id=55fea3dd-29ed-4f19-adbb-be056d20662f; __utmv=30149280.6427; _vwo_uuid_v2=FA20618BAACC1327F063B0F50F109092|69489e373a1268fa58eacb69817156a2; push_doumail_num=0; push_noty_num=0; viewed="26462816"; ap=1; __utmz=30149280.1526636126.83.43.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1526725684%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.698252912.1506060945.1526712868.1526725684.87; __utmt=1; ct=y; ps=y; _gid=GA1.2.275010010.1526725718; dbcl2="64279887:th80Ti3tLTY"; ck=bmyo; _pk_id.100001.8cb4=e7e1a240646f34ee.1506738033.104.1526726175.1526712868.; __utmb=30149280.6.10.1526725684'
}

#获取网页数据，解析为html
def getWeb(page):
    url = 'https://www.douban.com/people/yekingyan/statuses?p=%s' % page
    webData = requests.get(url,headers=headers).text
    s = etree.HTML(webData)

#用lxml获得豆瓣广播，时间
    says = s.xpath('//*[@id="content"]/div/div[1]/div[3]/div/div/div/div[2]/div[1]/blockquote/p/text()')
    times = s.xpath('//*[@id="content"]/div/div[1]/div[3]/div/div/div/div[2]/div[2]/span/@title')
    for (time,say) in zip(times,says):
        print(time)
        print(say)
        print('')

        #写入文件,如果
        with open('douban.txt','a',encoding='utf-8') as f:
            f.write(time)
            f.write('\n')
            f.write(say)
            f.write('\n')
            f.write('\n')
            f.seek(0)


#启动前清除历史数据
print("If you see a garbled file,make sure the file is encoded as utf-8.")
with open('douban.txt','wt') as f:
    f.seek(0)

#控制页数循环
pageNumber = int(input(u'请输入要备份的页数（前几页）：'))
pageNumber += 1
for i in range(1,pageNumber):
    getWeb(i)



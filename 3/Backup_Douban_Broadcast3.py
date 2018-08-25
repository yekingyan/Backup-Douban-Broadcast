import requests
from pyquery import PyQuery
import os
import json
import time
import random
import shutil


def headers(url):
    """
    豆瓣的request_header
    cookie之外要加上Referer才能获取status内容
    """
    header = {
        "User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36',
        "Cookie": 'bid=wafndqFvNNI; ps=y; dbcl2="64279887:DA7ClPtz04c"; ck=2fyn; ap_v=1,6.0; push_noty_num=0; push_doumail_num=0; __utma=30149280.96424992.1534848101.1534848101.1534848101.1; __utmc=30149280; __utmz=30149280.1534848101.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmv=30149280.6427; __utmb=30149280.4.10.1534848101',
        "Referer": f'{url}',
    }
    return header


class Model(object):
    """打印显示类属性的信息"""

    def __repr__(self):
        name = self.__class__.__name__
        properties = (f'{k}=({v})' for k, v in self.__dict__.items())
        string = '\n '.join(properties)
        s = f'\n<{name} \n {string}>'
        return s


class Status(Model):
    """每条状态的共有属性"""

    def __init__(self):
        self.time = ''
        self.action = ''
        self.quote = ''


class Content(Status):
    """
    书、电影、音乐等多出一个content属性
    拆分如下
    """

    def __init__(self):
        Status.__init__(self)
        self.title = ''
        self.info = ''
        self.img = ''


def page_nums():
    """备分数量级"""
    print("备份页面的数量级是？百页内请输入数字2，千页内请输入数字3，以此类推。")
    print("请输入：")
    n = input()
    # s = "0" * n
    s = [i for i in n]
    print(s)
    pass


def cashed_page(url):
    """
    下载页面，写入cached目录内,返回html数据
    保存的文件具有时效性，因为页数url的内容随增长而变动
    """
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)

    # 如果没有'cached'目录则创建
    if not os.path.exists(folder):
        os.makedirs(folder)
    # 写入数据
    s = requests.session().get(url, headers=headers(url))
    r = s.content
    # print(str(r))

    # 已下载则直接读出，数据有时效性
    if os.path.exists(path):
        with open(path, 'rb') as f:
            f.read()
            print(f"{path}从cached中读出")
        return r

    # 判断Html页面没有new-status类则不保存
    elif 'class="new-status' in str(r) is not None:
        with open(path, 'wb') as f:
            f.write(r)
            # Todo 时间控制，防封
            time.sleep(2)
            print(f"{path}已写入cached")
        return r
    else:
        print("内容下载完成")
        return 'break'


def get_status(div):
    """普通广播"""
    e = PyQuery(div)

    m = Status()
    m.time = e('.created_at').attr('title')
    m.action = e('.status-item').find('.text').text().split('\n', 2)[0].split(' ')[1]
    m.quote = e('blockquote').text()
    return m


def get_content(div):
    """书、电影、音乐"""
    e = PyQuery(div)

    m = Content()
    m.time = e('.created_at').attr('title')
    m.action = e('.status-item').find('.text').text().split('\n', 2)[0].split(' ')[1]
    m.quote = e('blockquote').text()

    m.title = e('.title').text().split(' ')[0]
    m.info = e('.info').text()

    m.img = str(e('.pic'))
    # print('b if', (m.img,))
    if m.img is not '':
        m.img = str(e('.pic')).split('src="')[1].split('"')[0]
    # print('m', m.title, (m.img,))

    return m


def status(url):
    """返回每一页含数据的列表，
    分为两个列表
    s1 普通
    s2 书、电影等等
    """
    # 最终用于auto()的循环停止
    page = cashed_page(url)
    if page == 'break':
        # print("status == break")
        return 'break'

    e = PyQuery(page)
    # 每个class="item"是一部电影
    items = e('.status-item')

    # # print(items)
    # for i in items:
    #     print('sns' in i.values())
    # print(dir(items))
    """
    ['__bool__', '__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_init', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'base_url', 'body', 'classes', 'clear', 'cssselect', 'drop_tag', 'drop_tree', 'extend', 'find', 'find_class', 'find_rel_links', 'findall', 'findtext', 'forms', 'get', 'get_element_by_id', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'head', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'iterlinks', 'itersiblings', 'itertext', 'keys', 'label', 'make_links_absolute', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'resolve_base_href', 'rewrite_links', 'set', 'sourceline', 'tag', 'tail', 'text', 'text_content', 'values', 'xpath']
    """

    # 分成两个列表,普通广播是有'sns'
    s1 = [get_status(i) for i in items if 'sns' in i.values()]
    s2 = [get_content(i) for i in items if 'sns' not in i.values()]
    # for i in s2:
    #     print(i)
    # s = s1 + s2
    # print(s)
    return s1, s2


def int_time(str_time):
    """str 2016-06-01 15:27:22
        转为
       int 20160601152722
    """
    # 没的捕找到时间就key为[0,1)的随机数
    if str_time is None:
        return random.random()

    else:
        t = str_time.split(' ')
        t = t[0] + t[1]
        t = t.split('-')
        t = t[0] + t[1] + t[2]
        t = t.split(':')
        t = t[0] + t[1] + t[2]
        times = int(t)
        # print(time)
        return times


def json_status(url):
    """
    保存为'dd.txt'的json文件
    时间为key
    """

    if status(url) == 'break':
        # 用于停止auto()的循环
        return 'break'
    else:
        s1, s2 = status(url)

    # 转成字典
    dict_status = {}
    # 表s1
    for d in s1:
        # print('s1', d.time)
        t = int_time(d.time)
        # print(t)
        dict_status[t] = {
            'time': d.time,
            'action': d.action,
            'quote': d.quote,
        }
    # 表s2
    for d in s2:
        # print('s2', d.time)
        t = int_time(d.time)
        # print(t)
        dict_status[t] = {
            'time': d.time,
            'action': d.action,
            'quote': d.quote,
            'title': d.title,
            'info': d.info,
            'img': d.img,
        }
    # print(dict_status)

    # 追加写入json文件
    j = json.dumps(dict_status, indent=4, ensure_ascii=False)
    # print(j)
    with open('status.txt', 'a', encoding='utf-8') as f:
        f.write(j)


def auto(func):
    """
    配合cashed_page()使用
    当下载到无内容页面时停止
    """
    n, s = 1, 1
    while s != 'break':
        url = f"https://www.douban.com/people/yekingyan/statuses?p={n}"
        s = func(url)
        # print(s)
        n += 1


def main():
    # 启动前清除旧数据
    if os.path.exists('status.txt'):
        os.remove('status.txt')

    # 时间久了，清除旧的html
    # if os.path.exists('cached'):
    #     shutil.rmtree('cached')

    url = "https://www.douban.com/people/yekingyan/statuses?p=32"

    auto(json_status)
    # json_status(url)
    # cashed_page(url)
    # status(url)
    # auto(print)


if __name__ == '__main__':
    main()

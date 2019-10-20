import requests
import re
from lxml import etree
import os
import time


def get_html():
    headers = {}
    '''提供访问方式,包含操作系统,cpu,浏览器等,服务器会根据User_Agent返回不同的界面'''
    headers['User_Agent'] = 'Mozilla/5.0 (Windows NT 10.0;' \
                            ' Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/76.0.3809.132 Safari/537.36'
    '''url代表网址'''
    url = 'http://www.xbiquge.la/15/15021/'
    '''content中间存的是字节码，而text中存的是Beautifulsoup根据猜测的编码方式将content内容编码成字符串,使用.decode()将其按照既定格式的编码返回html'''
    html = requests.get(url, headers=headers).content.decode('utf-8')
    return html


def get_novel_url(html):
    '''正则表达式解析html'''
    path2 = r"<dd><a href='(.*?)' >(.*?)</a></dd>"
    '''re.findall() 函数可以遍历匹配，可以获取字符串中所有匹配的字符串，返回一个列表,参数一是正则表达式,参数二是查找的字符串,path2带()的即为返回的内容'''
    title_name = re.findall(path2, html)
    path = 'G:/剑来'
    if not os.path.exists(path):
        os.makedirs(path)
    filename = path + '/' + '{}.txt'.format('剑来')
    '''没有文档就创建一个'''
    open(filename, 'w', encoding='utf-8')
    for title in title_name:
        '''title[0]:章节地址;title[1]:章节名'''
        novel_url = title[0]
        novel_name = title[1]
        newUrl = r'http://www.xbiquge.la' + novel_url

        response = requests.get(newUrl).content.decode('utf-8', 'ignore')
        '''tree.HTML():构造了一个XPath解析对象并对HTML文本进行自动修正'''
        response = etree.HTML(response)
        content = response.xpath('//*[@id="content"]/text()')
        try:
            print("正在下载小说----->%s" % novel_name)
            '''filename = path + '/' + '剑来.txt'
            filename = path + '/' + '{}.txt'.format(novel_name)'''
            with open(filename, 'a+', encoding='utf-8') as f:
                f.writelines(novel_name+'\n'+'\n')
                f.writelines(content)
                time.sleep(1)
        except Exception as e:
            print("下载出错", e)


def main():
    html = get_html()
    get_novel_url(html)


if __name__ == '__main__':
    main()

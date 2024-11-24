import requests
from lxml import etree
import re
import os
import threading
from PyQt5.QtGui import QTextCursor
pool=threading.BoundedSemaphore(1)
lastx=0
class check_time:
    def __init__(self,p_time):
        self.p_time=p_time
    def check(self,q_time):
        flag=False
        if q_time-self.p_time>0.2:
            flag=not flag
        self.p_time=q_time
        return flag
def get_max_e(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.content)
    max_e=0
    title=re.findall('《.*?》',html.xpath('/html/head/title/text()')[0])[0]
    i=0
    while True:
        i+=1
        try:
            e=int(html.xpath(f'//*[@id="hl-plays-list"]/li[{i}]/a/@href')[0].split('/')[-1].split('.')[0].split('-')[-1])
        except:
            max_e=e
            break
    return max_e+1,title
def get_video(url,title,min_e,i,textbrowser,cursor):
    global lastx
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    res=requests.get(url,headers=headers,stream=True)
    size=int(res.headers['Content-Length'])//(2**20*10)
    j=1
    f=open(f'ans/{title}/第{min_e+i}集.mp4','wb')
    textbrowser.append(f'下载进度0%');lastx=0
    for data in res.iter_content(chunk_size=2**20*10):
        f.write(data)
        x=j*100//size
        if x<100 and data:
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(str(lastx))+1)
            cursor.removeSelectedText()
            cursor.insertText(f'{x}%')
            textbrowser.setTextCursor(cursor)
            lastx=x
        j+=1
    f.close()
    cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(str(lastx))+6)
    cursor.removeSelectedText()
    textbrowser.setTextCursor(cursor)
    cursor.insertHtml(f'<br>第{min_e+i}集下载完成')
def get_video_list(urls,title,min_e):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    ts=[]
    def get_video(i):
        if urls[i]!=0:
            res=requests.get(urls[i],headers=headers)
            with open(f'ans/{title}/第{min_e+i}集.mp4','wb') as f:
                f.write(res.content)
        pool.release()
    for i in range(len(urls)):
        a=threading.Thread(target=get_video,args=(i,))
        pool.acquire()
        ts.append(a)
        a.start()
    for t in ts:
        t.join()
def get_base_url(s,page):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }   
    url=f'https://www.295yhw.com/search/{s}----------{page}---.html'
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.content)
    i=0
    res=[]
    while True:
        i+=1
        try:
            url=html.xpath(f'//*[@id="conch-content"]/div/div[2]/div/div/div[1]/div/div[2]/div/ul[1]/li[{i}]/div/div/div[2]/div[1]/a/@href')[0]
            title=html.xpath(f'//*[@id="conch-content"]/div/div[2]/div/div/div[1]/div/div[2]/div/ul[1]/li[{i}]/div/div/div[2]/div[1]/a/text()')[0]
            res.append((f'https://www.295yhw.com/{url}',title))
        except:
            break
    return res
def update(title):
    i=1
    current_path = os.path.abspath(__file__)
    parent_path = os.path.dirname(os.path.dirname(current_path))
    while os.path.exists(fr'{parent_path}/ans/{title}/第{i}集.mp4'):
        i+=1
    return i
import requests
from lxml import etree
import re
import os
import threading
from PyQt5.QtGui import QTextCursor
pool=threading.BoundedSemaphore(1)
lastx=0
class check_time:
    def __init__(self,p_time):
        self.p_time=p_time
    def check(self,q_time):
        flag=False
        if q_time-self.p_time>0.2:
            flag=not flag
        self.p_time=q_time
        return flag
def get_max_e(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.content)
    max_e=0
    title=re.findall('《.*?》',html.xpath('/html/head/title/text()')[0])[0]
    i=0
    while True:
        i+=1
        try:
            e=int(html.xpath(f'//*[@id="hl-plays-list"]/li[{i}]/a/@href')[0].split('/')[-1].split('.')[0].split('-')[-1])
        except:
            max_e=e
            break
    return max_e+1,title
def get_video(url,title,min_e,i,textbrowser,cursor):
    global lastx
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "connection": "keep-alive",
    "host": "v16m-default.akamaized.net",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    res=requests.get(url,headers=headers,stream=True)
    size=int(res.headers['Content-Length'])//(2**20*10)
    j=1
    f=open(f'ans/{title}/第{min_e+i}集.mp4','wb')
    textbrowser.append(f'下载进度0%');lastx=0
    for data in res.iter_content(chunk_size=2**20*10):
        f.write(data)
        x=j*100//size
        if x<100:
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(str(lastx))+1)
            cursor.removeSelectedText()
            cursor.insertText(f'{x}%')
            textbrowser.setTextCursor(cursor)
            lastx=x
        j+=1
    f.close()
    cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(str(lastx))+6)
    cursor.removeSelectedText()
    textbrowser.setTextCursor(cursor)
    cursor.insertHtml(f'<br>第{min_e+i}集下载完成')
def get_video_list(urls,title,min_e):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    ts=[]
    def get_video(i):
        if urls[i]!=0:
            res=requests.get(urls[i],headers=headers)
            with open(f'ans/{title}/第{min_e+i}集.mp4','wb') as f:
                f.write(res.content)
        pool.release()
    for i in range(len(urls)):
        a=threading.Thread(target=get_video,args=(i,))
        pool.acquire()
        ts.append(a)
        a.start()
    for t in ts:
        t.join()
def get_base_url(s,page):
    headers = {
    #"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #"accept-encoding": "gzip, deflate, br, zstd",
    #"accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    #"cookie": "tips=ok; PHPSESSID=p1vnotjm94134pr4r9mkpjhatn",
    #"priority": "u=0, i",
    #"sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    #"sec-ch-ua-mobile": "?0",
    #"sec-ch-ua-platform": "\"Windows\"",
    #"sec-fetch-dest": "document",
    #"sec-fetch-mode": "navigate",
    #"sec-fetch-site": "same-origin",
    #"sec-fetch-user": "?1",
    #"upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }   
    url=f'https://www.295yhw.com/search/{s}----------{page}---.html'
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.content)
    i=0
    res=[]
    while True:
        i+=1
        try:
            url=html.xpath(f'//*[@id="conch-content"]/div/div[2]/div/div/div[1]/div/div[2]/div/ul[1]/li[{i}]/div/div/div[2]/div[1]/a/@href')[0]
            title=html.xpath(f'//*[@id="conch-content"]/div/div[2]/div/div/div[1]/div/div[2]/div/ul[1]/li[{i}]/div/div/div[2]/div[1]/a/text()')[0]
            res.append((f'https://www.295yhw.com/{url}',title))
        except:
            break
    return res
def update(title):
    i=1
    current_path = os.path.abspath(__file__)
    parent_path = os.path.dirname(os.path.dirname(current_path))
    while os.path.exists(fr'{parent_path}/ans/{title}/第{i}集.mp4'):
        i+=1
    return i
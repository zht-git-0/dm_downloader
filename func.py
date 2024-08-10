import requests
from lxml import etree
import re
import os
import threading
pool=threading.BoundedSemaphore(5)
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
def print_list(lis):
    print('[')
    for i in range(len(lis)):
        print(f"'{lis[i]}'")
    print(']')
def get_video_list(urls,title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    ts=[]
    def get_video(i):
        res=requests.get(urls[i],headers=headers)
        with open(f'ans/{title}/第{i+1}集.mp4','wb') as f:
            f.write(res.content)
        pool.release()
    for i in range(len(urls)):
        a=threading.Thread(target=get_video,args=(i,))
        ts.append(a)
        a.start()
        pool.acquire()
    for t in ts:
        t.join()
def get_base_url(s):
    headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cookie": "tips=ok; PHPSESSID=p1vnotjm94134pr4r9mkpjhatn",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }   
    url=f'https://www.295yhw.com/search/{s}----------1---.html'
    res=requests.get(url,headers=headers)
    with open('1.html','wb') as f:
        f.write(res.content)
    html=etree.HTML(res.content)
    with open('1.html','wb') as f:
        f.write(res.content)
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
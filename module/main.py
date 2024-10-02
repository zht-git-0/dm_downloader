from playwright.sync_api import sync_playwright
from .func import *
from time import time,sleep

flag = check_time(time())

def download_video(base_url, textbrowser,cursor):
    if not flag.check(time()):
        return
    
    p_id = base_url.split('/')[-1].split('.')[0]
    e, title = get_max_e(base_url)
    min_e = update(title)
    textbrowser.append(f"开始下载{title}<br>已存在{min_e-1}集,还需下载{e-min_e}集")
    target_url = "https://v16m-default.akamaized.net/"
    video_urls = [0 for _ in range(min_e - 1, e - 1)]
    
    def fetch_url(url, context, i):
        page = context.new_page()
        page.set_default_timeout(600000)
        
        def on_response(response):
            if target_url in response.url:
                video_urls[i] = response.url
                textbrowser.append(f"获取{title}第{min_e + i}集链接:<br><a href='{response.url}'>{response.url}</a> ")
                page.close()
                get_video(response.url, title, min_e,i, textbrowser,cursor)
        
        page.on('response', on_response)
        
        try:
            page.goto(url)
            page.wait_for_timeout(600000)
        except:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        urls = [f"https://www.295yhw.com/play/{p_id}-1-{i}.html" for i in range(min_e, e)]
        for i, url in enumerate(urls):
            fetch_url(url, context, i)
        
        context.close()
        browser.close()
    sleep(0.01)
    textbrowser.append(f"下载完成{title}")

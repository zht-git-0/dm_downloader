from playwright.sync_api import sync_playwright
from .func import *
from time import time,sleep
import os
baseurl='https://www.295yhw.com'
# 在文件开头添加配置
#proxy_config = {
#    "server": "http://180.120.209.27:8089",  # 必填项，支持协议头 http:// / socks5://
#}
BROWSER_PATH = os.path.join(os.path.dirname(__file__), "pw", "chromium-1129", "chrome-win", "chrome.exe")
flag = check_time(time())

def download_video(base_url, textbrowser,cursor):
    if not flag.check(time()):
        return
    
    try:
        p_id = base_url.split('/')[-1].split('.')[0]
        e, title = get_max_e(base_url)
        min_e = update(title)
        if min_e == e:
            textbrowser.append(f"下载完成{title}")
            return
        textbrowser.append(f"开始下载{title}<br>已存在{min_e-1}集,还需下载{e-min_e}集")
        target_url = "https://v16-tiktokcdn-com.akamaized.net/"
        video_urls = [0 for _ in range(min_e - 1, e - 1)]
        
        def fetch_url(url, context, i):
            page = None
            try:
                page = context.new_page()
                page.set_default_timeout(60000)  # 设置合理的超时时间为60秒
                
                def on_response(response):
                    try:
                        if target_url in response.url:
                            video_urls[i] = response.url
                            textbrowser.append(f"获取{title}第{min_e + i}集链接成功")
                            get_video(response.url, title, min_e, i, textbrowser, cursor)
                            if page:
                                page.close()
                        elif "index.m3u8" in response.url:
                            video_urls[i] = response.url
                            textbrowser.append(f"获取{title}第{min_e + i}集m3u8链接成功")
                            get_m3u8_video(response.url, title, min_e, i, textbrowser, cursor)
                            if page:
                                page.close()
                    except Exception as e:
                        textbrowser.append(f"处理响应错误: {str(e)}")
                        if page:
                            page.close()
                
                page.on('response', on_response)
                
                try:
                    textbrowser.append(f"正在加载第{min_e + i}集页面...")
                    page.goto(url, wait_until='networkidle')
                    page.reload()  # 刷新页面
                    page.wait_for_timeout(5000)  # 设置合理的等待时间为5秒
                except Exception as e:
                    textbrowser.append(f"第{min_e + i}集页面加载失败: {str(e)}")
            except Exception as e:
                textbrowser.append(f"第{min_e + i}集页面创建失败: {str(e)}")
            finally:
                if page:
                    try:
                        page.close()
                    except:
                        pass

        with sync_playwright() as p:
            browser = None
            context = None
            try:
                browser = p.chromium.launch(
                    headless=True,  # 使用无头模式，减少资源占用和UI问题
                    executable_path=BROWSER_PATH,
                    args=[
                        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
                        '--disable-blink-features=AutomationControlled',
                        '--no-first-run',
                        '--disable-gpu',
                        '--no-sandbox'
                    ]
                )
                context = browser.new_context(
                    viewport={'width': 1280, 'height': 720},
                    java_script_enabled=True
                )
                urls = [f"{baseurl}/play/{p_id}-2-{i}.html" for i in range(min_e, e)]
                
                for i, url in enumerate(urls):
                    try:
                        fetch_url(url, context, i)
                        sleep(1)  # 添加延迟，避免过快请求
                    except Exception as e:
                        textbrowser.append(f"下载第{min_e + i}集失败: {str(e)}")
                        continue
                        
            except Exception as e:
                textbrowser.append(f"浏览器启动失败: {str(e)}")
                return
            finally:
                # 确保资源被正确释放
                if context:
                    try:
                        context.close()
                    except:
                        pass
                if browser:
                    try:
                        browser.close()
                    except:
                        pass
                
    except Exception as e:
        textbrowser.append(f"下载过程错误: {str(e)}")
    
    textbrowser.append(f"下载完成{title}")

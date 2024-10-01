from playwright.async_api import async_playwright
from .func import *
import asyncio
def download_video(base_url):
    p_id=base_url.split('/')[-1].split('.')[0]
    e,title=get_max_e(base_url)
    min_e=update(title)
    print(min_e,e)
    target_url = "https://v16m-default.akamaized.net/"
    video_urls = [0 for i in range(min_e-1,e-1)]
    async def fetch_url(url, context,i):
        page = await context.new_page()  
        page.set_default_timeout(600000)
        async def on_response(response):
            if target_url in response.url:
                video_urls[i]=response.url
                await page.close()
        page.on('response', on_response)
        try:await page.goto(url);await page.wait_for_timeout(600000)
        except:None
    async def main():  
        async with async_playwright() as p:    
            browser = await p.chromium.launch(headless=True)  
            context = await browser.new_context()  # 共享上下文
            urls = [f"https://www.295yhw.com/play/{p_id}-1-{i}.html" for i in range(min_e,e)]
            tasks = [fetch_url(urls[i],context,i) for i in range(len(urls))] 
            await asyncio.gather(*tasks)
            await context.close()  # 在所有任务完成后关闭上下文
            await browser.close()
    asyncio.run(main())
    get_video_list(video_urls,title,min_e)
    print(title+"下载完成")
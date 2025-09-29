import requests
from lxml import etree
import re
import os
import threading
import requests
from lxml import etree
from PyQt5.QtGui import QTextCursor
from time import time
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
    try:
        res=requests.get(url,headers=headers,timeout=10)
        res.raise_for_status()
        html=etree.HTML(res.content)
        max_e=0
        title_elements = html.xpath('/html/head/title/text()')
        if not title_elements:
            raise ValueError("无法获取页面标题")
        title_match = re.findall('《.*?》', title_elements[0])
        if not title_match:
            raise ValueError("无法提取标题")
        title = title_match[0]
        
        i=0
        while True:
            i+=1
            try:
                href = html.xpath(f'//*[@id="hl-plays-list"]/li[{i}]/a/@href')
                if not href:
                    break
                e=int(href[0].split('/')[-1].split('.')[0].split('-')[-1])
                max_e = e
            except (IndexError, ValueError):
                break
        
        if max_e == 0:
            raise ValueError("无法获取剧集信息")
            
        return max_e+1,title
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求错误: {str(e)}")
    except Exception as e:
        raise Exception(f"解析页面错误: {str(e)}")
def get_video(url,title,min_e,i,textbrowser,cursor):
    global lastx
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    
    file_path = f'ans/{title}/第{min_e+i}集.mp4'
    temp_file_path = f'{file_path}.tmp'
    
    # 检查是否存在临时文件或完整文件
    downloaded_size = 0
    if os.path.exists(temp_file_path):
        downloaded_size = os.path.getsize(temp_file_path)
        file_mode = 'ab'  # 追加模式继续下载
    elif os.path.exists(file_path):
        # 文件已完整下载，跳过
        textbrowser.append(f'第{min_e+i}集已存在，跳过下载')
        return
    else:
        file_mode = 'wb'  # 新建文件下载
    
    # 获取文件总大小
    if downloaded_size > 0:
        headers['Range'] = f'bytes={downloaded_size}-'
    
    try:
        res = requests.get(url, headers=headers, stream=True, timeout=60)
        res.raise_for_status()  # 检查HTTP错误
        
        content_length = res.headers.get('Content-Length')
        if content_length:
            total_size = int(content_length) + downloaded_size
        else:
            total_size = 0
        
        # 如果支持断点续传
        if 'content-range' in res.headers:
            content_range = res.headers['content-range']
            try:
                total_size = int(content_range.split('/')[-1])
            except (ValueError, IndexError):
                total_size = 0
        
        if total_size == 0:
            # 无法获取文件大小，使用默认块大小
            total_size = 100 * 1024 * 1024  # 默认100MB
        
        chunk_size = 2**20 * 5  # 减小到5MB，避免内存问题
        
        # 使用临时文件下载
        with open(temp_file_path, file_mode) as f:
            if downloaded_size == 0:
                textbrowser.append(f'第{min_e+i}集 开始下载...')
                lastx = 0
            else:
                if total_size > 0:
                    progress = int((downloaded_size / total_size) * 100)
                    textbrowser.append(f'第{min_e+i}集 继续下载，当前进度{progress}%')
                    lastx = progress
                else:
                    textbrowser.append(f'第{min_e+i}集 继续下载，已下载{downloaded_size//1024//1024}MB')
                    lastx = 0
            
            downloaded = downloaded_size
            last_update_time = time()
            timeout_counter = 0
            for chunk_num, data in enumerate(res.iter_content(chunk_size=chunk_size)):
                if data:
                    f.write(data)
                    downloaded += len(data)
                    timeout_counter = 0  # 重置超时计数器
                    
                    # 每2秒更新一次进度，避免过于频繁
                    current_time = time()
                    if current_time - last_update_time >= 2:
                        try:
                            if total_size > 0:
                                progress = min((downloaded / total_size) * 100, 100.0)
                            else:
                                progress = 0.0
                            
                            # 只有当进度有变化时才更新
                            if int(progress) != int(lastx):
                                textbrowser.append(f'第{min_e+i}集 下载进度: {progress:.1f}% ({downloaded//1024//1024}MB)')
                                lastx = progress
                            last_update_time = current_time
                        except Exception:
                            pass  # 忽略UI更新错误
                else:
                    # 如果连续5次没有数据，则认为下载超时
                    timeout_counter += 1
                    if timeout_counter >= 5:
                        textbrowser.append(f'第{min_e+i}集 下载超时，已保存进度')
                        break
        
        # 验证文件完整性
        try:
            final_size = os.path.getsize(temp_file_path)
            if final_size >= total_size or total_size == 0:
                # 下载完成，重命名临时文件
                if os.path.exists(temp_file_path):
                    os.rename(temp_file_path, file_path)
                textbrowser.append(f'第{min_e+i}集 下载完成')
            else:
                textbrowser.append(f'第{min_e+i}集 下载未完成，已保存进度({final_size}/{total_size})')
        except OSError as e:
            textbrowser.append(f'第{min_e+i}集 文件验证错误: {str(e)}')
            
    except requests.exceptions.RequestException as e:
        textbrowser.append(f'第{min_e+i}集 网络错误: {str(e)}')
    except IOError as e:
        textbrowser.append(f'第{min_e+i}集 文件错误: {str(e)}')
    except Exception as e:
        textbrowser.append(f'第{min_e+i}集 下载错误: {str(e)}')

def get_m3u8_video(url,title,min_e,i,textbrowser,cursor):
    global lastx
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }
    os.makedirs(f'ans/{title}',exist_ok=True)
    
    file_path = f'ans/{title}/第{min_e+i}集.mp4'
    temp_file_path = f'{file_path}.tmp'
    ts_dir = f'ans/{title}/第{min_e+i}集_ts'
    
    # 检查是否存在完整文件
    if os.path.exists(file_path):
        # 文件已完整下载，跳过
        textbrowser.append(f'第{min_e+i}集已存在，跳过下载')
        return
    
    # 创建临时目录存放ts片段
    os.makedirs(ts_dir, exist_ok=True)
    
    try:
        # 获取m3u8文件内容
        textbrowser.append(f'第{min_e+i}集 正在解析m3u8文件...')
        res = requests.get(url, headers=headers, timeout=60)
        res.raise_for_status()
        
        # 解析m3u8文件，获取ts片段列表或子m3u8列表
        m3u8_content = res.text
        ts_urls = []
        sub_m3u8_urls = []
        base_url = url.rsplit('/', 1)[0] + '/'  # 获取基础URL
        
        for line in m3u8_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                if line.endswith('.m3u8'):
                    # 子m3u8文件
                    if line.startswith('http'):
                        sub_m3u8_urls.append(line)
                    else:
                        sub_m3u8_urls.append(base_url + line)
                else:
                    # ts片段
                    if line.startswith('http'):
                        ts_urls.append(line)
                    else:
                        ts_urls.append(base_url + line)
        
        # 如果有子m3u8文件，选择第一个（通常是最高分辨率）并解析
        if sub_m3u8_urls:
            textbrowser.append(f'第{min_e+i}集 发现子m3u8文件，正在解析...')
            sub_m3u8_url = sub_m3u8_urls[0]  # 默认选择第一个子m3u8
            sub_res = requests.get(sub_m3u8_url, headers=headers, timeout=60)
            sub_res.raise_for_status()
            
            # 解析子m3u8文件
            sub_m3u8_content = sub_res.text
            ts_urls = []  # 重置ts_urls
            sub_base_url = sub_m3u8_url.rsplit('/', 1)[0] + '/'  # 获取子m3u8的基础URL
            
            for line in sub_m3u8_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('http'):
                        ts_urls.append(line)
                    else:
                        ts_urls.append(sub_base_url + line)
        
        if not ts_urls:
            raise ValueError("无法从m3u8文件中解析出视频片段")
        
        textbrowser.append(f'第{min_e+i}集 共发现{len(ts_urls)}个视频片段，开始下载...')
        
        # 下载所有ts片段
        total_size = 0
        downloaded = 0
        last_update_time = time()
        
        # 检查已下载的ts片段
        existing_ts_files = []
        for ts_index in range(len(ts_urls)):
            ts_file = os.path.join(ts_dir, f"{ts_index:05d}.ts")
            if os.path.exists(ts_file):
                existing_ts_files.append(ts_index)
                downloaded += os.path.getsize(ts_file)
        
        # 创建线程安全的下载队列和结果列表
        from queue import Queue
        from threading import Thread, Lock
        
        # 创建锁用于线程安全地更新进度
        progress_lock = Lock()
        download_success = [True] * len(ts_urls)  # 跟踪每个片段的下载状态
        
        # 定义下载单个TS片段的函数
        def download_ts(ts_index, ts_url, ts_file):
            nonlocal downloaded
            retry_count = 0
            
            while True:  # 无限重试直到下载成功
                try:
                    ts_res = requests.get(ts_url, headers=headers, timeout=30)
                    ts_res.raise_for_status()
                    ts_data = ts_res.content
                    
                    # 验证ts数据是否有效
                    if len(ts_data) < 188 or ts_data[0] != 0x47:  # TS文件以0x47同步字节开头
                        raise ValueError("无效的TS片段数据")
                    
                    with open(ts_file, 'wb') as ts_f:
                        ts_f.write(ts_data)
                    
                    # 使用锁安全地更新下载大小
                    with progress_lock:
                        downloaded += len(ts_data)
                        download_success[ts_index] = True  # 标记下载成功
                    
                    break  # 下载成功，跳出重试循环
                    
                except Exception as e:
                    with progress_lock:
                        download_success[ts_index] = False  # 标记下载失败
                    textbrowser.append(f'第{min_e+i}集 下载片段{ts_index+1}失败，正在重试(第{retry_count}次): {str(e)}')
                    retry_count += 1
                    # 添加短暂延迟，避免过于频繁的重试
                    import time
                    time.sleep(1)
        
        # 创建并启动下载线程
        threads = []
        max_threads = 8  # 最大线程数
        
        for ts_index, ts_url in enumerate(ts_urls):
            ts_file = os.path.join(ts_dir, f"{ts_index:05d}.ts")
            
            # 如果ts文件已存在，跳过下载
            if os.path.exists(ts_file):
                continue
                
            # 创建下载线程
            thread = Thread(target=download_ts, args=(ts_index, ts_url, ts_file))
            threads.append(thread)
            thread.start()
            
            # 限制并发线程数
            if len(threads) >= max_threads:
                for t in threads:
                    t.join()
                threads = []
                
                # 更新进度
                with progress_lock:
                    progress = min((sum(1 for i in range(len(ts_urls)) if os.path.exists(os.path.join(ts_dir, f"{i:05d}.ts"))) / len(ts_urls)) * 100, 100.0)
                    if int(progress) != int(lastx):
                        textbrowser.append(f'第{min_e+i}集 下载进度: {progress:.1f}% ({downloaded//1024//1024}MB)')
                        lastx = progress
        
        # 等待所有剩余线程完成
        for thread in threads:
            thread.join()
        
        # 检查是否有片段下载失败
        failed_count = sum(1 for success in download_success if not success)
        if failed_count > 0:
            textbrowser.append(f'第{min_e+i}集 有{failed_count}个片段下载失败，视频可能不完整')
        
        # 最终进度更新
        progress = min((sum(1 for i in range(len(ts_urls)) if os.path.exists(os.path.join(ts_dir, f"{i:05d}.ts"))) / len(ts_urls)) * 100, 100.0)
        textbrowser.append(f'第{min_e+i}集 下载进度: {progress:.1f}% ({downloaded//1024//1024}MB)')
        
        # 合并ts文件为mp4
        textbrowser.append(f'第{min_e+i}集 开始合并视频片段...')
        
        # 先将所有ts文件按顺序合并为一个临时ts文件
        temp_ts_file = f'{temp_file_path}_combined.ts'
        with open(temp_ts_file, 'wb') as outfile:
            for ts_index in range(len(ts_urls)):
                ts_file = os.path.join(ts_dir, f"{ts_index:05d}.ts")
                if os.path.exists(ts_file):
                    with open(ts_file, 'rb') as infile:
                        outfile.write(infile.read())
        
        # 尝试使用ffmpeg将ts转换为mp4
        try:
            import subprocess
            ffmpeg_cmd = [
                'ffmpeg', '-i', temp_ts_file, '-c', 'copy', '-f', 'mp4', 
                '-movflags', '+faststart', temp_file_path
            ]
            textbrowser.append(f'第{min_e+i}集 正在转换为MP4格式...')
            process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                textbrowser.append(f'第{min_e+i}集 FFmpeg转换失败，使用备用方法')
                # 如果ffmpeg失败，使用原始方法
                with open(temp_file_path, 'wb') as outfile:
                    with open(temp_ts_file, 'rb') as infile:
                        outfile.write(infile.read())
            else:
                textbrowser.append(f'第{min_e+i}集 MP4格式转换成功')
                
        except (ImportError, FileNotFoundError):
            textbrowser.append(f'第{min_e+i}集 未找到FFmpeg，使用备用方法')
            # 如果没有ffmpeg，使用原始方法
            with open(temp_file_path, 'wb') as outfile:
                with open(temp_ts_file, 'rb') as infile:
                    outfile.write(infile.read())
        
        # 删除临时ts文件
        try:
            if os.path.exists(temp_ts_file):
                os.remove(temp_ts_file)
        except Exception as e:
            textbrowser.append(f'第{min_e+i}集 删除临时文件时出错: {str(e)}')
        
        # 重命名临时文件为最终文件
        if os.path.exists(temp_file_path):
            os.rename(temp_file_path, file_path)
        
        # 清理临时ts文件
        try:
            for ts_index in range(len(ts_urls)):
                ts_file = os.path.join(ts_dir, f"{ts_index:05d}.ts")
                if os.path.exists(ts_file):
                    os.remove(ts_file)
            os.rmdir(ts_dir)
        except Exception as e:
            textbrowser.append(f'第{min_e+i}集 清理临时文件时出错: {str(e)}')
        
        textbrowser.append(f'第{min_e+i}集 下载完成')
            
    except requests.exceptions.RequestException as e:
        textbrowser.append(f'第{min_e+i}集 网络错误: {str(e)}')
    except IOError as e:
        textbrowser.append(f'第{min_e+i}集 文件错误: {str(e)}')
    except Exception as e:
        textbrowser.append(f'第{min_e+i}集 下载错误: {str(e)}')
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
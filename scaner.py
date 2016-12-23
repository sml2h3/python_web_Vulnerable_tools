#coding=utf-8
import threading
import Queue
import importlib
import ConfigParser
#导入日志记录类
from logger import Logger
from collections import defaultdict
#导入线程池模块
import threadpool
#exp&poc模块导入处

#exp&poc模块导入结束


logger = Logger('collect.py')


class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        inqueue()


def inqueue():
    global urlListQueue
    global fr
    global urlNum
    while True:
        url = fr.readline()
        if url:
            urlNum = urlNum + 1
            urlListQueue.put(url)
        else:
            logger.info("当前URL文档已经全部导入处理队列中,共计导入域名" + str(urlNum) + "个，导入线程已退出")
            break

def loadplugins():
    # 读取ini配置项
    global Auto_modules
    global Modules_list
    global Finger_list
    logger.info("加载插件配置中...")
    config = ConfigParser.ConfigParser()
    config.read('plugins.ini')
    Auto_modules = config.items("Exp")
    for mod in Auto_modules:
        test = importlib.import_module(mod[1])
        Modules_list[mod[0]].append(getattr(test, mod[0])())
        Finger_list.append(getattr(test, mod[0])())
    # 自动加载类
    logger.info("加载插件配置结束")
    return True

def cmsScanner(start):
    global urlListQueue
    global Modules_list
    global Finger_list
    url = urlListQueue.get(True)
    print Modules_list
    for mod in Finger_list:
        cms = mod.getfinger(url)
        if cms:
            result = mod.exp(url)
            logger.info("URL:" + url + " CMS：" + cms + "检测结果:" + result)
            break
        else:
            logger.info('false')


if __name__ == '__main__':
    urlNum = 0  #记录总共导入的url数目
    Auto_modules = {}  #自动加载插件目录
    Modules_list = defaultdict(list)
    Finger_list = []
    try:
        fr = file('urlList.txt', "r")
    except Exception as e:
        logger.error("文件urlList.txt不存在")
        exit()
    #加载插件（考虑是否需要整体延迟加载，先识别？后加载）
    if  loadplugins():
        # aspcms = Modules_list['aspcms']
        logger.info("插件加载成功")
    else:
        logger.error("插件加载失败")
        exit()
    # 启动一个存储url列表的队列
    urlListQueue = Queue.Queue()
    # 单独启动一条线成导入url
    try:
        queue = myThread()
        queue.start()
    except Exception as e:
        logger.error("线程启动失败")
        exit()
    pool = threadpool.ThreadPool(20)
    reqrest = threadpool.makeRequests(cmsScanner,'start')
    [pool.putRequest(req) for req in reqrest]
    pool.wait()
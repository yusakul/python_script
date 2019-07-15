import urllib.request
import multiprocessing,time
from multiprocessing import Pool

def DownLoad(url,num_retry=5):
    print("start....")
    html = None
    try:
        html = urllib.request.urlopen(url).read()
    except Exception as e:
        print(e)
    return html

def CreateUrl(num):
    url = 'http://193.32.161.77/postttt/%s.txt'%num
    path = 'Message/test%s.txt'%num
    result = DownLoad(url)
    with open(path,'wb+') as file:
        file.write(result)

def start():
    m = multiprocessing.Manager()
    proclist = []
    p = Pool(10)

    for num in range(78,20000000):
        proc = p.apply_async(CreateUrl,args=(num,))
        proclist.append(proc)
        time.sleep(0.5)
    p.close()
    p.join()

if __name__ == "__main__":
    start()
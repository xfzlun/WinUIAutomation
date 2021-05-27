import threading
import time

def test():  # 定义一个test函数供线程调用
    for i in range(5):
        print('test', i)
        time.sleep(1)

thread1 = threading.Thread(target=test)
thread1.start()

for i in range(5):
    print('main', i)
    time.sleep(1)

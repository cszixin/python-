# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:25:44 2016

@author: thor
自己在get函数中使用Future的线程池的submit返回一个future对象，并添加其回调函数，需要使用@web.asynchronous来保持http的长连接
并在回调中完成对client的数据发送，以及连接的释放,不必使用 gen.coroutine 修饰get
"""

from tornado.ioloop import IOLoop
from tornado import gen, web
from tornado.concurrent import Future
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time
import json
executor = ThreadPoolExecutor(5)

@gen.coroutine
def test(delay):

    yield mysleep(delay)
    print 'testpyt'


def mysleep(delay):
    time.sleep(int(delay))
    fut = Future()
    fut.set_result("test")
    return fut
    

test(1)
print '123'

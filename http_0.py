# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:25:44 2016

@author: thor
自己在get函数中使用Future的线程池的submit返回一个future对象，并添加其回调函数，需要使用@web.asynchronous来保持http的长连接
并在回调中完成对client的数据发送，以及连接的释放,不必使用 gen.coroutine 修饰get
"""

from tornado.ioloop import IOLoop
from tornado import gen, web
from concurrent.futures import Future
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time
import json

def test(x,y,delay):
    time.sleep(int(delay))
    return x+y

class ExampleHandler( web.RequestHandler ):
    executor = ThreadPoolExecutor(5)
    def callback(self,f):
        ff = Future()
        ff.set_result(f.result())
        self.write({'status':ff.result()})
        self.finish()
    @web.asynchronous 
    @gen.coroutine
    def get( self ):
        delay = self.get_argument( 'delay', 5 )
        #yield gen.sleep( int( delay ))
        res = self.executor.submit(test,7,8,delay)
        res.add_done_callback(self.callback)
        
#    @gen.coroutine
#    def post( self ):
#        pass

    def test(self,x,y,delay):
        time.sleep(int(delay))
        fut = Future()
        fut.set_result(x+y)
        return fut

application = web.Application( [
                        ( r"/example", ExampleHandler ),
                        #( r"/other", OtherHandler ),
                               ], autoreload = True )

application.listen( 8765 )
IOLoop.current().start()

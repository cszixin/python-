# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:25:44 2016

@author: thor
在get中yield一个用run_on_executor修饰的耗时函数,注意yield 返回后直接是结果，而不是future对象

"""

from tornado.ioloop import IOLoop
from tornado import gen, web
from tornado.concurrent import Future
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
        
    @gen.coroutine
    def get( self ):
        delay = self.get_argument( 'delay', 5 )
        #yield gen.sleep( int( delay ))
        res =  yield self.test(7,9,delay)
        print type(res)
        self.write( { "status": 2,"message":res} )
        self.finish()
        
#    @gen.coroutine
#    def post( self ):
#        pass
    @run_on_executor
    def test(self,x,y,delay):
        time.sleep(int(delay))
        return x+y

        
application = web.Application( [
                        ( r"/example", ExampleHandler ),
                        #( r"/other", OtherHandler ),
                                ], autoreload = True )

application.listen( 8765 )
IOLoop.current().start()

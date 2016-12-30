# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 23:25:44 2016

@author: thor
用多线程实现

"""

from tornado.ioloop import IOLoop
from tornado import gen, web
from concurrent.futures import Future
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import time
import json
import threading


class ExampleHandler(web.RequestHandler):

    @gen.coroutine
    @web.asynchronous
    def get(self):
      delay = self.get_argument( 'delay', 5 )
      x = self.get_argument( 'x', 5 )
      y = self.get_argument( 'y', 5 )
      th = threading.Thread(target= self.do_test,args= (delay,x,y))
      th.start()


    def do_test(self,delay,x,y):
        time.sleep(int(delay))
        self.write(str(x+y))
        self.finish()


        
application = web.Application( [
                        ( r"/example", ExampleHandler ),
                        #( r"/other", OtherHandler ),
                                ], autoreload = True )

application.listen( 8765 )
IOLoop.current().start()

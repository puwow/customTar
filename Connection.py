#-*- coding:utf-8 -*-
import requests
import json
import logging
from requests.exceptions import ConnectionError
import os

logging.basicConfig(level=logging.INFO) 

class Connection:
    def __init__( self, url=None ):
        self.url = 'http://127.0.0.1:5000/api/'
        if url is not None:
            self.url = url
    def ajax( self, method='query', resource=None, data=None ):
        #对资源进行操作，并返以字典形式结果
        if resource is not None:
            if self.url.endswith('/'):
                self.url = self.url + resource.lstrip('/')
            else:
                self.url = self.url + '/' + resource.lstrip('/')
        logging.info( self.url )
        try:
            resp = "{'code':200, 'msg':u'交易成功!'}"
            if method == 'add' or method == 'ADD':
                resp = requests.post( self.url, data=data )
            elif method == 'update' or method == 'UPDATE':
                resp = requests.put( self.url, data=data )
            elif method == 'delete' or method == 'DELETE':
                resp = requests.delete( self.url, data=data )
            elif method == 'query' or method == 'QUERY':
                resp = requests.get( self.url, data=data )
            else:
                resp = "{'code':404, 'msg':u'不支持的资源操作!'}"
            return json.loads(resp.text)
        except ConnectionError as er:
            return {'code':500, 'msg':u'连接服务器失败!'}
        except Exception as e:
            return json.loads(resp.text)

if __name__ == '__main__':
    conn = Connection()
    ret = conn.ajax( resource='/user', data={'username':'admin'} )
    print ret

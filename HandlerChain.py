# coding: utf-8
'''
Created on 2013-7-3
handler chain
@author: xuechong
'''

from moehandlers import __default_chain__
from moehandlers import __text_chain__
from moehandlers import __event_handlers__
import logging
import Weixin
from Weixin import textReply

def textHandlerChain(userMsg):
    """
    return a new instance of a default text msg handler chain
    """
    return HandlerChain(userMsg,list(__text_chain__))

class HandlerChain(object):
    """
    the handler chain 
    call doChain to get a reply xml str
    """
    handlers = list()
    userMsg = None
    
    def __init__(self,userMsg,handlerList=None):
        self.handlers = handlerList
        self.userMsg = userMsg
        if self.handlers==None:
            if(self.getMsgType()==Weixin.__MSGTYPE_TEXT__):
                self.handlers=list(__text_chain__)
            else :
                if(self.getMsgType()==Weixin.__MSGTYPE_EVENT__):
                    self.handlers=list(__event_handlers__)
                else :
                    self.handlers=list(__default_chain__)
        logging.debug("new handlerChain" + str(self.handlers))
        
        
    def doChain(self):
        """
        invoke handlers and return reply xmlstr
        """
        try :
            result =  self.invokeNext()
            return result==None and textReply(self.userMsg) or result
        except Exception as e:
            logging.exception(str(e))
            return textReply(self.userMsg,"555不能碰那里了啦><")
    
    def invokeNext(self):
        """
        invoke next handler until there is no handler left or have result
        returns None if no handler can hand the income msg
        """
        result = None
        if len(self.handlers)>0:
            handler = self.handlers.pop()()
            result = handler.handle(self)
            if result==None and len(self.handlers)>0:
                result = self.invokeNext()
        return result
    
    def getMsgType(self):
        """
        get the msgtype of the income msg
        """
        return self.userMsg.get("MsgType")
    
    def getMsgContent(self):
        """
        get the content of the income msg
        ***only text msg has this value***
        """
        return self.userMsg.get("Content").encode("utf-8").strip()
    
    def getFromMsg(self,key):
        """
        get things from the income msg
        """
        return self.userMsg.get(key).encode("utf-8").strip()
    
    def forceStop(self):
        """
        stop the handler chain 
        after call this ,if you can return a None to reply user a default msg
        and the rest of the handlers will not be invoked
        *return a None*
        """
        self.handlers = list()
        return None
        
        
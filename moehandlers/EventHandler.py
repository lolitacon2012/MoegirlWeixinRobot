# coding: utf-8
'''
Created on 2013-8-14

@author: xuechong
'''
import Weixin
import logging

__event_subscribe__ = "subscribe"
__event_unsubscribe__ = "unsubscribe"

class EventHandler(object):
   
    def handle(self,handlerChain):
        
        if (handlerChain.getMsgType()==Weixin.__MSGTYPE_EVENT__):
            if(handlerChain.getFromMsg("Event")==__event_subscribe__):
                logging.debug("new user!")
                return Weixin.textReply(handlerChain.userMsg,"")
        
        return handlerChain.invokeNext()
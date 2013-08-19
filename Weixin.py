# coding: utf-8
'''
Created on 2013-7-3
constants & basic function for weixin api
@author: xuechong
'''

import hashlib
import logging
from xml.etree import ElementTree

__token = "token"
__text_answer = "<xml><ToUserName><![CDATA[${toUser}]]></ToUserName><FromUserName><![CDATA[${fromUser}]]></FromUserName><CreateTime>${createTime}</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[${Content}]]></Content><MsgId>${MsgId}</MsgId></xml>"
__pic_answer="<xml>\
 <ToUserName><![CDATA[$toUser]]></ToUserName>\
 <FromUserName><![CDATA[$fromUser]]></FromUserName>\
 <CreateTime>$createTimt</CreateTime>\
 <MsgType><![CDATA[news]]></MsgType>\
 <ArticleCount>2</ArticleCount>\
 <Articles>\
 <item>\
 <Title><![CDATA[title1]]></Title> \
 <Description><![CDATA[description1]]></Description>\
 <PicUrl><![CDATA[picurl]]></PicUrl>\
 <Url><![CDATA[url]]></Url>\
 </item>\
 <item>\
 <Title><![CDATA[title]]></Title>\
 <Description><![CDATA[description]]></Description>\
 <PicUrl><![CDATA[picurl]]></PicUrl>\
 <Url><![CDATA[url]]></Url>\
 </item>\
 </Articles>\
 </xml> "
__MSGTYPE_TEXT__ = "text"
__MSGTYPE_EVENT__ = "event"

def validate(param):
    """
    validate if the request is posted by weixin 
    """
    list_ = sorted([__token, param("timestamp"), param("nonce")])
    sha1 = hashlib.sha1()
    sha1.update("".join(list_))
    return str(sha1.hexdigest()) == param("signature")

def textReply(originMsg,replyStr="阿嘞?人家不懂你在说什么啦,输入'帮助'可以查看帮助哦!"):
    """
    return a text type reply xml
    """
    result = __text_answer.replace("${toUser}", originMsg.get("FromUserName"))\
    .replace("${fromUser}",originMsg.get("ToUserName"))\
    .replace("${createTime}",originMsg.get("CreateTime"))\
    .replace("${MsgId}",originMsg.get("MsgId"))\
    .replace("${Content}",replyStr)
    logging.debug(result)
    return result

class MsgContent:
    """
    the content of the user post msg 
    """
    content = {}
    
    def __init__(self,xmlContent):
        '''
        xmlContent the str content of the xml
        '''
        root = ElementTree.fromstring(xmlContent)
        _nodes = root.getiterator("xml")
        for node in _nodes.pop().getchildren():
            self.content[node.tag]=node.text
    
    def get(self,key):
        return self.content.get(key)
    
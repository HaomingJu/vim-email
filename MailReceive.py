# -*- coding: utf-8 -*-

import imaplib
import email
from email.header import Header, decode_header, make_header
import re
import logging

# 保存邮箱地址, 为了后面的通讯录建设
class MailAddress:
    def __init__(self, desc_, addrs_):
        self.Description = desc_
        self.Address = addrs_


# 邮件标头, 用于速看
class MailTitle:
    def __init__(self, title):
        # sele.mailReg = "@"
        self.Subject = make_header(decode_header(title['Subject']))
        self.Date = make_header(decode_header(title['Date']))
        self.From = []
        self.To = []
        self.Attach = None
        self.UID = -1

        # Tos = str(make_header(decode_header(title['To']))).split(',')
        # for ele in Tos:
            # ele = ele.strip()
            # ret = re.search('(?P<description>.+)\s+<(?P<address>.+@.+)>', ele)
            # if ret is None:
                # ret = re.search('(?P<address>.+@.+)', ele)
                # logging.info(ret.groupdict()['address'])
            # else:
                # logging.info(ret.groupdict()['description'])
                # logging.info(ret.groupdict()['address'])

        Froms = str(make_header(decode_header(title['From'])))
        logging.info(Froms)


        # logging.info(self.Subject)
        # logging.info(make_header(decode_header(title['To'])))




class MailReceive:

    # Link remote mail server (连接远程服务器)
    def __init__(self, imap_ssl_addr, imap_ssl_port, user_name, user_pwd):
        self.imap_ssl_addr = imap_ssl_addr
        self.imap_ssl_port = imap_ssl_port
        self.imap_user_name = user_name
        self.imap_user_pwd = user_pwd
        self.client = imaplib.IMAP4_SSL(self.imap_ssl_addr, self.imap_ssl_port)
        self.Mails = []
        try:
            self.client.login(self.imap_user_name, self.imap_user_pwd)
            logging.info("Login successful.")
        except:
            logging.error("Login failed.")
            # TODO: return or throw err (返回or抛出异常)

        self.mailFolders = {}

    def getMailNums(self):
        return self.Mails.__len__()

    # Close link with remote while destroy this object (析构时关闭同远程服务器的链接)
    def __del__(self):
        self.client.logout()

    # Get all folder's name of remote mail server (获取远程服务器中所有文件夹名称)
    def fetchFolder(self):
        ret, mailFolders = self.client.list()
        for ele in mailFolders:
            folderName = ele.decode('utf-8').split(' "/" ')[-1]
            self.mailFolders[folderName] = []
            logging.info(folderName)
        # TODO: 正确显示中文

    def selectInboxAll(self):
        self.client.select(readonly=True)
        ret, inboxUnseen = self.client.search(None, 'ALL')
        inboxUnseen = inboxUnseen[0].split()

        for ele in inboxUnseen:
            mailRet, mailData = self.client.fetch(str(ele.decode('utf-8')), '(UID BODY[HEADER])')
            if mailData[0] is None and mailRet == 'OK':
                continue
            mailMessage = email.message_from_bytes(mailData[0][1])
            self.Mails.append(MailTitle(mailMessage))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    gIMAP_SSL_ADDRESS = "imap.exmail.qq.com"
    gIMAP_SSL_PORT = 993
    gUSER_NAME = None
    gUSER_PWD = None

    rec = MailReceive(gIMAP_SSL_ADDRESS, gIMAP_SSL_PORT, gUSER_NAME, gUSER_PWD)
    # rec.fetchFolder()
    rec.selectInboxAll()

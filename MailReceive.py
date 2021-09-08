# -*- coding: utf-8 -*-

import imaplib
import email
import logging



class MailReceive:

    # Link remote mail server (连接远程服务器)
    def __init__(self, imap_ssl_addr, imap_ssl_port, user_name, user_pwd):
        self.imap_ssl_addr = imap_ssl_addr
        self.imap_ssl_port = imap_ssl_port
        self.imap_user_name = user_name
        self.imap_user_pwd = user_pwd
        self.client = imaplib.IMAP4_SSL(self.imap_ssl_addr, self.imap_ssl_port)
        try:
            self.client.login(self.imap_user_name, self.imap_user_pwd)
            logging.info("Login successful.")
        except:
            logging.error("Login failed.")
            # TODO: return or throw err (返回or抛出异常)

        self.mailFolders = {}

    # Get all folder's name of remote mail server (获取远程服务器中所有文件夹名称)
    def fetchFolder(self):
        ret, mailFolders = self.client.list()
        for ele in mailFolders:
            folderName = ele.decode('utf-8').split(' "/" ')[-1]
            self.mailFolders[folderName] = []
            logging.info(folderName)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    gIMAP_SSL_ADDRESS = "imap.exmail.qq.com"
    gIMAP_SSL_PORT = 993
    gUSER_NAME = "TODO"
    gUSER_PWD = "TODO"

    rec = MailReceive(gIMAP_SSL_ADDRESS, gIMAP_SSL_PORT, gUSER_NAME, gUSER_PWD)
    rec.fetchFolder()




    # mailNums = int(messags[0])
    # for index in range(mailNums):
        # mailRet, mailData = client.fetch(str(index), '(UID BODY[HEADER])')
        # if mailData[0] is None:
            # print("NONE")
            # continue

        # mailMessage = email.message_from_bytes(mailData[0][1])
        # print('------------------------------------------------------')
        # print('Date: %s' % mailMessage['Date'])
        # print('From: %s' % mailMessage['From'])
        # print('To: %s' % mailMessage['To'])
        # print('Subject: %s' % mailMessage['Subject'])

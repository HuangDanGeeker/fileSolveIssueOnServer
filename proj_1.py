#-*- coding: utf-8 -*-
from socket import *
import struct
import time
class TcpClient:
    HOST='202.197.61.231'
    PORT=10086
    ADDR=(HOST, PORT)
    filePath = "D:/"
    def __init__(self):
        try:
            self.clientSocket = socket(AF_INET, SOCK_STREAM)
            self.clientSocket.connect(self.ADDR)
        except clientSocket.error:
            print ('Failed to create socket. Error code ' + str(socket.error[0]) + " , Error message  " + socket.error[1])
            sys.exit();
        print ('>>Socket Created')
        while True:
            choice = input(">>your choice :\n   listAll pull get eixt\n >>")
            if 'listAll' == choice:
                self.listAllFile()
            elif "get" == choice:
                self.getFormServer()
            elif "pull" == choice:
                self.putToServer()
            elif "exit" == choice:
                break
            else:
                continue
        self.clientSocket.close()

    #listAll
    def listAllFile(self):
        listStuct = struct.pack('!B',1)
        self.clientSocket.send(listStuct);
        recBuffer = self.clientSocket.recv(1024)
        print(recBuffer)
        replyType = struct.unpack('!B',bytes(recBuffer[0]))
        if replyType:
            sign,size = struct.unpack('!BH',recBuffer)
            data = self.clientSocket.recv(4096)
        else:
            sign,size = struct.unpack('!BB',recBuffer)
            data = clientSocket.recv(size)
        print(str(data,encoding='utf-8'))
        print(str(self.clientSocket.recv(1024), encoding="utf-8"))
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.ADDR)



    #Get
    def getFormServer(self):
        fileName = input(">>the file you download :")
        length = len(fileName)
        getStuct = struct.pack('!BB'+str(length)+'s',0,length,bytes(fileName,\
          encoding='utf-8'))
        self.clientSocket.send(getStuct)
        rcvBuffer = self.clientSocket.recv(1024)
        replyType,fileSize = struct.unpack('!BL',rcvBuffer)
        #文件获取成功的判断
        if 2 == replyType:
            recvSize = 0
            admit = input(">>the file will be download at root D:/ (Y/N)  ")
            if "N" == admit :
                self.filePath = input(">>input your download root: ")
            print(">>make sure that the file is not exist on your root, or it will occur failure")
            with open(self.filePath + fileName,'wb') as filePointer:
                while recvSize < fileSize:
                    fileBuffer = self.clientSocket.recv(1024)
                    recvSize += len(fileBuffer)
                    filePointer.write(fileBuffer)
            print("file download success")
        #文件获取失败
        else:
            erroMsg = self.clietnSocket.recv(fileSize)
            print(str(erroMsg, encoding="utf-8"))
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.ADDR)

    #put
    def putToServer(self):
        print(">>root is what you have set in Get part(Default: D:/)")
        admit = input(">>would you like to change the root (Y/N)")
        if "Y" == admit :
            self.filePath = input(">>the root of the upload file")
        fileName = input('>>the file you upload: ')
        destFileName = "1502_haodong_wang_test.txt"
        lengthOfDestFileName = len(destFileName)
        with open(self.filePath + fileName,'rb') as filePointer:
            fileBuffer = bytes()
            for line in filePointer:
                fileBuffer += line
        fileSize = len(fileBuffer)
        pullStruct = struct.pack('!BBL'+str(lengthOfDestFileName)+'s'+ str(fileSize)+'s',\
                                 2,lengthOfDestFileName,fileSize,bytes(destFileName, encoding='utf-8'),fileBuffer)
        self.clientSocket.send(pullStruct)
        print(str(self.clientSocket.recv(1024), encoding="utf-8"))
        print(">>the file" + destFileName + "has been uploaded to the server, you may have seen it before")
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(self.ADDR)

if __name__ == '__main__':
    client=TcpClient()




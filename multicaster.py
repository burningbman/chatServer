import utils
from threading import Timer
from utils import TYPE_CHAT

DELAY = 1

class Multicaster(object):

    def __init__(self):
        self.clientSockets = list()
        self.file = open('input.txt', 'r')
        
        # set up a timer to send out the chat message to all connected clients
        Timer(DELAY, self.sendChat).start()
        
    def addClientSocket(self, socket):
        self.clientSockets.append(socket)
        
    def sendChat(self):
        next100Bytes = self.file.read(100)
        
        # if the file is empty, stop casting
        if next100Bytes == None:
            return
        
        # send the 100 bytes to all connected clients
        for i, socket in enumerate(self.clientSockets):
            utils.sendPacket(socket, TYPE_CHAT, {
                'data': next100Bytes,
                'seqNumber': i # sequence number of the chat session
                })

        # schedule the next message cast
        Timer(DELAY, self.sendChat).start()
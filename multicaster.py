import utils, json, threading
from utils import TYPE_CHAT

class Multicaster(object):

    def __init__(self):
        self.clientSockets = list()
        
    def listenToClientSocket(self, socket):
        # listen for client chat messages
        while True:
            data = json.loads(socket.recv(4096))
            utils.processReceivedPacket(data, socket)
            self.sendChat(data['data'])
        
    def addClientSocket(self, socket):
        self.clientSockets.append(socket)
        
        # start a thread to listen to client for chat
        threading.Thread(target=self.listenToClientSocket, args=[socket]).start()
        
    def sendChat(self, data):        
        # send the 100 bytes to all connected clients
        for i, socket in enumerate(self.clientSockets):
            utils.sendPacket(socket, TYPE_CHAT, {
                'data': data,
                'seqNumber': i # sequence number of the chat session
                })
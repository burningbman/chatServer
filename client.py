import socket, utils, json
from sys import getsizeof

userName = 'Blake'

def main():
    # create a connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((utils.HOST, utils.PORT))
    
    # send the first registration request
    utils.sendPacket(s, utils.TYPE_REG, {
        'mName': 'localhost',
        'uName': userName,
        'seqNumber': 1
    })
    
    # send the second registration request
    utils.sendPacket(s, utils.TYPE_REG, {
        'mName': 'localhost',
        'uName': userName,
        'seqNumber': 2
    })
    
    # send the third registration request
    utils.sendPacket(s, utils.TYPE_REG, {
        'mName': 'localhost',
        'uName': userName,
        'seqNumber': 3
    })
    
    # listen for server ack and multicast messages
    while True:
        data = s.recv(4096)
        utils.processReceivedPacket(json.loads(data), s)

if __name__ == '__main__':
    main()

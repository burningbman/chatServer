import socket, utils, json, threading

userName = 'Blake'

# TODO: Accept user input and send it to the chat server
def listenToUser(socket):
    while True:
        data = input('Enter message to send:')
        utils.sendPacket(socket, utils.TYPE_CHAT, {
            'uName': userName,
            'data': data})


def main():
    # TODO: Get chat room number from user
    chatRoom = input('Enter the chat room to join  (an integer):')

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
    
    # TODO: Add chat room number
    # send the third registration request
    utils.sendPacket(s, utils.TYPE_REG, {
        'mName': 'localhost',
        'uName': userName,
        'seqNumber': 3,
        'chatRoom': int(chatRoom)
    })
    
    # begin listening to the user for chat messages to send 
    threading.Thread(target=listenToUser, args=[s]).start()
    
    # listen for server ack and multicast messages
    while True:
        data = s.recv(4096)
        utils.processReceivedPacket(json.loads(data), s)


if __name__ == '__main__':
    main()

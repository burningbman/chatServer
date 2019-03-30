import socket, json
global HOST, PORT, TYPE_REG, TYPE_CONF, TYPE_CHAT, TYPE_CHAT_RESP, TYPE_MAP

def sendPacket(conn, packetType, packetData={}):
    """ Send a packet using the provided socket with the supplied data
    
    Build the packet data, switching integers to use network byte order.
    Send the packet using the provided socket.
    Print the sent data
    
    Args:
        conn (socket): socket to send data along
        packetType (int): type of packet to send
    Kwargs:
        packetData (dictionary): data to send in packet
    """
    
    addr = conn.getpeername()
    print('Sending %s to %s:%d with data' % (TYPE_MAP[packetType], addr[0], addr[1]), packetData)
    
    # change integers to network byte order
    for param in INT_VALUES:
        if param in packetData:
            packetData[param] = socket.htons(packetData[param])
    
    # combine packet type data with additional packet data
    dataToSend = {**{
        'type': socket.htons(packetType)
    }, **packetData}
    
    # send the packet data
    data = json.dumps(dataToSend).encode('utf-8')
    conn.sendall(data)
    
def processIntsInPacket(packet):
    for param in INT_VALUES:
        if param in packet:
            packet[param] = socket.ntohs(packet[param])
    
def processReceivedPacket(packet, conn):            
    """ Processes a packet that has been received.
    
    Switch integers from network byte order to host byte order.
    Prints the information about the received packet.
    
    Args:
        packet (dictionary): data received from client
        conn (socket): socket with TCP connection to client
    Returns:
        dictionary. Data received from the socket with modified integers
    """
    
    # handle byte order for integers
    processIntsInPacket(packet)
    
    # print out the received connection
    addr = conn.getpeername()
    print ('Received %s from %s:%d with data' % (TYPE_MAP[packet['type']], addr[0], addr[1]), packet)
    
    return packet
    
HOST = 'localhost'
PORT = 29384
TYPE_REG = 121
TYPE_CONF = 221
TYPE_CHAT = 131
TYPE_CHAT_RESP = 231
TYPE_MAP = {
    TYPE_REG: 'REGISTRATION',
    TYPE_CONF: 'CONFIRMATION',
    TYPE_CHAT: 'CHAT',
    TYPE_CHAT_RESP: 'CHAT RESPONSE'
    }
INT_VALUES = 'type', 'seqNumber'
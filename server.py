import socket, json, utils, threading
from multicaster import Multicaster
from utils import TYPE_CONF

multicasters = {}

def getMulticaster(num):
    if num not in multicasters:
        multicasters[num] = Multicaster()
        
    return multicasters[num]

# sent the packet to the correct processor based on method
def processClient(packet, conn):
    # process registration packet one
    utils.processReceivedPacket(packet, conn)
    
    # listen for and process registration packet two
    data = conn.recv(73)
    utils.processReceivedPacket(json.loads(data), conn)
    
    # listen for and process registration packet three
    data = json.loads(conn.recv(90))
    utils.processReceivedPacket(data, conn)
    
    # send confirmation message to client
    utils.sendPacket(conn, TYPE_CONF)

    # add the registered client to the multicaster
    getMulticaster(data['chatRoom']).addClientSocket(conn)

def main():
    """ Start the server
    
    Start the server. Once a client connects, start a thread to handle the initial response
    and continue listening for requests.
    
    """
    # set up a socket to listen on
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((utils.HOST, utils.PORT))
    s.listen()
        
    # set up a loop to listen to new connections
    while True:
        conn, addr = s.accept()
        
        # get the packet from the client and turn it in to a dict
        data = conn.recv(73)
        jsonData = json.loads(data)
        
        # fire up a thread to handle client registration
        threading.Thread(target=processClient, args=[jsonData, conn]).start()

# start the server if the server is being executed
if __name__ == '__main__':
    main()

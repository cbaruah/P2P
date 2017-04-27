import socket
import os
import shlex
import threading

index_list=list()
count=0
peer_list=list()
SERVER_PORT = 7734
rfcList=list()

#Reference was used from www.stackoverflow.com for completion of this project

class RFCRecord:
    def __init__(self, rfc_number = -1, rfc_title = 'None', peerHostname ='None', peerid =-1):
        self.rfc_number = rfc_number
        self.peerid = peerid
        self.peerHostname = peerHostname
        self.rfc_title = rfc_title

    def __str__(self):
        return str(self.rfc_number)+' '+str(self.rfc_title)+' '+str(self.peerHostname)+' '+str(self.peerid)



class PeerRecord:                                                                                            
    def __init__(self,peerHostname='None',peerPortNo=10000,peerid=-1):
        self.peerHostname=peerHostname
        self.peerPortNo=peerPortNo
        self.peerid=peerid

    def __str__(self):
        return str(self.peerHostname)+' '+str(self.peerPortNo)+' '+str(self.peerid)

def register(data, clientsocket, flag):
    global count
    count = count+1
    rlist=shlex.split(data)
    rfc_list=str(data).rsplit(':',1)
    c=shlex.split(rfc_list[1])
    counter = 0
    if True:
        peer_list.insert(0,PeerRecord(rlist[3],rlist[5],count))
        counter = counter + 1;
        for i,j in zip(c[::2],c[1::2]):
            counter=counter+1;
            index_list.insert(0,RFCRecord(i,j,rlist[3],count))
    if counter:
        counter=0
    reply="Thank you for registering"
    clientsocket.send(reply)

def listAll(clientsocket, value):
    global status
    global phrase
    list_status(0, '')


    reply=list()
    if not index_list:
        list_status(404, 'BAD REQUEST')
    else:
        record_list(reply)

    response="P2P-CI/1.0 "+str(status)+" "+str(phrase)+"\n"
    flag=1
    for i in reply:
        if flag:
            reply_list=shlex.split(str(i))
            counter=flag+1
            response=response+str(reply_list[0])+" "+reply_list[1]+" "+reply_list[2]+" "+str(reply_list[3])+"\n"
            flag=1
    clientsocket.send(response)


def list_status(code, msg):
    global status, phrase
    status = code
    phrase = msg


def record_list(reply):
    global status, phrase
    for x in index_list:
        if True:
            for peer_record in peer_list:
                if peer_record.peerid == x.peerid:
                    peer_port = peer_record.peerPortNo
            reply.append(RFCRecord(x.rfc_number, x.rfc_title, x.peerHostname, peer_port))
            status = 200
            phrase = 'OK'


def search(clientsocket, rfc_number):
    reply=list()
    counter=1
    flag=0
    for x in index_list:
        if int(x.rfc_number)==int(rfc_number):
            while True:
                reply.append(RFCRecord(x.rfc_number,x.rfc_title,x.peerHostname,x.peerid))
                flag, phrase, status = search_status_pass(flag)
                break
    
    if(flag==0):
        status = 404
        phrase = 'FILE NOT FOUND'
        phrase, status = search_status_fail(phrase, status)
    
    response="P2P-CI/1.0 "+str(status)+" "+str(phrase)+"\n"
    for i in reply:
        reply_list=shlex.split(str(i))
        if counter:
            response=response+str(reply_list[0])+" "+reply_list[1]+" "+reply_list[2]+" "+str(reply_list[3])+"\n"
    clientsocket.send(response)


def search_status_pass(flag):
    status = 200
    phrase = 'OK'
    flag = 1
    return flag, phrase, status


def search_status_fail(phrase, status):
    status = 404
    phrase = 'FILE NOT FOUND'
    return phrase, status


def add_RFC(rlist, count, data, clientsocket):
    index_list.insert(0,RFCRecord(rlist[1],rlist[8],rlist[4],count))
    response = init_add(data, rlist)
    clientsocket.send(response)


def init_add(data, rlist):
    a = data.splitlines()
    title = a[3].split(":")
    status = 200
    phrase = 'OK'
    response = "P2P-CI/1.0 " + str(status) + " " + str(phrase) + "\n" + "RFC " + rlist[1] + " " + title[1] + " " + \
               rlist[4] + " " + rlist[6]
    return response


def exit(rlist, count):
    global peerhost
    peerport=rlist[5]
    list_exit(peerport,'OK', 1)

    for i in [x for x, y in enumerate(peer_list) if y.peerPortNo == peerport]:
        del peer_list[i]
    clientsocket.send("Bye")


def list_exit(peerport,status, flag):
    global peerhost
    for q in peer_list:
        if q.peerPortNo == peerport:
            peer_status=status
            peerhost = q.peerHostname
            idx2 = [x for x, y in enumerate(index_list) if y.peerHostname == str(peerhost)]
            if flag:
                for i in sorted(idx2, reverse=True):
                    del index_list[i]


def remove(rlist,count):
    rfc_pos = 0
    phostname=rlist[4]
    for q in index_list:
       if q.rfc_number==rlist[1]:
        if q.peerHostname==phostname:
            if q.peerid == count:
                del index_list[rfc_pos]
       rfc_pos = rfc_pos + 1
    clientsocket.send("Done")

def main_handler(clientsocket, clientaddr):

    print "~"*37
    print "Client Request :"
    data = clientsocket.recv(1024)

    print data
    print "~"*37
    global count
    rlist=shlex.split(data)
    if rlist[0] == 'REGISTER':
        register(data, clientsocket, count)

    elif rlist[0] == 'LOOKUP':
        search(clientsocket, rlist[1])

    elif rlist[0] == 'EXIT':
        exit(rlist, count)

    elif rlist[0] == 'REMOVE':
        remove(rlist, count)

    elif rlist[0] == 'ADD':
        add_RFC(rlist, count, data, clientsocket)

    elif rlist[0] == 'LISTALL':
        listAll(clientsocket, count)


    
if __name__=="__main__":

    serversocket = socket.socket()
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(),SERVER_PORT))

    serversocket.listen(5)

    print "Server is listening for connection \n Host: "+socket.gethostname()
    
    while(1):
        clientsocket, clientaddr = serversocket.accept()
        serverThread = threading.Thread(target=main_handler, args=(clientsocket, clientaddr))
        serverThread.start()
    serversocket.close()

    

import threading
import platform
import socket
import shlex
import sys
import os




OS = platform.system()
rfc_title=[]
a=[]
EXIT_FLAG = False
SERVER_PORT = 7734
rfc_list=[]



def rfc_retrieve(name, sock):
    request=sock.recv(1024)
    print request
    rfc_number=shlex.split(request)
    file_found = 0
    file_found, file_name = loop_val(file_found, rfc_number)

    field_condition(file_found, file_name, sock)


def loop_val(file_found, rfc_number):
    for x in a:
        t = x.split("-")
        if True:
            if int(t[0]) == int(rfc_number[2]):
                file_found = 1
                print t[0]
                file_name = str(x) + ".txt"
    return file_found, file_name


def field_condition(file_found, file_name, sock):
    if file_found == 0:
        print "File not found"
        sock.send("P2P-CI/1.0 404 FILE NOT FOUND" + "\n")
    else:
        sock.send("P2P-CI/1.0 200 OK" + "\n")
        with open(file_name, 'r') as f:
            bytesToSend = byte_send(f, sock)
            while bytesToSend != "":
                bytesToSend = byte_send(f, sock)
    sock.close()


def byte_send(f, sock):
    bytesToSend = f.read(1024)
    sock.send(bytesToSend)
    return bytesToSend


def client_resp():
    cs_socket = init()
    while(EXIT_FLAG != True):
        (peer_socket,peer_addr)=cs_socket.accept()
        print "Connected to", peer_addr
        init_thread(peer_socket)
    cs_socket.close()
    return


def init_thread(peer_socket):
    thread_third = threading.Thread(target=rfc_retrieve, args=("retrThread", peer_socket))
    thread_third.start()
    thread_third.join()


def init():
    cs_host = socket.gethostname()
    cs_port = PORT
    cs_socket = socket.socket()
    cs_socket.bind((cs_host, cs_port))
    cs_socket.listen(2)
    cs_thread = threading.current_thread()
    return cs_socket


def serv_resp_handler(message, serverIP, serverPort):
    print "~" * 100
    print "Server Response"
    sock = socket.socket()
    sock.connect((serverIP,serverPort))
    sock.send(message)
    print sock.recv(16384)
    print "~"*100
    sock.close()

def loop_condition():
    while True:
        try:
            
            condition = int(input("Do you want to continue(1/0): "))
        except ValueError:
            print("Sorry, I didn't understand that.")
            
            continue
        else:
            break
    if condition == 1: 
        return True
    else:
        print exit

def input_data():
    print "Enter RFC number"
    rfc_number = int(raw_input())
    print "Enter RFC title"
    rfc_title=raw_input()
    return rfc_number,rfc_title


def server_message(value, rfc_number, HOST, PORT, rfc_title):
    global message
    message = value + " " + str(rfc_number) + " P2P-CI/1.0" + "\n" + " Host: " + HOST + "\n" + " Port: " + str(
        PORT) + "\n" + " Title: " + rfc_title


def input_extra():
    global name_peer, port_peer
    print "Enter peer hostname(which contains the file): "
    name_peer = raw_input()
    print "Enter Peer port # : "
    port_peer = int(raw_input())


if __name__== "__main__":

    global HOST
    global PORT
    global IP
    global a

    HOST = ''
    PORT = 0
    IP = ''
    HOST = socket.gethostname()
    print "Host: "+ HOST +"\nEnter your upload port# : "
    PORT = int(raw_input())

    try:
        therad_listen = threading.Thread(target=client_resp)

        therad_listen.daemon = True

        therad_listen.start()

        temp_rfc = list()

        temp_title = list()
        print "Enter Host name of the Centralised Server"
        serverIP=raw_input()
        message = "REGISTER P2P-CI/1.0 Host: "+HOST+" Port: "+str(PORT)+"\n"
        serv_resp_handler(message, serverIP, SERVER_PORT)
        file_list = os.listdir(os.getcwd())

        print file_list
        for file_name in file_list:
            files = file_name.split(".")
            if files[1] == "txt":
                a.append(str(files[0]))
                files1 = str(files[0]).split("-")
                temp_title.append(files1[1])
                temp_rfc.append(int(files1[0]))
        
        print temp_rfc
        for x in range(len(temp_rfc)):
            server_message("ADD", temp_rfc[x], HOST, PORT, temp_title[x])
            serv_resp_handler(message, serverIP, SERVER_PORT)

        condition = True
        while condition:
            print "Select"
            print "1. List all RFC"
            print "2. Search RFC"
            print "3. Add RFC"
            print "4. Download RFC"
            print "5. Exit"

            choice = int(raw_input("Enter you Choice: "))

            if choice == 1:
                message="LISTALL P2P-CI/1.0"+"\n"+"Host: "+HOST+"\n"+" Port: "+str(PORT)
                serv_resp_handler(message, serverIP, SERVER_PORT)
                
            if choice == 2:
                rfc_number,rfc_title=input_data()
                server_message("LOOKUP", rfc_number, HOST, PORT, rfc_title)
                serv_resp_handler(message, serverIP, SERVER_PORT)

            if choice == 3:
                rfc_number, rfc_title = input_data()
                a.insert(0,str(rfc_number))
                server_message("ADD", rfc_number, HOST, PORT, rfc_title)
                serv_resp_handler(message, serverIP, SERVER_PORT)
                                
            if choice == 4:
                rfc_number,rfc_title=input_data()
                input_extra()
                message = "GET RFC " +str(rfc_number)+ " " +"P2P-CI/1.0\n"+"Host: "+name_peer+"\n"+"OS: "+str(OS)

                peer_ip= socket.gethostbyname(name_peer)
                s = socket.socket()
                s.connect((peer_ip,port_peer))
                print "\nclient connected: \n"
                s.send(message)
                reply_list = shlex.split(s.recv(1024))
                os.chdir(os.getcwd())
                file_name=str(rfc_number)+"-"+rfc_title+".txt"
                if str(reply_list[1])=='200':
                    file1=open(file_name,'wb')

                    q=s.recv(1024)
                    if q:
                        file1.write(q)
                        status = True
                    else:
                        file1.close()
                        print "File %s downloaded successfully\n" % (file_name)
                        status = True

                    s.close()
                else:
                    print "File Not Found"
                    s.close()
                    status = False

                if status == True:
                    a.insert(0,str(rfc_number))
                    server_message("ADD", rfc_number, HOST, PORT, rfc_title)
                    serv_resp_handler(message, serverIP, SERVER_PORT)

            if choice == 5:
                message = "EXIT P2P-CI/1.0 Host: "+HOST+" Port: "+str(PORT)
                serv_resp_handler(message, serverIP, SERVER_PORT)
                EXIT_FLAG
                EXIT_FLAG = True

            if choice == 6:
                rfc_number, rfc_title = input_data()
                str_file_name = str(rfc_number)+"-"+rfc_title+".txt"
                os.remove(str_file_name)
                server_message("REMOVE", rfc_number, HOST, PORT, rfc_title)
                serv_resp_handler(message, serverIP, SERVER_PORT)
                
                          
            condition = loop_condition()       

        while(EXIT_FLAG == False):
            pass  
        sys.exit(0)

    except KeyboardInterrupt:
        sys.exit(0)
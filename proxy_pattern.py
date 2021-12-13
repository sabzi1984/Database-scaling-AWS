#!/usr/bin/python3

import socket
import pickle
from random import randint
import argparse
# import  mysql-connector-python
from pythonping import ping




parser = argparse.ArgumentParser()
parser.add_argument('mode', help='mode of implementation of proxy, direct, random or custom')
args = parser.parse_args()

mode=args.mode 
# 0: master and [1,...]: slave id

targets={0:{"ip":"34.202.223.21", "port":3306},1:{"ip":"35.174.80.126", "port":3306},2:{"ip":"52.5.114.194", "port":3306}}

#socket programming, inspired from https://realpython.com/python-sockets/,  https://docs.python.org/3/library/socket.html, https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/
def main():

    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.bind(('', 5001))   #socket.gethostname()
    listen.listen(1)
    while True:
        conn, addr = listen.accept()
        print(f"Connection from {addr} has been established.")
        with conn:
            print('Connected by', addr)

            while True:
                data = conn.recv(2048) 
                if not data:
                    break
                
                cmd_type, command = load_data(data)
                
                if cmd_type=="insert" and mode=='direct':
                    targ=0
                    target_node="master"
                    cnx = mysql.connector.connect(user='proxy', password='alfi1326', host=targets[targ]["ip"], database='tp3')
                    print ('Connection to DB opened')
                    cursor = cnx.cursor()
                    cursor.execute(command)
                    cnx.commit()
                    response = {'handled by':target_node, 'response': "OK"}
                    response = pickle.dumps(response)
                    conn.send(response)
                    
                    
                if cmd_type=="select" and mode=='direct':
                    targ=0
                    target_node="master"
                    cnx = mysql.connector.connect(user='proxy', password='alfi1326', host=targets[targ]["ip"], database='tp3')
                    print ('Connection to DB opened')
                    cursor = cnx.cursor()
                    cursor.execute(command)
                    print('handled by :{target_node}')
                    conn.send(cursor)
                    
                if cmd_type=="select" and mode=='random':
                    targ=randint(1, 3)
                    target_node="slave"+str(targ)

                    cnx = mysql.connector.connect(user='proxy', password='alfi1326', host=targets[targ]["ip"], database='tp3')
                    print ('Connection to DB opened')
                    cursor = cnx.cursor()
                    cursor.execute(command)
                    print('handled by :{target_node}')
                    conn.send(cursor)
                    # for (Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1) in cursor:
                    #     print (f"{Series_reference}, {Period, Data_value}, {Status, Units}, {Magnitude}, {Series_title_1}")
                    
                if cmd_type=="select" and mode=='custom':
                    targ=custom()
                    target_node="slave"+str(targ)
                    cnx = mysql.connector.connect(user='proxy', password='alfi1326', host=targets[targ]["ip"], database='tp3')
                    print ('Connection to DB opened')
                    cursor = cnx.cursor()
                    cursor.execute(command)
                    print('handled by :{target_node}')
                    conn.send(cursor)
                    # for (Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1) in cursor:
                    #     print (f"{Series_reference}, {Period, Data_value}, {Status, Units}, {Magnitude}, {Series_title_1}")
                
                
                # send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # send.connect((targets[targ]["ip"], targets[targ]["port"]))
                # cnx = mysql.connector.connect(user='root', password='alfi1326', host=targets[targ]["ip"], database='tp3')
                # print ('Connection to DB opened')
                # cursor = cnx.cursor()
                # if cmd_type == 'insert':
                # cursor.execute(command)
                # cnx.commit()
                
                # send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                

                # response = pickle.dumps(response)
                # # send.send(pickledobj)
                
                # # response =' handled by node ' + str(targ)
                # conn.send(response)

        print ('Will close socket')
        # send.close()
        listen.close()


def load_data(data):
    data=pickle.loads(data)
    
    type = 'select'

    if data['type']=='insert':
        type = 'insert'

    command = data['command']

    return type, command


def custom():
    responses={}
    for target in targets.keys():
        resp = ping(target.server_host)
        responses[target.server_host]=resp.rtt_avg

    fastest_host = min(responses, key=responses.get)

    target = list(filter(lambda connection: connection.server_host == fastest_host, targets))[0]
    return target


if __name__ == '__main__':
    main()

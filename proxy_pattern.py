#!/usr/bin/python3

import shlex
from subprocess import Popen, PIPE, STDOUT
import socket
import pickle
from random import randint
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('mode', help='mode of implementation of proxy, direct, random or custom')
args = parser.parse_args()

mode=args.mode 
# 0: master and [1,...]: slave id

targets={0:{"ip":"ec2-18-212-67-21.compute-1.amazonaws.com", "port":5001},1:{"ip":"ec2-18-212-201-7.compute-1.amazonaws.com", "port":5001},2:{"ip":"ec2-18-233-9-44.compute-1.amazonaws.com", "port":5002},3:{"ip":"ec2-54-235-230-176.compute-1.amazonaws.com", "port":5001}}

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
                data = str(data)
                print ('data: ' , data)
                
                cmd_type, command = parse_data(data)
                
                if cmd_type=="insert" or mode=='direct':
                    targ=0
                
                if cmd_type=="select" and mode=='random':
                    targ=randint(1, 3)
                    
                if cmd_type=="select" and mode=='custom':
                    targ=custom()
                
                
                send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send.connect((targets[targ]["ip"], targets[targ]["port"]))
                

                obj = {'type':cmd_type, 'command': command}
                pickledobj = pickle.dumps(obj)
                send.send(pickledobj)
                
                response =' handled by node ' + str(targ)
                conn.send(response)

        print ('Will close socket')
        send.close()
        listen.close()


def parse_data(data):
    data=pickle.loads(data)
    
    type = 'select'

    if data['type']=='insert':
        type = 'insert'

    command = data['command']

    return type, command


def custom():
    selectedSlave = 1
    minTiming = 999999

    for slaveIndex in range (1, 4):
        slaveConfigName = 'Slave' + str(slaveIndex)
        host = config.get(slaveConfigName, 'host')
        time = get_ping_time(host, 1)
        print ('Slave-' + str(slaveIndex) + ' timing: ' + str(time))
        if time < minTiming:
            minTiming = time
            selectedSlave = slaveIndex

    return selectedSlave

def get_command_output(cmd, stderr=STDOUT):

    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def get_ping_time(host, tryCount=3):
    host = host.split(':')[0]
    cmd = 'fping {host} -C {tryCount} -q'.format(host=host, tryCount=tryCount)
    res = [float(x) for x in get_command_output(cmd).strip().split(':')[-1].split() if x != '-']
    if len(res) > 0:
        return sum(res)/len(res)
    else:
        return 9999999

if __name__ == '__main__':
    main()

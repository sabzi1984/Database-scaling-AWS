#!/usr/bin/python3

import socket
import pickle
from time import sleep



def main():

    host = "ec2-100-27-3-168.compute-1.amazonaws.com"
    port = 5001 #proxy port

    print ('connecting to ' + host + ':' + str(port))

    s = socket.socket()
    s.connect((host, port))

    with open('data.csv', 'r') as f:
        next(f) #avoid header
        lines = f.readlines()
        is_insert = True
        cmd_type = 'insert'
        for line in lines:
            line = line.strip('\n')
            Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1= line.split(",")
            if(is_insert):
                cmd = 'INSERT INTO transactions VALUES (' + Series_reference + ", '" + Period + "', '" + Data_value + "', '" + Status + "', '" + Units + "', " + Magnitude + ", " + Series_title_1+ "');"
                is_insert = False
                cmd_type = 'insert'
            else:
                cmd = 'SELECT * FROM transactions WHERE Series_reference = ' + "'" + Series_reference + "';"
                is_insert = True
                cmd_type = 'select'
            obj = {'type': cmd_type, 'command': cmd}
            pickledobj = pickle.dumps(obj)
                s.send(pickledobj)
            data = s.recv(1024)
            print ('Received from server: ' + str(data))

    print ('Will close socket')
    s.close()


if __name__ == '__main__':
    main()

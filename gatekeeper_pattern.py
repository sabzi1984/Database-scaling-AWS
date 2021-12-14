#!/usr/bin/python3

import socket
import pickle
import re

def main():


    listenPort = 5001
    #target = master
    targetHost = "54.237.135.3"
    targetPort = 5001


    send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send.connect((targetHost, targetPort))

    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.bind(('', listenPort))
    listen.listen(1)
    conn, addr = listen.accept()
    print(f"Connection from {addr} has been established.")
    cmd_type = ''
    with conn:
        print('Connected by', addr)

        while True:
            data = conn.recv(2048)

            if not data:
                break
            data = pickle.loads(data)
            if(validate(data)):
                print ('Will pass data')
                pickledobj = pickle.dumps(data)
                send.send(pickledobj)
                response="data validated by gatekeeper"
            else:
                response="data DENIED by gatekeeper")
                print ('Data sent')

            conn.send(response)

    print ('closing socket')
    send.close()
    listen.close()


select_validator = re.compile(r"(^select \* from transactions where Series_reference = [\d]{3,4};)")
insert_validator = re.compile(r"(^insert into transactions values)")


def validate(data):
    cmd_type = data['type']
    cmd=data['command'].lower()
    # print (data)
    if cmd_type=='insert':
        return bool(insert_validator.match(cmd))
    if cmd_type=='select':
        return bool(select_validator.match(cmd))
    return False


if __name__ == '__main__':
    main()

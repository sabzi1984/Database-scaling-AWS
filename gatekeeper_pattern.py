#!/usr/bin/python3

import socket
import pickle
import re

def main():


    host_ip = "54.237.135.3"
    host_port = 5001


    

    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.bind(('', 5001))
    listen.listen(1)
    conn, addr = listen.accept()
    print(f"Connection from {addr} has been established.")
    send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send.connect((host_ip, host_port))
    with conn:
        print('Connected by', addr)

        while True:
            data = conn.recv(2048)

            if not data:
                break
            data = pickle.loads(data)
            if(validate(data)):
                print ('Data Validated by gatekeeper')
                pickledobj = pickle.dumps(data)
                send.send(pickledobj)
                data = s.recv(1024)
                data = pickle.loads(data)
                data['validation_result']="VALID"
                data=pickle.dumps(data)
                conn.send(data)
                
            else:
                response="data DENIED by gatekeeper"
                print ('Data Denied')
                response = pickle.dumps(response)
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

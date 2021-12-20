
#!/usr/bin/python3

import socket
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('operation', help='mode of implementation of proxy, direct, random or custom')
args = parser.parse_args()

operation=args.operation 

def main():

    host = "35.171.55.43" #gatekeeper ip
    port = 5001 #proxy port

    print ('connecting to ' + host + ':' + str(port))

    s = socket.socket()
    s.connect((host, port))
    print("connected")
    

    with open('data.csv', 'r') as f:
        next(f) #avoid header 
        lines = f.readlines()
        if operation=='insert':
            for line in lines:
                line = line.strip('\n')
                Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1= line.split(",")
                cmd = 'insert into transactions values (' +"'"+ Series_reference + "'," + Period + "," + Data_value + ",'" + Status + "','" + Units + "'," + Magnitude + ",'" + Series_title_1+ "');"
                cmd_type = 'insert'
                obj = {'type': cmd_type, 'command': cmd}
                pickledobj = pickle.dumps(obj)
                s.send(pickledobj)
                data = s.recv(1024)
                data=pickle.loads(data)
                print ('insert into master: ' + data['response'])
        
        if operation=='select':
    # with open('data.csv', 'r') as f:
    #     next(f) #avoid header 
    #     lines = f.readlines()
            for line in lines:
                line = line.strip('\n')
                Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1= line.split(",")
                cmd = 'select * from transactions where Series_reference = ' + Series_reference + ";"
                cmd_type = 'select'
                obj = {'type': cmd_type, 'command': cmd}
                pickledobj = pickle.dumps(obj)
                s.send(pickledobj)
                data = s.recv(1024)
                data=pickle.loads(data)
                print (data)
            
            # for (Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1) in data["response"]:
            #            print (f"{Series_reference}, {Period}, {Data_value}, {Status}, {Units}, {Magnitude}, {Series_title_1}")
    print ('closing socket')
    s.close()


if __name__ == '__main__':
    main()

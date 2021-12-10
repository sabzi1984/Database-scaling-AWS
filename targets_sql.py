#!/usr/bin/python
"""Python module that receives TCP requests."""

import socket
import pickle
import mysql.connector
from random import randint


def main():
    """Main."""
    # Initialisation de la connexion
    cnx = mysql.connector.connect(user='root', password='alfi1326', host='0.0.0.0', database='tp3')
    cursor = cnx.cursor()
    print ('Connection to DB opened')

    s = socket.socket()
    s.bind(('',5001))

    print ('Listening port : ' + str(5001))

    s.listen(1)  # Listen to one connection
    c, addr = s.accept()
    print ('connection from: ' + str(addr))

    while True:
        data = c.recv(2048) 
        if not data:
            break

        data = str(data)
        obj = pickle.loads(data)
        cmd_type = obj['type']
        command = obj['command']

        print (command)

        if cmd_type == 'insert':
            cursor.execute(command)
            cnx.commit()
        else:
            cursor.execute(command)
            for (Series_reference, Period, Data_value, Status, Units, Magnitude, Series_title_1) in cursor:
                print (f"{Series_reference}, {Period, Data_value}, {Status, Units}, {Magnitude}, {Series_title_1}")

        response = 'Command ' + command + ' handled by node ' + str(target)
        c.send(response)

    print ('close socket')
    c.close()
    print ('close connection to DB')
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()

#!bin/bash
sudo sysbench --db-driver=mysql --mysql-user='root' --mysql-password=alfi1326 --mysql-db=sakila --table-size=10000 --threads=4 /usr/share/sysbench/oltp_read_write.lua prepare



#!bin/bash
sudo sysbench\
 --db-driver=mysql\
 --mysql-user='root'\
 --mysql-password=alfi1326\
 --mysql-db=sakila\
 --table-size=10000\
 --events=0\
 --time=60\
 --threads=8\
 --tables=1\
 --rate=40\  #rate 
  /usr/share/sysbench/oltp_read_write.lua run
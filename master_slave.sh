#Install mysql on master and slaves
sudo apt update
sudo apt install mysql-server -y
sudo mysql_secure_installation

#in master node
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
[mysqld]
bind-address            = 0.0.0.0
service-id              =  1
binlog-do-db            =  sakila

sudo service mysql restart;
#install sakila on master
sudo mkdir /home/sakila
cd /home/sakila
sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz
sudo tar -xvzf sakila-db.tar.gz
#loginto mysql on master
sudo mysql -u root -p
#configure and monitor sakila on master
SOURCE /home/sakila/sakila-db/sakila-schema.sql;
SOURCE /home/sakila/sakila-db/sakila-data.sql;
USE sakila;
SHOW FULL TABLES;

#create replication user
CREATE USER 'slave1'@'%' IDENTIFIED BY 'alfi1326';
GRANT ALL ON *.* TO 'slave1'@'%'; 

CREATE USER 'slave2'@'%' IDENTIFIED BY 'alfi1326';
GRANT ALL  ON *.* TO 'slave2'@'%'; 

CREATE USER 'slave3'@'%' IDENTIFIED BY 'alfi1326';
GRANT ALL ON *.* TO 'slave3'@'%'; 

CREATE USER 'proxy'@'%' IDENTIFIED BY 'alfi1326';
GRANT ALL ON *.* TO 'proxy'@'%'; 
ALTER USER 'proxy'@'%' IDENTIFIED WITH mysql_native_password BY 'alfi1326';

FLUSH PRIVILEGES;

FLUSH TABLES WITH READ LOCK;

SHOW MASTER STATUS;
#the parametrs used for slave config
#File == binlog.000115
# position== 1362512

UNLOCK TABLES;

#install sakila on slaves
sudo mkdir /home/sakila
cd /home/sakila
sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz
sudo tar -xvzf sakila-db.tar.gz
#loginto mysql on master
sudo mysql -u root -p
#configure and monitor sakila on master
SOURCE /home/sakila/sakila-db/sakila-schema.sql;
SOURCE /home/sakila/sakila-db/sakila-data.sql;
USE sakila;
SHOW FULL TABLES;


sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
#slave1
service-id              =  2
binlog-do-db            =  sakila
relay_log = /var/log/mysql/mysql-relay-bin.log
uncomment log_bin
#slave2
service-id              =  4
binlog-do-db            =  sakila
relay_log = /var/log/mysql/mysql-relay-bin.log
uncomment log_bin

#slave3
service-id              =  3
binlog-do-db            =  sakila
relay_log = /var/log/mysql/mysql-relay-bin.log
uncomment log_bin

#restrat mysql on slaves
sudo service mysql restart

#conncect again to mysql on slave1
sudo mysql -u root -p
CHANGE MASTER TO MASTER_HOST='34.202.223.21', MASTER_USER='slave1', MASTER_PASSWORD='alfi1326', MASTER_LOG_FILE='mysql-bin.000014', MASTER_LOG_POS= 197009;




CHANGE MASTER TO MASTER_HOST='34.202.223.21', MASTER_USER='slave2', MASTER_PASSWORD='alfi1326', MASTER_LOG_FILE='mysql-bin.000014', MASTER_LOG_POS= 197009;
# ERROR 29 (HY000): File '/var/log/mysql-relay-bin.index' not found (OS errno 13 - Permission denied)
ALTER USER 'slave2'@'%' IDENTIFIED WITH mysql_native_password BY 'alfi1326';


CHANGE MASTER TO MASTER_HOST='34.202.223.21', MASTER_USER='slave3', MASTER_PASSWORD='alfi1326', MASTER_LOG_FILE='mysql-bin.000014', MASTER_LOG_POS= 197009;
ALTER USER 'slave3'@'%' IDENTIFIED WITH mysql_native_password BY 'alfi1326';



tp3 database
 mysql-bin.000013
 326

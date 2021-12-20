#Install mysql
sudo apt update
sudo apt install mysql-server -y
sudo mysql_secure_installation
#install sakila
sudo mkdir /home/sakila
cd /home/sakila
sudo wget https://downloads.mysql.com/docs/sakila-db.tar.gz
sudo tar -xvzf sakila-db.tar.gz
#loginto mysql
sudo mysql -u root -p
#configure and monitor sakila
SOURCE /home/sakila/sakila-db/sakila-schema.sql;
SOURCE /home/sakila/sakila-db/sakila-data.sql;
USE sakila;
SHOW FULL TABLES;
#sysbench
sudo apt-get install sysbench -y
#sysbench options
man sysbench

service mysql start && mysql -uroot -e "CREATE DATABASE SqliDB; CREATE USER 'sqli-server'@'localhost' IDENTIFIED BY 'Bx117@\$YaML**\!'; GRANT ALL PRIVILEGES ON SqliDB.* TO 'sqli-server'@'localhost'; USE SqliDB; CREATE TABLE Users (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, User varchar(20), Password varchar(100)); INSERT INTO Users (User,Password) VALUES ('admin','708DxSUf2O%C*pLWNI'); SET PASSWORD FOR root@'localhost' = PASSWORD('Tl6@$0lxyaA@#--Jl3NMA@1-9283D')";



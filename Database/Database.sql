create database demo;
use demo;
create table Adgroup(
adgp_id varchar(11) not null,
adgp_name varchar(255) not null,
campaign_id varchar(11) not null,
campaign_name varchar(11) not null,
account_id varchar(11) not null,
primary key (adgp_id),
FOREIGN KEY (account_id) REFERENCES Account(Account_id)
);
create table Account(
Account_id varchar(11) not null,
user_id varchar(20) not null,
Media varchar(50) not null,
primary key (Account_id),
FOREIGN KEY (user_id) REFERENCES User(User_id)
);
create table User(
User_id varchar(20) not null,
Slack_id varchar(20) not null,
PIC_name varchar(50) not null,
primary key (User_id)
);

INSERT INTO User
VALUES ('111111','@U063ADBHVTR','Doan Nguyen Duy');
INSERT INTO Account
VALUES ('111','111111','Google');
INSERT INTO Adgroup
VALUES ('333333','fruit','33333','Food','111');





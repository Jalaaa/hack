USE plates_db;
CREATE TABLE IF NOT EXISTS artikel (
     id INT AUTO_INCREMENT PRIMARY KEY,
     name VARCHAR(255) NOT NULL,
     default_price DECIMAL(10,2),
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


# create table mit namen bugitems
create table IF NOT EXISTS bugitems (id INT NOT NULL auto_increment, primary key (id));
alter table bugitems add column priority INT not null;
alter table bugitems add column username VARCHAR(30) not null;
alter table bugitems add column title VARCHAR(64) not null;
alter table bugitems add column description VARCHAR(512) not null;

# create table mit namen bugusers
create table IF NOT EXISTS bugusers(id int not null auto_increment, primary key(id));
alter table bugusers add column username varchar(30) not null;
alter table bugusers add column email_address varchar(50) not null;
alter table bugusers add column password varchar(60) not null;

CREATE TABLE IF NOT EXISTS plateusers (id INT NOT NULL auto_increment, primary key (id));
alter table plateusers add column firstName varchar(30) NOT NULL;
alter table plateusers add column lastName varchar(30) NOT NULL;
alter table plateusers add column username varchar(30) NOT NULL;
alter table plateusers add column email varchar(30) NOT NULL;
alter table plateusers add column password varchar(30) NOT NULL;


CREATE TABLE IF NOT EXISTS gerplates (id INT NOT NULL auto_increment, primary key (id));
alter table gerplates add column kuerzel varchar(5) NOT NULL;
alter table gerplates add column stadt varchar(50) NOT NULL;
alter table gerplates add column bundesland varchar(30);
alter table gerplates add column country varchar(600);


# make entrfries unique, see ticketusers above
ALTER TABLE bugusers ADD UNIQUE (username);
ALTER TABLE bugusers ADD UNIQUE (email_address);
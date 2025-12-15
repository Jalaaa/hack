USE plates_db;

# show tables of current database
show tables;

# get details of table
describe bugitems;

#insert into bugitems table
INSERT INTO bugitems (id, priority, username, title, description) VALUES (1, 2, 'Luke', 'GUI Problem', 'GUI really not working');
INSERT INTO bugitems (id, priority, username, title, description) VALUES (2, 2, 'Nat', 'Backend Problem', 'Backend not starting');
INSERT INTO bugitems (id, priority, username, title, description) VALUES (3, 3, 'Anakin', 'Totally Broke', 'Nothing works out');

#insert into ticketusers table
INSERT INTO bugusers (id, username, email_address, password) VALUES (1, 'Derk', 'de@alb.de', 'pass');
INSERT INTO bugusers (id, username, email_address, password) VALUES (2, 'Natalie', 'na@alb.de', 'pass');
INSERT INTO bugusers (id, username, email_address, password) VALUES (3, 'Anaking', 'an@alb.de', 'pass');



#check content of table
select * from bugitems;
select * from bugusers;
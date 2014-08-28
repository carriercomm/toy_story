CREATE KEYSPACE toystory WITH REPLICATION = { 'class' : 'SimpleStrategy' , 'replication_factor' :  1}  ;
USE toystory;

CREATE TABLE repos (
    repo_name VARCHAR,
    PRIMARY KEY (repo_name)
); 



\c postgres
DROP DATABASE IF EXISTS CommentCloud;
DROP USER IF EXISTS simple_user;

CREATE USER simple_user WITH LOGIN ENCRYPTED PASSWORD 'simple_user';
CREATE DATABASE CommentCloud;


\c postgres
DROP DATABASE IF EXISTS CommentCloud;
DROP USER IF EXISTS simple_user;

CREATE USER simple_user WITH LOGIN PASSWORD 'simple_user';
CREATE DATABASE CommentCloud;

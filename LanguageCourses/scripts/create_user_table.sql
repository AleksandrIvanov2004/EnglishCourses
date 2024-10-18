CREATE TABLE users (
    id serial4,
    age int,
    email varchar unique,
    password varchar,
    first_name varchar,
    second_name varchar
);
INSERT INTO users (age, email, password, first_name, second_name) VALUES
(25, 'ivanov@example.com', 'password123', 'Иван', 'Иванов'),
(30, 'petrov@example.com', 'password456', 'Петр', 'Петров');
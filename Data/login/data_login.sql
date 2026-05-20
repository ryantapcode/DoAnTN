CREATE TABLE login_data (
    email VARCHAR(255),
    password VARCHAR(255),
    expected TEXT
);

INSERT INTO login_data (email, password, expected) VALUES
('seconhungconcaphaigiacho', '1111', 'Please include an ''@'' in the email address. ''seconhungconcaphaigiacho'' is missing an ''@''.'),
('fake@abc.com', '', 'Please fill out this field.'),
('', '123456', 'Please fill out this field.'),
('', '', 'Please fill out this field.');
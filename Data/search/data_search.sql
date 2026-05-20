CREATE TABLE search_data (
    search VARCHAR(255),
    expected TEXT
);

INSERT INTO search_data (search, expected) VALUES
('tee', 'Có 150 sản phẩm cho tìm kiếm'),
('áo', 'Không tìm thấy "". Vui lòng kiểm tra chính tả'),
('123456', 'Không tìm thấy "123456". Vui lòng kiểm tra chính tả'),
('#%$@%', 'Không tìm thấy "#%$@%". Vui lòng kiểm tra chính tả'),
('tê', 'Có 150 sản phẩm cho tìm kiếm'),
('     bag', 'Có 2 sản phẩm cho tìm kiếm'),
('', 'Please fill out this field.'),
('SWE SPIKE BOXY TEE – WHITE', 'Có 1 sản phẩm cho tìm kiếm');
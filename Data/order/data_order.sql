CREATE TABLE checkout_data (
    keyword VARCHAR(255),
    name VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    province VARCHAR(100),
    address TEXT,
    expected VARCHAR(100)
);

INSERT INTO checkout_data (keyword, name, phone, email, province, address, expected) VALUES
('SWE CHERRY BOXY TEE - BLACK', '', '0912345678', 'namanh@gmail.com', 'Hà Nội', 'Thị trấn Xuân Mai, Huyện Chương Mỹ, Hà Nội', 'name'),
('SWE CROSS BOXY TEE - WHITE', 'bình', '', 'namanh@gmail.com', 'Hà Nội', 'Thị trấn Xuân Mai, Huyện Chương Mỹ, Hà Nội', 'phone'),
('SWE KNIT POLO - GRAY', 'an', '0977364522', 'binhyennhungphutgiay', 'Hà Nội', 'Thị trấn Xuân Mai, Huyện Chương Mỹ, Hà Nội', 'email'),
('SWE KNIT POLO - NAVY', 'an', '0977364536', 'chiecgiuong@gmail.com', '', 'Thị trấn Xuân Mai, Huyện Chương Mỹ, Hà Nội', 'province'),
('SWE SCRIPT JACKET - BEIGE', 'mai', '097523746', 'test@gmail.com', 'Hà Nội', 'Thị trấn Xuân Mai, Huyện Chương Mỹ, Hà Nội', 'phone');
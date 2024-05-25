use [BD-Project];
-- Products
    INSERT INTO PRODUCTS
    VALUES
        -- ELETRONICS
        (5000, 'Raspberry PI 5', 'Raspberry PI novo', 
            60, 'electronics', 25, 1),
        (5001, 'Condensador 470 μF', 'Condensador com capacidade 470 μF 50V',
            0.85, 'electronics', 1000, 1),
        (5002, 'Multimetro', 'Multimetro digital profissional',
            25, 'electronics', 15, 1),
        (5003, 'Cabos de ligação', 'Conjunto de 50 cabos de ligação',
            5, 'electronics', 200, 1),

        -- CLOTHING
        (5010, 'T-shirt DETI', 'T-shirt de poliéster',
            20, 'clothing', 50, 1),
        (5011, 'Pullover DETI', 'Pullover com Logo do DETI',
            30, 'clothing', 80, 1),
        (5012, 'Casaco DETI', 'Casaco de Parka DETI ', 
            40, 'clothing', 25, 1),
        (5013, 'T-shirt UA', 'T-shirt de algodão da Universidade de Aveiro',
            15, 'clothing', 150, 1),

        -- FOOTWEAR
        (5030, 'Sapatilhas Adidas', 'Sapatilhas Adidas VS Pace', 
            35, 'footwear', 15, 1),
        (5031, 'Chinelos Havaianas', 'Chinelos Havaianas originais',
            25, 'footwear', 25, 1),

        -- KITCHEN
        (5040,  'Torradeira usada', 'Torradeira em 2ª Mão, pertencente a aluno de ERASMUS',
            10, 'kitchen', 3, 1),
        (5041, 'Tostadeira usada', 'Tostadeira em 2ª Mão, pertencente a aluno de ERASMUS',
            7, 'kitchen', 4, 1),
        (5042, 'Ferro de Engomar usado', 'Ferro de Engomar em 2ª Mão, pertencente a aluno de ERASMUS',
            15, 'kitchen', 1, 1),
        (5043, 'Kit cozinha', 'Panelas, tachos, frigideira em 2ª Mão, pertencente a aluno de ERASMUS',
            30,'kitchen', 1, 1),

        -- ACCESSORIES
        (5050, 'Colar Corrente', 'Colar Corrente DETI ',
            20, 'accessories', 15, 1),
        (5051, 'Dog Tag prateado', 'Dog tag prateado com simbolo do DETI', 
            30, 'accessories', 20, 1),

        -- SOFTWARE
        (5060, 'Licença Matlab', 'Licença Matlab vitalícia',
            100, 'software', 100, 1),
        (5061, 'Licença Office 365', 'Licença Office 365 3 anos', 
            30, 'software', 250, 1),

        -- FITNESS
        (5070, 'Calças Fato de Treino', 'Calças Fato de Treino com Logo do DETI', 
            30, 'fitness', 15, 1),
        (5071, 'Dumbbell', 'Dumbbell com peso ajustável 0-50kg', 
            80, 'fitness', 10, 1),
        (5072, 'Creatina 500g', 'Creatina Monohidratada creapure',
            25, 'fitness', 256, 1);

-- Users
    INSERT INTO USERS
    VALUES
        (10000, 'Jorge Costa', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10001, 'Pedro Abrunhosa', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10002, 'Tomás Shelby', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10003, 'Artur Campos', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10004, 'J1mmy', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10005, 'Ingus', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10006, 'Jorge Torvesta', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10007, 'Oda J. Block', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10008, 'Timmy Thomas', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0),
        (10009, 'Rendi Mento', 'hashedpassword', null, null, 'email', 'totpSecretKey', '1970-01-01', 0);

-- Emergency_codes
-- Can Ignore for now, only accessible accounts really need

-- Orders
    INSERT INTO ORDERS
    VALUES 
        (1, 10001, 0, 'Fake Address', '2024-02-14'),
        (2, 10005, 0, 'Fake Address', '2024-03-12'),
        (3, 10009, 0, 'Fake Address', '2024-05-02'),
        (4, 10003, 0, 'Fake Address', '2024-04-18'),
        (5, 10000, 0, 'Fake Address', '2024-03-22'),
        (6, 10007, 0, 'Fake Address', '2024-02-27'),
        (7, 10002, 0, 'Fake Address', '2024-04-05'),
        (8, 10004, 0, 'Fake Address', '2024-05-10'),
        (9, 10008, 0, 'Fake Address', '2024-02-21'),
        (10, 10006, 0, 'Fake Address', '2024-03-29'),
        (11, 10001, 0, 'Fake Address', '2024-04-25'),
        (12, 10005, 0, 'Fake Address', '2024-03-08'),
        (13, 10009, 0, 'Fake Address', '2024-02-17'),
        (14, 10003, 0, 'Fake Address', '2024-05-18'),
        (15, 10000, 0, 'Fake Address', '2024-04-12'),
        (16, 10007, 0, 'Fake Address', '2024-03-03'),
        (17, 10002, 0, 'Fake Address', '2024-05-14'),
        (18, 10004, 0, 'Fake Address', '2024-02-23'),
        (19, 10008, 0, 'Fake Address', '2024-04-01'),
        (20, 10006, 0, 'Fake Address', '2024-05-05');


-- Products Ordered
    INSERT INTO PRODUCTS_ORDERED
    VALUES 
        (1, 5000, 2),
        (1, 5011, 1),
        (1, 5040, 3),
        (2, 5010, 2),
        (2, 5042, 1),
        (2, 5072, 3),
        (3, 5003, 1),
        (3, 5012, 2),
        (3, 5061, 1),
        (4, 5013, 3),
        (4, 5050, 2),
        (4, 5070, 1),
        (5, 5030, 1),
        (5, 5051, 2),
        (5, 5060, 3),
        (6, 5001, 2),
        (6, 5043, 1),
        (7, 5002, 3),
        (7, 5031, 2),
        (8, 5050, 1),
        (8, 5071, 2),
        (9, 5010, 1),
        (9, 5060, 3),
        (10, 5041, 1),
        (10, 5072, 2),
        (11, 5012, 1),
        (11, 5051, 2),
        (11, 5061, 3),
        (12, 5002, 2),
        (12, 5042, 1),
        (13, 5000, 3),
        (13, 5071, 2),
        (14, 5013, 1),
        (14, 5040, 2),
        (14, 5050, 3),
        (15, 5011, 1),
        (15, 5060, 2),
        (16, 5030, 2),
        (16, 5072, 1),
        (17, 5041, 3),
        (17, 5051, 2),
        (18, 5003, 1),
        (18, 5043, 3),
        (19, 5001, 2),
        (19, 5010, 1),
        (19, 5070, 3),
        (20, 5031, 1),
        (20, 5050, 2);

-- Reviews
    INSERT INTO Reviews
    VALUES
        (1, 5000, 10001, 'Great product!', 5, '2024-02-20'),
        (2, 5072, 10005, 'Very satisfied', 4, '2024-03-15'),
        (3, 5061, 10009, 'Not bad', 3, '2024-05-10'),
        (4, 5050, 10003, 'Excellent quality', 5, '2024-04-20'),
        (5, 5060, 10000, 'Quite good', 4, '2024-03-25'),
        (6, 5043, 10007, 'Needs improvement', 2, '2024-03-01'),
        (7, 5031, 10002, 'Very good', 4, '2024-04-07'),
        (8, 5071, 10004, 'Top notch', 5, '2024-05-15'),
        (9, 5060, 10008, 'Just okay', 3, '2024-02-25'),
        (10, 5072, 10006, 'Perfect fit', 5, '2024-04-01');
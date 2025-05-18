
-- DML

-- User Table
INSERT INTO User VALUES
('U001', 'tahsin52', 'pass123', 'Tahsin', 'Karcı'),
('U002', 'ardaguler', '123pass', 'Arda', 'Güler'),
('U003', 'wishimay', 'password1', 'Hasan', 'Karcı'),
('U004', 'james007', 'bond7', 'James', 'Bond'),
('U005', 'whoami', 'donot', 'Kim', 'Chen');

-- Addresses Table
INSERT INTO Addresses VALUES
('A01', 'Cumhuriyet Sok', '17', 'Maple Home', '34646', 'U001'),
('A02', 'Zafer Sok', '12A', 'Oak Residence', '22222', 'U002'),
('A03', 'Milli Sok', '56C', 'Pine Place', '33333', 'U001'), -- a user can have different addresses
('A04', 'Dram Sok', '7D', 'Elm House', '44444', 'U004'),
('A05', 'Eren Sok', '9A', 'Cedar Villa', '55555', 'U005');

-- Phone Table
INSERT INTO Phone VALUES
('5551112222', 'U001'),
('5553334444', 'U002'),
('5555556666', 'U003'),
('5557778888', 'U004'),
('5559990000', 'U005');

-- Customer Table
INSERT INTO Customer VALUES
('U003', CURRENT_TIMESTAMP),
('U005', CURRENT_TIMESTAMP),
('U004', CURRENT_TIMESTAMP);

-- Manager Table
INSERT INTO Manager VALUES
('U002', 4900.00),
('U001', 4800.00);

-- Restaurant Table
INSERT INTO Restaurant VALUES
('R001', 'Burger King', '123 Flame St', 'Spicetown', 'spicy@grill.com', '555-1234', 'BBQ'),
('R002', 'HD İskender', '456 Water Ave', 'Seaville', 'ocean@bites.com', '555-5678', 'Seafood'),
('R003', 'Sushico', '789 Noodle Rd', 'Pastaville', 'pasta@place.com', '555-9012', 'Italian'),
('R004', 'Pizza Bulls', '101 Beef Blvd', 'BurgerCity', 'barn@burger.com', '555-3456', 'Fast Food'),
('R005', 'Green Salas', '202 Vegan St', 'Greenville', 'leaf@green.com', '555-7890', 'Vegan');

-- MenuItem Table
INSERT INTO MenuItem VALUES
('M001', 'BBQ Burger', 'Grilled beef patty with BBQ sauce and crispy onions', 15.99),
('M002', 'İskender', 'Traditional Turkish dish with döner meat over pita, yogurt, and tomato sauce', 18.50),
('M003', 'California Roll', 'Sushi roll with crab, avocado, and cucumber', 12.75),
('M004', 'Margherita', 'Classic pizza with tomato sauce, mozzarella, and fresh basil', 9.99),
('M005', 'Penne with Chicken', 'Penne pasta tossed with grilled chicken and creamy tomato sauce', 11.25);


-- Discount Table
INSERT INTO Discount VALUES
('D001', 'M001', '2025-05-01 00:00:00', '2025-05-31 23:59:59', 2.00),
('D002', 'M002', '2025-05-05 00:00:00', '2025-06-05 23:59:59', 3.50),
('D003', 'M003', '2025-05-10 00:00:00', '2025-05-20 23:59:59', 1.75),
('D004', 'M004', '2025-05-01 00:00:00', '2025-05-15 23:59:59', 1.00),
('D005', 'M005', '2025-05-03 00:00:00', '2025-06-01 23:59:59', 1.25);

-- Cart Table
INSERT INTO Cart VALUES
('C001', 'open', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 25.00),
('C002', 'closed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 35.00),
('C003', 'open', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 20.00),
('C004', 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 15.50),
('C005', 'open', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 40.75);

-- Sales Table
INSERT INTO Sales VALUES
('S001', 'paid', 25.00),
('S002', 'paid', 35.00),
('S003', 'refunded', 20.00),
('S004', 'pending', 15.50),
('S005', 'paid', 40.75);

-- Rating Table
INSERT INTO Rating VALUES
('RA001', 5, 'Excellent food!', 'R001'),
('RA002', 4, 'Very tasty!', 'R002'),
('RA003', 3, 'It was okay.', 'R003'),
('RA004', 2, 'Could be better.', 'R004'),
('RA005', 1, 'Not good.', 'R005');

-- leaves Table
INSERT INTO leaves VALUES
('RA001', 'U001'),
('RA002', 'U002'),
('RA003', 'U003'),
('RA004', 'U004'),
('RA005', 'U005');

-- makes Table
INSERT INTO makes VALUES
('S001', 'U001', CURRENT_TIMESTAMP),
('S002', 'U002', CURRENT_TIMESTAMP),
('S003', 'U003', CURRENT_TIMESTAMP),
('S004', 'U004', CURRENT_TIMESTAMP),
('S005', 'U005', CURRENT_TIMESTAMP);

-- places Table
INSERT INTO places VALUES
('S001', 'C001'),
('S002', 'C002'),
('S003', 'C003'),
('S004', 'C004'),
('S005', 'C005');

-- contains Table
INSERT INTO contains VALUES
('C001', 'M001'),
('C002', 'M002'),
('C003', 'M003'),
('C004', 'M004'),
('C005', 'M005');

-- offers Table
INSERT INTO offers VALUES
('M001', 'R001'),
('M002', 'R002'),
('M003', 'R003'),
('M004', 'R004'),
('M005', 'R005');

-- receives Table
INSERT INTO receives VALUES
('C001', 'R001'),
('C002', 'R002'),
('C003', 'R003'),
('C004', 'R004'),
('C005', 'R005');

-- manages Table
INSERT INTO manages VALUES
('U001', 'R001'),
('U002', 'R002'),
('U003', 'R003'),
('U004', 'R004'),
('U005', 'R005');

-- checks Table
INSERT INTO checks VALUES
('S001', 'U001'),
('S002', 'U002'),
('S003', 'U003'),
('S004', 'U004'),
('S005', 'U005');

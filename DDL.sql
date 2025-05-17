CREATE Schema If Not exists project;

USE project;

-- Entites --
CREATE TABLE User (
  user_id     VARCHAR(10)    PRIMARY KEY,
  username    VARCHAR(50)    NOT NULL UNIQUE,
  password    VARCHAR(255)   NOT NULL,
  first_name  VARCHAR(50),
  last_name   VARCHAR(50)
);

CREATE TABLE Addresses (
  address_id  VARCHAR(10),
  street_name VARCHAR(100),
  home_no     VARCHAR(10),
  home_name   VARCHAR(50),
  postal_code VARCHAR(10),
  user_id     VARCHAR(10)    NOT NULL,
  PRIMARY KEY (user_id, address_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id)  ON DELETE CASCADE
);

CREATE TABLE Phone (
  phone_number VARCHAR(20),
  user_id      VARCHAR(10)   NOT NULL,
  PRIMARY KEY (user_id, phone_number),
  FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Customer (
  user_id VARCHAR(10)    PRIMARY KEY,
  signup_date TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Manager (
  user_id  VARCHAR(10)    PRIMARY KEY,
  salary      DECIMAL(10,2),
  FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Restaurant (
  restaurant_id VARCHAR(10)  PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  address_line  VARCHAR(200),
  city          VARCHAR(100),
  email         VARCHAR(100),
  phone         VARCHAR(20),
  cuisine_type  VARCHAR(50)
);

CREATE TABLE MenuItem (
  menu_item_id  VARCHAR(10)  PRIMARY KEY,
  name          VARCHAR(100) NOT NULL,
  description   TEXT,
  price         DECIMAL(10,2)
);

CREATE TABLE Discount (
  discount_id  VARCHAR(10),
  menu_item_id  VARCHAR(10),
  start_date   TIMESTAMP,
  finish_date  TIMESTAMP,
  amount       DECIMAL(5,2),
  PRIMARY KEY (discount_id  , menu_item_id),
  FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id) ON DELETE CASCADE
);


CREATE TABLE Cart (
  cart_id       VARCHAR(10)  PRIMARY KEY,
  status        VARCHAR(20),
  created_at    TIMESTAMP,
  updated_at    TIMESTAMP,
  total_amount  DECIMAL(10,2)
);



CREATE TABLE Sales (
  sale_id     VARCHAR(10)    PRIMARY KEY,
  status      VARCHAR(20),
  price       DECIMAL(10,2)
);

CREATE TABLE Rating (
  rating_id     VARCHAR(10)  PRIMARY KEY,
  star          INT,
  comment       TEXT,
  restaurant_id VARCHAR(10),
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id)
);

-- Relations --

CREATE TABLE leaves (
  rating_id    VARCHAR(10),
  user_id      VARCHAR(10),
  PRIMARY KEY (user_id, rating_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (rating_id) REFERENCES Rating(rating_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE makes (
  sale_id     VARCHAR(10),
  user_id      VARCHAR(10),
  date TIMESTAMP,
  PRIMARY KEY (sale_id, user_id),
  FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (sale_id) REFERENCES Sales(sale_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE places (
  sale_id     VARCHAR(10),
  cart_id       VARCHAR(10),
  PRIMARY KEY (sale_id, cart_id),
  FOREIGN KEY (sale_id) REFERENCES Sales(sale_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (cart_id) REFERENCES Cart(cart_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE contains (
  cart_id       VARCHAR(10),
  menu_item_id  VARCHAR(10),
  PRIMARY KEY (cart_id, menu_item_id),
  FOREIGN KEY (cart_id) REFERENCES Cart(cart_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE offers (
  menu_item_id  VARCHAR(10),
  restaurant_id      VARCHAR(10),
  PRIMARY KEY (menu_item_id, restaurant_id),
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (menu_item_id) REFERENCES MenuItem(menu_item_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE receives (
  cart_id       VARCHAR(10),
  restaurant_id      VARCHAR(10),
  PRIMARY KEY (cart_id , restaurant_id),
  FOREIGN KEY (cart_id ) REFERENCES Cart(cart_id ) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE manages (
  user_id       VARCHAR(10),
  restaurant_id      VARCHAR(10),
  PRIMARY KEY (user_id , restaurant_id),
  FOREIGN KEY (user_id ) REFERENCES User(user_id ) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (restaurant_id) REFERENCES Restaurant(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE checks (
  sale_id      VARCHAR(10),
  user_id     VARCHAR(10),
  PRIMARY KEY (sale_id , user_id),
  FOREIGN KEY (sale_id ) REFERENCES Sales(sale_id ) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);








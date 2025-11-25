drop database if exists cs3560;
create database if not exists cs3560;
use cs3560;

create table owners (
ownerID int not null auto_increment,
username varchar(150) not null,
password varchar(150) not null,
full_name varchar(150) not null,
email varchar(150) not null,
primary key (ownerID)
);

create table customers (
customerID int not null auto_increment,
username varchar(150) not null,
password varchar(150) not null,
full_name varchar(150) not null,
email varchar(150) not null,
primary key (customerID)
);

create table restaurant (
restaurantID int not null auto_increment,
name varchar(150) not null,
email varchar(150) not null,
address varchar(150) not null,
phoneNumber varchar(150) not null,
priceRange varchar(150) not null,
operatingHours varchar(150) not null,
cuisine varchar(150) not null,
ownerID int not null,
primary key (restaurantID),
foreign key (ownerID) references owners(ownerID)
);

create table reviews (
reviewID int not null auto_increment,
reviewDate date not null,
customerID int not null,
restaurantID int not null,
rating int not null check (rating between 1 and 5),
reviewContent varchar(150),
primary key (reviewID),
foreign key (restaurantID) references restaurant(restaurantID) on delete cascade,
foreign key (customerID) references customers(customerID) on delete cascade
);

create table replies (
replyID int not null auto_increment,
reviewID int not null,
ownerID int not null,
replyContent varchar(150) not null,
replyDate date not null,
primary key (replyID),
foreign key (reviewID) references reviews(reviewID),
foreign key (ownerID) references owners(ownerID)
);

-- Insert into the new Owners table (OwnerID is auto_incrementing)
INSERT INTO Owners (username, password, full_name, email)
VALUES
('mario','ownerpass','Mario Lopez','mario@touchngo.com'),  -- New OwnerID 1
('rrios','train123','Ricky Rios','ricky@gmail.com'),       -- New OwnerID 2
('cchavez','ballpass','Chris Chavez','chris.chavez@gmail.com'); -- New OwnerID 3

-- Insert into the new Customers table (customerID is auto_incrementing)
INSERT INTO Customers (username, password, full_name, email)
VALUES
('dcarbajal','pass123','David Carbajal','david@gmail.com'),     -- New customerID 1
('jhernandez','pass456','Jose Hernandez','jose@gmail.com'),     -- New customerID 2
('csantana','pass789','Carlos Santana','carlos@gmail.com');    -- New customerID 3


INSERT INTO restaurant (name,email,address,phoneNumber,priceRange,operatingHours,cuisine,ownerID)
VALUES
('Touch N Go Grill','info@touchngo.com','123 Soccer Way Tustin, CA','7145551234','$$','Mon-Fri 9am-9pm','American',1),
('Laguna Eats','contact@lagunaeats.com','456 Beach Blvd Laguna, CA','9495555678','$$$','Daily 8am-10pm','Seafood',2),
('Corona Bistro','info@coronabistro.com','789 River Rd, Corona, CA','9515553344','$$','Mon-Sun 11am-9pm','Mexican',3);

-- Corrected reviews inserts using the new customerID mapping and customerID column
INSERT INTO reviews (reviewDate, customerID, restaurantID, rating, reviewContent)
VALUES
('2025-10-01',1,1,5,'Amazing food and excellent staff.'),  -- dcarbajal (1)
('2025-10-02',2,2,3,'Great seafood but a bit pricey.'),  -- jhernandez (2)
('2025-10-03',3,3,3,'Good tacos, but service was slow.');  -- csantana (3)

-- Corrected replies inserts using the new ownerID mapping and ownerID column
INSERT INTO replies (reviewID, ownerID, replyContent, replyDate)
VALUES
(1,1,'Thanks David! We appreciate your support!','2025-10-02'),    -- Mario (1)
(2,2,'Glad you liked the seafood! We’ll review our prices.','2025-10-03'),  -- Mario (1)
(3,3,'Thanks for the feedback, Carlos. We’re training new staff.','2025-10-04');-- Ricky (2)
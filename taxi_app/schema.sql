DROP TABLE IF EXISTS tblUsers;
DROP TABLE IF EXISTS tblUserNotificationSettings;
DROP TABLE IF EXISTS tblUserSettings;
DROP TABLE IF EXISTS tblReviews;
DROP TABLE IF EXISTS tblDrivers;
DROP TABLE IF EXISTS tblRides;

CREATE TABLE IF NOT EXISTS tblUsers (
    user_id integer PRIMARY KEY AUTOINCREMENT,
    username varchar(30) NOT NULL,
    password varchar(30) NOT NULL,
    email varchar(30) NOT NULL,
    date_of_birth date NOT NULL
);
CREATE TABLE IF NOT EXISTS tblUserNotificationSettings (
    user_id INTEGER PRIMARY KEY,
    push_notifications BOOLEAN NOT NULL DEFAULT 1,
    enroute_driver_updates BOOLEAN NOT NULL DEFAULT 1,
    distance integer NOT NULL DEFAULT 1,
    time integer NOT NULL DEFAULT 1,
    special_offers BOOLEAN NOT NULL DEFAULT 1,
    booking_receipts BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES tblUsers (user_id)
);
CREATE TABLE IF NOT EXISTS tblUserSettings (
    user_id INTEGER PRIMARY KEY,
    nightmode BOOLEAN NOT NULL DEFAULT 0,
    text_to_speech BOOLEAN NOT NULL DEFAULT 0,
    text_colour_1 varchar(7) NOT NULL DEFAULT '#000000',
    text_colour_2 varchar(7) NOT NULL DEFAULT '#0000FF',
    background_colour varchar(7) NOT NULL DEFAULT '#FFFFFF',
    FOREIGN KEY (user_id) REFERENCES tblUsers (user_id)
);
CREATE TABLE IF NOT EXISTS tblReviews (
    review_id  integer PRIMARY KEY AUTOINCREMENT,
    user_id  integer NOT NULL,
    title varchar(30) NOT NULL,
    body varchar(200) NOT NULL,
    rating integer NOT NULL,
    driver_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tblUsers (user_id),
    FOREIGN KEY (driver_id) REFERENCES tblDrivers (driver_id)
);
CREATE TABLE IF NOT EXISTS tblDrivers (
    driver_id integer PRIMARY KEY AUTOINCREMENT,
    firstname varchar(20) NOT NULL,
    surname varchar(20) NOT NULL,
    car_manufacturer varchar(20) NOT NULL,
    car_model varchar(20) NOT NULL,
    rides_completed integer NOT NULL DEFAULT 0,
    average_rating  decimal(3, 2) NOT NULL DEFAULT 0,
    latitude real NOT NULL,
    longitude real NOT NULL
);
CREATE TABLE IF NOT EXISTS tblRides (
    ride_id integer PRIMARY KEY AUTOINCREMENT,
    user_id varchar(20) NOT NULL,
    driver_id varchar(20) NOT NULL,
    date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    review_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES tblUsers (user_id),
    FOREIGN KEY (driver_id) REFERENCES tblDrivers (driver_id),
    FOREIGN KEY (review_id) REFERENCES tblReviews (review_id)
);
INSERT INTO tblUsers (username, password, email, date_of_birth)
VALUES ('Guest', 'Guest', 'guest@guest.com' , 1/1/1)
;
INSERT INTO tblUserNotificationSettings (user_id)
VALUES (1)
;
INSERT INTO tblUserSettings (user_id)
VALUES (1)
;
INSERT INTO tblReviews (user_id, title, body, driver_id, rating)
VALUES (1, 'Brilliant', 'I thoroughly enjoyed the ride; even had a really good conversation with the driver.', 1, 5)
;
INSERT INTO tblReviews (user_id, title, body, driver_id, rating)
VALUES (1, 'Very Good', 'Quite quick journey.', 2, 4)
;
INSERT INTO tblRides (user_id, driver_id, review_id, date)
VALUES (1, 1, 1, "2024-05-08 12:24:48")
;
INSERT INTO tblRides (user_id, driver_id, review_id, date)
VALUES (1, 2, 2, "2024-05-12 18:48:28")
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Lee', 'Cattermole', 'Volkswagen', 'Polo', (SELECT coalesce(avg(rating), 0) FROM tblReviews WHERE driver_id = 1),
        (SELECT coalesce(count(rating), 0)   FROM tblReviews WHERE driver_id = 1), 54.880751, -1.413042)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Daisy', 'Renton', 'Mazda', 'MX-30', (SELECT coalesce(avg(rating), 0)  FROM tblReviews WHERE driver_id = 2),
        (SELECT coalesce(count(rating), 0)   FROM tblReviews WHERE driver_id = 2), 54.8667, -1.4)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Kye', 'Hutson', 'Mercedes-Benz', 'S-Class', (SELECT coalesce(avg(rating), 0)  FROM tblReviews WHERE driver_id = 3),
        (SELECT coalesce(count(rating), 0)   FROM tblReviews WHERE driver_id = 3), 54.8629, -1.4067)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Emilia', 'Fulton', 'Audi', 'A4', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.86554, -1.408262)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Kevin', 'Phillips' , 'Jaguar', 'F-Type', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.9223, -1.3716)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Jordan', 'Henderson' , 'Land Rover', 'Defender', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8744, -1.4286)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Nathan', 'Levitt' , 'Volvo', 'B12B', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8899, -1.3937)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Raich', 'Carter' , 'Aston Martin', 'DB3', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8957, -1.3668)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Danielle', 'Morgan' , 'Subaru', 'WRX STi', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8941, -1.3854)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Jack', 'Lacy' , 'Renault', 'Clio', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8883, -1.4123)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Jordan', 'Pickford' , 'GMC', 'Yukon', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8974, -1.5174)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Antony', 'Broadhead' , 'Dacia', 'Sandero', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8673, -1.4142)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Luke', "O'Nien" , 'Renault', 'Megane', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8948, -1.4484)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Jack', 'Clarke' , 'Audi', 'TT Coupe', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8880, -1.4429)
;
INSERT INTO tblDrivers (firstname, surname, car_manufacturer, car_model, average_rating, rides_completed, latitude, longitude)
VALUES ('Reece', 'Blakesley' , 'Nissan', 'Juke', (SELECT coalesce(avg(rating), 0)   FROM tblReviews WHERE driver_id = 4),
        (SELECT coalesce(count(rating), 0)  FROM tblReviews WHERE driver_id = 4),  54.8826, -1.4324)
;
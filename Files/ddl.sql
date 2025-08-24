CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Itineraries (
    itinerary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(255),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE DailySchedules (
    schedule_id INT AUTO_INCREMENT PRIMARY KEY,
    itinerary_id INT,
    day_number INT, 
    start_time TIME,
    end_time TIME,
    summary VARCHAR(500),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (itinerary_id) REFERENCES Itineraries(itinerary_id)
);

CREATE TABLE POI (
    poi_id INT AUTO_INCREMENT PRIMARY KEY,
    schedule_id INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100), 
    location VARCHAR(255),
    target_audience VARCHAR(255), 
    booking_link VARCHAR(500),
    avg_duration INT,
    opening_hours VARCHAR(255),
    ticket_price VARCHAR(100),
    review_summary TEXT,
    review_source VARCHAR(255),
    rating DECIMAL(2,1),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES DailySchedules(schedule_id)
);

CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    poi_id INT,
    itinerary_id INT,
    booking_link VARCHAR(500),
    status ENUM('Pending','Confirmed','Cancelled'),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (poi_id) REFERENCES POI(poi_id),
    FOREIGN KEY (itinerary_id) REFERENCES Itineraries(itinerary_id)
);

CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    itinerary_id INT,
    schedule_id INT,
    feedback_text TEXT,
    feedback_type ENUM('TooRushed','TooSlow','MoreFood','LessWalking','Other'),
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (itinerary_id) REFERENCES Itineraries(itinerary_id),
    FOREIGN KEY (schedule_id) REFERENCES DailySchedules(schedule_id)
);
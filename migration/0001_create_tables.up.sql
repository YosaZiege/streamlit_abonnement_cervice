CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    internet_limit VARCHAR(50) NOT NULL,
    call_minutes VARCHAR(50) NOT NULL,
    social_networks TEXT NOT NULL,
    international_minutes VARCHAR(50) NOT NULL,
    inwi_calls_unlimited BOOLEAN NOT NULL
);
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
);
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    subscription_id INT REFERENCES subscriptions(id),
    amount_paid DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    months_paid INT NOT NULL,  
    start_date TIMESTAMP NOT NULL,  
    abandoned BOOLEAN DEFAULT FALSE  
);
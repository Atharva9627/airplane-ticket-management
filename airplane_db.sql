CREATE TABLE ticket (
    ticket_no SERIAL PRIMARY KEY,    -- Automatically increments IDs (1, 2, 3...)
    booking_date DATE NOT NULL,      -- Stores the date
    class VARCHAR(20) NOT NULL,      -- Stores 'Economy' or 'Business'
    fare NUMERIC(10, 2) NOT NULL     -- Stores currency (e.g., 4500.50)
);
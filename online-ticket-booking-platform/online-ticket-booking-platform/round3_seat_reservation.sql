-- ROUND 3: High-Level Design - MySQL seat reservation demonstration

CREATE DATABASE IF NOT EXISTS ticketdb;
USE ticketdb;

DROP TABLE IF EXISTS seats;

CREATE TABLE seats (
    seat_id INT PRIMARY KEY,
    event_id INT NOT NULL,
    status ENUM('AVAILABLE', 'RESERVED', 'BOOKED') NOT NULL DEFAULT 'AVAILABLE'
);

INSERT INTO seats (seat_id, event_id, status) VALUES
(101, 1, 'AVAILABLE'),
(102, 1, 'AVAILABLE'),
(103, 1, 'BOOKED'),
(201, 2, 'AVAILABLE');

-- First reservation attempt: should change one row.
UPDATE seats
SET status = 'RESERVED'
WHERE seat_id = 101
  AND event_id = 1
  AND status = 'AVAILABLE';

SELECT * FROM seats WHERE seat_id = 101;

-- Second reservation attempt for the same seat: should change zero rows.
UPDATE seats
SET status = 'RESERVED'
WHERE seat_id = 101
  AND event_id = 1
  AND status = 'AVAILABLE';

SELECT * FROM seats WHERE seat_id = 101;

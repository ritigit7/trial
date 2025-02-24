use ppe;



CREATE TABLE IF NOT EXISTS detection_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    image_name VARCHAR(255) NOT NULL,
    person_id INT,
    body_part VARCHAR(50),
    ppe_type VARCHAR(50),
    confidence DECIMAL(5,2),
    violation BOOLEAN
);

-- Insert 20 rows of sample data
-- (You would replace this with actual data from your PPE detection system)
INSERT INTO detection_data (image_name, person_id, body_part, ppe_type, confidence, violation) VALUES
('image1.jpg', 1, 'head', 'helmet', 95.5, FALSE),
('image1.jpg', 1, 'hands', 'gloves', 90.0, FALSE),
('image2.jpg', 2, 'head', NULL, 0.0, TRUE), -- No helmet
('image3.jpg', 3, 'hands', 'gloves', 92.1, FALSE),
('image3.jpg', 3, 'face', 'mask', 98.7, FALSE),
('image4.jpg', 4, 'head', 'helmet', 88.2, FALSE),
('image4.jpg', 4, 'hands', NULL, 0.0, TRUE), -- No gloves
('image5.jpg', 5, 'head', 'helmet', 91.4, FALSE),
('image5.jpg', 5, 'face', NULL, 0.0, TRUE),   -- No mask
('image6.jpg', 1, 'head', 'helmet', 93.3, FALSE),
('image6.jpg', 1, 'hands', 'gloves', 85.6, FALSE),
('image7.jpg', 2, 'head', NULL, 0.0, TRUE),   -- No helmet
('image8.jpg', 3, 'hands', 'gloves', 89.9, FALSE),
('image8.jpg', 3, 'face', 'mask', 97.0, FALSE),
('image9.jpg', 4, 'head', 'helmet', 90.5, FALSE),
('image9.jpg', 4, 'hands', NULL, 0.0, TRUE),   -- No gloves
('image10.jpg', 5, 'head', 'helmet', 92.7, FALSE),
('image10.jpg', 5, 'face', 'mask', 99.1, FALSE),
('image11.jpg', 6, 'hands', 'gloves', 75.0, FALSE),
('image12.jpg', 7, 'head', 'helmet', 94.4, FALSE);
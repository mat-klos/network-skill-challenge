CREATE DATABASE network_assets;

\c network_assets

CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(15),
    mac_address VARCHAR(17),
    vendor_name VARCHAR(255)
);

INSERT INTO assets (ip_address, mac_address, vendor_name) VALUES 
('192.168.100.10', '00:1A:A1:4B:7C:2D', 'Cisco Systems');

INSERT INTO assets (ip_address, mac_address, vendor_name) VALUES 
('192.168.100.11', 'AC:87:A3:12:34:56', 'Apple');

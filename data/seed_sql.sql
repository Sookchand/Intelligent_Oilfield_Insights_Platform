-- PostgreSQL Seed Data for Intelligent Oilfield Insights Platform
-- Production Telemetry Database

-- Create production_data table
CREATE TABLE IF NOT EXISTS production_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    rig_name VARCHAR(100) NOT NULL,
    well_name VARCHAR(100),
    basin VARCHAR(100),
    production_rate DECIMAL(10, 2),
    pressure DECIMAL(10, 2),
    temperature DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create maintenance_schedule table
CREATE TABLE IF NOT EXISTS maintenance_schedule (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR(100) NOT NULL,
    equipment_type VARCHAR(100),
    last_maintenance_date DATE,
    next_maintenance_due DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create incidents table
CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    incident_id VARCHAR(100) UNIQUE NOT NULL,
    severity VARCHAR(50),
    description TEXT,
    location VARCHAR(200),
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample production data for Rig Alpha
INSERT INTO production_data (timestamp, rig_name, well_name, basin, production_rate, pressure, temperature) VALUES
('2024-12-30 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 850.5, 2500, 180),
('2024-12-30 09:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 870.0, 2520, 181),
('2024-12-30 08:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 890.5, 2540, 182),
('2024-12-29 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 900.0, 2550, 182),
('2024-12-29 09:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 920.5, 2560, 183),
('2024-12-28 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 950.0, 2580, 184),
('2024-12-27 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 980.5, 2600, 185),
('2024-12-26 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 1000.0, 2620, 186),
('2024-12-25 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 1020.5, 2640, 187),
('2024-12-24 10:00:00', 'Rig Alpha', 'Well W-12', 'Permian', 1050.0, 2660, 188);

-- Insert sample production data for other wells
INSERT INTO production_data (timestamp, rig_name, well_name, basin, production_rate, pressure, temperature) VALUES
('2024-12-30 10:00:00', 'Rig Beta', 'Well W-15', 'Permian', 450.0, 2300, 175),
('2024-12-30 10:00:00', 'Rig Gamma', 'Well W-20', 'Eagle Ford', 720.0, 2450, 178),
('2024-12-30 10:00:00', 'Rig Delta', 'Well W-25', 'Permian', 380.0, 2200, 172);

-- Insert maintenance schedule data
INSERT INTO maintenance_schedule (equipment_id, equipment_type, last_maintenance_date, next_maintenance_due, status) VALUES
('PUMP-45', 'Pump', '2024-10-15', '2024-12-15', 'OVERDUE'),
('GAUGE-G40', 'Pressure Gauge', '2024-11-01', '2025-01-01', 'SCHEDULED'),
('SENSOR-S12', 'Temperature Sensor', '2024-09-20', '2024-12-20', 'OVERDUE'),
('VALVE-V08', 'Control Valve', '2024-11-15', '2025-01-15', 'SCHEDULED');

-- Insert incident data
INSERT INTO incidents (incident_id, severity, description, location, timestamp) VALUES
('INC-2024-045', 'HIGH', 'Pressure anomaly detected at Well W-12', 'Rig Alpha, Well W-12', '2024-12-20 14:30:00'),
('INC-2024-046', 'MEDIUM', 'Minor leak detected at pump station', 'Rig Beta, Pump Station 2', '2024-12-22 09:15:00'),
('INC-2024-047', 'LOW', 'Routine inspection flagged sensor calibration', 'Rig Gamma, Well W-20', '2024-12-25 11:00:00');

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_production_rig_timestamp ON production_data(rig_name, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_production_well ON production_data(well_name);
CREATE INDEX IF NOT EXISTS idx_production_basin ON production_data(basin);
CREATE INDEX IF NOT EXISTS idx_maintenance_equipment ON maintenance_schedule(equipment_id);
CREATE INDEX IF NOT EXISTS idx_incidents_timestamp ON incidents(timestamp DESC);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO oilfield_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO oilfield_user;


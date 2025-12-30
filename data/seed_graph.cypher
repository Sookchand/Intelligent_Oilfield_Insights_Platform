// Neo4j Seed Data for Intelligent Oilfield Insights Platform
// Asset Hierarchy and Relationships

// Create Basins
CREATE (permian:Basin {name: 'Permian', location: 'West Texas', area_sqkm: 200000})
CREATE (eagleford:Basin {name: 'Eagle Ford', location: 'South Texas', area_sqkm: 100000})

// Create Rigs
CREATE (rigAlpha:Rig {name: 'Rig Alpha', type: 'Drilling', status: 'OPERATIONAL', capacity: 5000})
CREATE (rigBeta:Rig {name: 'Rig Beta', type: 'Drilling', status: 'OPERATIONAL', capacity: 4500})
CREATE (rigGamma:Rig {name: 'Rig Gamma', type: 'Workover', status: 'OPERATIONAL', capacity: 3000})
CREATE (rigDelta:Rig {name: 'Rig Delta', type: 'Drilling', status: 'MAINTENANCE', capacity: 5000})

// Create Wells
CREATE (wellW12:Well {name: 'Well W-12', depth_ft: 8500, status: 'PRODUCING', daily_target: 1000})
CREATE (wellW15:Well {name: 'Well W-15', depth_ft: 7200, status: 'PRODUCING', daily_target: 600})
CREATE (wellW20:Well {name: 'Well W-20', depth_ft: 9100, status: 'PRODUCING', daily_target: 800})
CREATE (wellW25:Well {name: 'Well W-25', depth_ft: 6800, status: 'UNDERPERFORMING', daily_target: 700})

// Create Sensors and Equipment
CREATE (gaugeG40:Sensor {sensor_id: 'G-40', sensor_type: 'Pressure Gauge', status: 'FAULTY', last_reading: 1850.5, last_reading_anomaly: true, anomaly_detected_at: datetime('2024-12-18T10:15:00')})
CREATE (sensorT15:Sensor {sensor_id: 'T-15', sensor_type: 'Temperature Sensor', status: 'OPERATIONAL', last_reading: 180.5, last_reading_anomaly: false})
CREATE (sensorF22:Sensor {sensor_id: 'F-22', sensor_type: 'Flow Meter', status: 'OPERATIONAL', last_reading: 850.0, last_reading_anomaly: false})
CREATE (sensorV08:Sensor {sensor_id: 'V-08', sensor_type: 'Vibration Sensor', status: 'WARNING', last_reading: 45.2, last_reading_anomaly: true, anomaly_detected_at: datetime('2024-12-25T08:30:00')})

CREATE (pump45:Equipment {id: 'PUMP-45', type: 'Pump', status: 'OPERATIONAL', last_maintenance: date('2024-10-15')})
CREATE (valve12:Equipment {id: 'VALVE-12', type: 'Control Valve', status: 'OPERATIONAL', last_maintenance: date('2024-11-20')})

// Create Incidents
CREATE (inc045:Incident {incident_id: 'INC-2024-045', severity: 'HIGH', description: 'Pressure anomaly detected', timestamp: datetime('2024-12-20T14:30:00')})
CREATE (inc046:Incident {incident_id: 'INC-2024-046', severity: 'MEDIUM', description: 'Minor leak detected', timestamp: datetime('2024-12-22T09:15:00')})

// Create Relationships - Basin to Rigs
CREATE (permian)-[:CONTAINS]->(rigAlpha)
CREATE (permian)-[:CONTAINS]->(rigBeta)
CREATE (permian)-[:CONTAINS]->(rigDelta)
CREATE (eagleford)-[:CONTAINS]->(rigGamma)

// Create Relationships - Rigs to Wells
CREATE (rigAlpha)-[:HAS_WELL]->(wellW12)
CREATE (rigBeta)-[:HAS_WELL]->(wellW15)
CREATE (rigGamma)-[:HAS_WELL]->(wellW20)
CREATE (rigDelta)-[:HAS_WELL]->(wellW25)

// Create Relationships - Wells to Sensors
CREATE (wellW12)-[:HAS_SENSOR]->(gaugeG40)
CREATE (wellW12)-[:HAS_SENSOR]->(sensorT15)
CREATE (wellW12)-[:HAS_SENSOR]->(sensorF22)
CREATE (wellW15)-[:HAS_SENSOR]->(sensorV08)

// Create Relationships - Wells to Equipment
CREATE (wellW12)-[:HAS_EQUIPMENT]->(pump45)
CREATE (wellW12)-[:HAS_EQUIPMENT]->(valve12)

// Create Relationships - Incidents to Locations
CREATE (inc045)-[:OCCURRED_AT]->(wellW12)
CREATE (inc046)-[:OCCURRED_AT]->(wellW15)

// Create Relationships - Incidents to Equipment
CREATE (inc045)-[:RELATED_TO]->(gaugeG40)
CREATE (inc046)-[:RELATED_TO]->(pump45)

// Create indexes for better query performance
CREATE INDEX rig_name_idx IF NOT EXISTS FOR (r:Rig) ON (r.name);
CREATE INDEX well_name_idx IF NOT EXISTS FOR (w:Well) ON (w.name);
CREATE INDEX sensor_id_idx IF NOT EXISTS FOR (s:Sensor) ON (s.sensor_id);
CREATE INDEX equipment_id_idx IF NOT EXISTS FOR (e:Equipment) ON (e.id);
CREATE INDEX incident_id_idx IF NOT EXISTS FOR (i:Incident) ON (i.incident_id);
CREATE INDEX basin_name_idx IF NOT EXISTS FOR (b:Basin) ON (b.name);

// Return summary
MATCH (n)
RETURN labels(n)[0] as NodeType, count(n) as Count
ORDER BY Count DESC;


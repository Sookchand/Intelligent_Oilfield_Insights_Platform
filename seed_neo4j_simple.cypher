// Simple Neo4j seed data for testing
// Create Basins
CREATE (permian:Basin {name: 'Permian Basin', location: 'West Texas'})
CREATE (eagleford:Basin {name: 'Eagle Ford', location: 'South Texas'})

// Create Rigs
CREATE (rigAlpha:Rig {name: 'Rig Alpha', status: 'active', basin: 'Permian Basin'})
CREATE (rigBeta:Rig {name: 'Rig Beta', status: 'active', basin: 'Eagle Ford'})

// Create Wells
CREATE (wellW12:Well {name: 'W-12', status: 'producing', depth_ft: 8500})
CREATE (wellW15:Well {name: 'W-15', status: 'producing', depth_ft: 9200})
CREATE (wellW18:Well {name: 'W-18', status: 'shut-in', depth_ft: 7800})

// Create Equipment
CREATE (gaugeG40:Sensor {sensor_id: 'G-40', sensor_type: 'pressure_gauge', status: 'faulty', last_reading: 2450.5})
CREATE (pump45:Sensor {sensor_id: 'PUMP-45', sensor_type: 'pump', status: 'operational', last_reading: 95.2})
CREATE (valve12:Sensor {sensor_id: 'VALVE-12', sensor_type: 'valve', status: 'operational', last_reading: 100.0})

// Create Incidents
CREATE (inc045:Incident {incident_id: 'INC-045', type: 'equipment_failure', severity: 'high', date: '2024-01-15'})
CREATE (inc046:Incident {incident_id: 'INC-046', type: 'pressure_drop', severity: 'medium', date: '2024-01-20'})

// Create Relationships - Basin to Rigs
CREATE (permian)-[:CONTAINS]->(rigAlpha)
CREATE (eagleford)-[:CONTAINS]->(rigBeta)

// Create Relationships - Rigs to Wells
CREATE (rigAlpha)-[:HAS_WELL]->(wellW12)
CREATE (rigAlpha)-[:HAS_WELL]->(wellW15)
CREATE (rigBeta)-[:HAS_WELL]->(wellW18)

// Create Relationships - Wells to Equipment
CREATE (wellW12)-[:HAS_SENSOR]->(gaugeG40)
CREATE (wellW12)-[:HAS_SENSOR]->(pump45)
CREATE (wellW15)-[:HAS_SENSOR]->(valve12)

// Create Relationships - Incidents
CREATE (inc045)-[:OCCURRED_AT]->(wellW12)
CREATE (inc045)-[:RELATED_TO]->(gaugeG40)
CREATE (inc046)-[:OCCURRED_AT]->(wellW15)
CREATE (inc046)-[:RELATED_TO]->(pump45)

RETURN 'Data seeded successfully' as result;


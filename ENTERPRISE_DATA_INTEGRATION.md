# 🏢 Enterprise Data Integration Architecture

## 🎯 **Overview**

This system is designed with **pluggable data source adapters** to integrate with any enterprise data platform. While the demo uses PostgreSQL + Neo4j, the architecture generalizes to:

- **Relational:** SQL Server, Oracle, PostgreSQL, MySQL, Snowflake
- **Data Lakes:** AWS S3, Azure Data Lake, Google Cloud Storage
- **Lakehouse:** Databricks Delta Lake, Apache Iceberg, Apache Hudi
- **Graph:** Neo4j, Amazon Neptune, Azure Cosmos DB (Gremlin)
- **Vector:** Qdrant, Pinecone, Weaviate, Milvus, pgvector
- **Time-Series:** InfluxDB, TimescaleDB, Prometheus

---

## 🏗️ **Adapter Pattern Architecture**

### **1. Abstract Data Source Interface**

```python
# backend/data_sources/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DataSourceAdapter(ABC):
    """
    Abstract base class for all data source adapters
    
    Ensures consistent interface across:
    - SQL databases (PostgreSQL, SQL Server, Oracle)
    - NoSQL databases (MongoDB, Cassandra)
    - Data lakes (S3, ADLS, GCS)
    - Graph databases (Neo4j, Neptune)
    - Vector stores (Qdrant, Pinecone)
    """
    
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> None:
        """Establish connection to data source"""
        pass
    
    @abstractmethod
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute query and return results"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Retrieve schema/metadata for query planning"""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check connection health"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close connection"""
        pass
```

---

### **2. SQL Database Adapters**

```python
# backend/data_sources/sql_adapters.py
from sqlalchemy import create_engine, text
from typing import List, Dict

class PostgreSQLAdapter(DataSourceAdapter):
    """PostgreSQL adapter (current demo)"""
    
    def __init__(self, config: Dict):
        self.engine = create_engine(
            f"postgresql://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['database']}"
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result]


class SQLServerAdapter(DataSourceAdapter):
    """
    Microsoft SQL Server adapter
    
    Use case: Legacy Oil & Gas ERP systems (SAP, Oracle E-Business Suite)
    """
    
    def __init__(self, config: Dict):
        # pyodbc for SQL Server
        self.engine = create_engine(
            f"mssql+pyodbc://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['database']}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        # Same interface, different backend
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result]


class OracleAdapter(DataSourceAdapter):
    """
    Oracle Database adapter
    
    Use case: Enterprise data warehouses (Oracle Exadata)
    Common in large Oil & Gas companies (Shell, BP, ExxonMobil)
    """
    
    def __init__(self, config: Dict):
        # cx_Oracle for Oracle
        self.engine = create_engine(
            f"oracle+cx_oracle://{config['user']}:{config['password']}@"
            f"{config['host']}:{config['port']}/{config['service_name']}"
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result]


class SnowflakeAdapter(DataSourceAdapter):
    """
    Snowflake adapter
    
    Use case: Cloud data warehouses for analytics
    """
    
    def __init__(self, config: Dict):
        self.engine = create_engine(
            f"snowflake://{config['user']}:{config['password']}@"
            f"{config['account']}/{config['database']}/{config['schema']}"
            f"?warehouse={config['warehouse']}&role={config['role']}"
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return [dict(row) for row in result]
```

---

### **3. Data Lake Adapters**

```python
# backend/data_sources/lake_adapters.py
import boto3
import pandas as pd
from typing import List, Dict

class S3DataLakeAdapter(DataSourceAdapter):
    """
    AWS S3 Data Lake adapter
    
    Use case: Petabyte-scale sensor data, seismic data, well logs
    
    Features:
    - Parquet/ORC file reading
    - Partition pruning
    - Predicate pushdown
    - Schema evolution
    """
    
    def __init__(self, config: Dict):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key'],
            region_name=config['region']
        )
        self.bucket = config['bucket']
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Query S3 using AWS Athena or direct Parquet reading
        
        Example query:
        SELECT * FROM s3://bucket/production_data/year=2024/month=01/*.parquet
        WHERE rig_name = 'Rig Alpha'
        """
        # Option 1: Use AWS Athena for SQL queries
        athena_client = boto3.client('athena')
        response = athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': params.get('database', 'default')},
            ResultConfiguration={'OutputLocation': f's3://{self.bucket}/athena-results/'}
        )
        
        # Wait for query completion and fetch results
        # ... (implementation details)
        
        # Option 2: Direct Parquet reading with PyArrow
        import pyarrow.parquet as pq
        table = pq.read_table(f's3://{self.bucket}/{params["path"]}')
        df = table.to_pandas()
        return df.to_dict('records')


class DeltaLakeAdapter(DataSourceAdapter):
    """
    Databricks Delta Lake adapter
    
    Use case: ACID transactions on data lakes, time travel, schema enforcement
    
    Features:
    - ACID guarantees
    - Time travel (query historical data)
    - Schema evolution
    - Upserts/Deletes
    """
    
    def __init__(self, config: Dict):
        from delta import DeltaTable
        self.spark = self._create_spark_session(config)
        self.catalog = config.get('catalog', 'main')
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        """
        Query Delta Lake using Spark SQL
        
        Example:
        SELECT * FROM delta.`s3://bucket/production_delta`
        WHERE date >= '2024-01-01'
        VERSION AS OF 10  -- Time travel!
        """
        df = self.spark.sql(query)
        return df.toPandas().to_dict('records')
    
    def time_travel_query(self, table: str, version: int) -> List[Dict]:
        """Query historical version of data"""
        df = self.spark.read.format("delta").option("versionAsOf", version).load(table)
        return df.toPandas().to_dict('records')
```

---

### **4. Graph Database Adapters**

```python
# backend/data_sources/graph_adapters.py

class Neo4jAdapter(DataSourceAdapter):
    """Neo4j adapter (current demo)"""
    # ... (existing implementation)


class NeptuneAdapter(DataSourceAdapter):
    """
    AWS Neptune adapter
    
    Use case: Managed graph database in AWS
    Supports both Gremlin and SPARQL
    """
    
    def __init__(self, config: Dict):
        from gremlin_python.driver import client
        self.client = client.Client(
            f"wss://{config['endpoint']}:8182/gremlin",
            'g'
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute Gremlin query"""
        result = self.client.submit(query, params or {})
        return [r for r in result]


class CosmosDBAdapter(DataSourceAdapter):
    """
    Azure Cosmos DB (Gremlin API) adapter
    
    Use case: Multi-model database in Azure
    """
    
    def __init__(self, config: Dict):
        from gremlin_python.driver import client
        self.client = client.Client(
            f"wss://{config['account']}.gremlin.cosmos.azure.com:443/",
            'g',
            username=f"/dbs/{config['database']}/colls/{config['collection']}",
            password=config['key']
        )
    
    def query(self, query: str, params: Dict = None) -> List[Dict]:
        result = self.client.submit(query, params or {})
        return [r for r in result]
```

---

## 🔌 **Adapter Registry & Dynamic Loading**

```python
# backend/data_sources/registry.py
from typing import Dict, Type

class DataSourceRegistry:
    """
    Central registry for all data source adapters
    
    Enables dynamic adapter selection based on configuration
    """
    
    _adapters: Dict[str, Type[DataSourceAdapter]] = {
        # SQL Databases
        "postgresql": PostgreSQLAdapter,
        "sqlserver": SQLServerAdapter,
        "oracle": OracleAdapter,
        "mysql": MySQLAdapter,
        "snowflake": SnowflakeAdapter,
        
        # Data Lakes
        "s3": S3DataLakeAdapter,
        "adls": AzureDataLakeAdapter,
        "gcs": GCSDataLakeAdapter,
        "delta": DeltaLakeAdapter,
        
        # Graph Databases
        "neo4j": Neo4jAdapter,
        "neptune": NeptuneAdapter,
        "cosmosdb": CosmosDBAdapter,
        
        # Vector Stores
        "qdrant": QdrantAdapter,
        "pinecone": PineconeAdapter,
        "weaviate": WeaviateAdapter,
    }
    
    @classmethod
    def get_adapter(cls, source_type: str, config: Dict) -> DataSourceAdapter:
        """
        Factory method to create adapter instance
        
        Usage:
        adapter = DataSourceRegistry.get_adapter("oracle", {
            "host": "oracle.company.com",
            "port": 1521,
            "service_name": "PROD"
        })
        """
        if source_type not in cls._adapters:
            raise ValueError(f"Unknown data source type: {source_type}")
        
        adapter_class = cls._adapters[source_type]
        return adapter_class(config)
```

---

## 📋 **Configuration-Driven Integration**

```yaml
# config/data_sources.yaml
data_sources:
  # Production database (SQL Server)
  production_db:
    type: sqlserver
    host: sqlserver.oilco.com
    port: 1433
    database: ProductionData
    user: ${SQL_USER}
    password: ${SQL_PASSWORD}
    
  # Data warehouse (Snowflake)
  analytics_warehouse:
    type: snowflake
    account: oilco.us-east-1
    database: ANALYTICS
    schema: PUBLIC
    warehouse: COMPUTE_WH
    user: ${SNOWFLAKE_USER}
    password: ${SNOWFLAKE_PASSWORD}
    
  # Data lake (S3 + Delta Lake)
  sensor_data_lake:
    type: delta
    path: s3://oilco-datalake/sensor-data/
    catalog: unity_catalog
    
  # Knowledge graph (Neo4j)
  asset_graph:
    type: neo4j
    uri: bolt://neo4j.oilco.com:7687
    user: ${NEO4J_USER}
    password: ${NEO4J_PASSWORD}
```

---

## ✅ **Key Benefits**

1. **Pluggable Architecture** - Add new data sources without changing core logic
2. **Consistent Interface** - Same query API across all sources
3. **Enterprise Ready** - Supports SQL Server, Oracle, Snowflake, Delta Lake
4. **Cloud Native** - AWS, Azure, GCP integrations
5. **Configuration Driven** - No code changes for new sources

**This architecture demonstrates production-grade data integration capabilities required for enterprise Oil & Gas deployments.**


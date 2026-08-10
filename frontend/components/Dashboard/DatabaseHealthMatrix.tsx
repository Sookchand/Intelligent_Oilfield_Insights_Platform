'use client';

import { useEffect, useState } from 'react';
import { Database, Network, FileText, HardDrive } from 'lucide-react';

interface DatabaseStatus {
  postgres: boolean;
  neo4j: boolean;
  qdrant: boolean;
  minio: boolean;
}

export default function DatabaseHealthMatrix() {
  const [status, setStatus] = useState<DatabaseStatus>({
    postgres: false,
    neo4j: false,
    qdrant: false,
    minio: false,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDatabaseStatus();
    const interval = setInterval(fetchDatabaseStatus, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const fetchDatabaseStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/status/databases');
      const data = await response.json();
      setStatus(data.databases);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch database status:', error);
      setLoading(false);
    }
  };

  const databases = [
    {
      name: 'PostgreSQL',
      key: 'postgres' as keyof DatabaseStatus,
      icon: Database,
      description: 'Production Data',
    },
    {
      name: 'Neo4j',
      key: 'neo4j' as keyof DatabaseStatus,
      icon: Network,
      description: 'Asset Graph',
    },
    {
      name: 'Qdrant',
      key: 'qdrant' as keyof DatabaseStatus,
      icon: HardDrive,
      description: 'Vector Search',
    },
    {
      name: 'MinIO',
      key: 'minio' as keyof DatabaseStatus,
      icon: FileText,
      description: 'Documents',
    },
  ];

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
            System Health Matrix
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
            Real-time database connectivity
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-green-600 dark:text-green-400">
            Live
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {databases.map((db) => {
          const Icon = db.icon;
          const isHealthy = status[db.key];
          
          return (
            <div
              key={db.key}
              className={`
                relative p-4 rounded-lg border-2 transition-all
                ${isHealthy 
                  ? 'border-green-500 bg-green-50 dark:bg-green-900/20' 
                  : 'border-red-500 bg-red-50 dark:bg-red-900/20'
                }
              `}
            >
              {/* Pulsing LED Indicator */}
              <div className="absolute top-2 right-2">
                <div
                  className={`
                    w-3 h-3 rounded-full led-indicator
                    ${isHealthy ? 'led-success' : 'led-danger'}
                  `}
                  style={{
                    background: isHealthy ? '#10B981' : '#EF4444',
                    boxShadow: `0 0 10px ${isHealthy ? '#10B981' : '#EF4444'}`,
                  }}
                ></div>
              </div>

              {/* Icon */}
              <div className={`
                w-10 h-10 rounded-lg flex items-center justify-center mb-3
                ${isHealthy 
                  ? 'bg-green-100 dark:bg-green-800' 
                  : 'bg-red-100 dark:bg-red-800'
                }
              `}>
                <Icon className={`
                  w-5 h-5
                  ${isHealthy 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'
                  }
                `} />
              </div>

              {/* Name */}
              <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-1">
                {db.name}
              </h4>
              
              {/* Description */}
              <p className="text-xs text-slate-600 dark:text-slate-400 mb-2">
                {db.description}
              </p>

              {/* Status */}
              <div className={`
                inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
                ${isHealthy 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' 
                  : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                }
              `}>
                {loading ? 'Checking...' : isHealthy ? 'Online' : 'Offline'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}


'use client';

import { useQuery } from '@tanstack/react-query';
import { queryAPI } from '@/lib/api';
import { Database, CheckCircle, XCircle, Loader } from 'lucide-react';

const databases = [
  { key: 'postgres', name: 'PostgreSQL', description: 'Time-series production data' },
  { key: 'neo4j', name: 'Neo4j', description: 'Asset relationship graph' },
  { key: 'qdrant', name: 'Qdrant', description: 'Vector search engine' },
  { key: 'minio', name: 'MinIO', description: 'Object storage' },
];

export default function DatabaseStatus() {
  const { data, isLoading } = useQuery({
    queryKey: ['database-status'],
    queryFn: () => queryAPI.getDatabaseStatus(),
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Database className="w-5 h-5 text-slate-600 dark:text-slate-400" />
          <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
            Database Connectivity
          </h2>
        </div>
        
        {data?.all_healthy && (
          <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs font-medium rounded-full">
            All Systems Operational
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {databases.map((db) => {
          const isConnected = data?.databases?.[db.key];
          
          return (
            <div
              key={db.key}
              className={`
                p-4 rounded-lg border-2 transition-all
                ${isConnected 
                  ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20' 
                  : 'border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20'
                }
              `}
            >
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold text-slate-900 dark:text-white text-sm">
                  {db.name}
                </h3>
                {isLoading ? (
                  <Loader className="w-4 h-4 text-slate-400 animate-spin" />
                ) : isConnected ? (
                  <CheckCircle className="w-4 h-4 text-green-600 dark:text-green-400" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                )}
              </div>
              
              <p className="text-xs text-slate-600 dark:text-slate-400">
                {db.description}
              </p>
              
              <div className="mt-2">
                <span className={`
                  text-xs font-medium
                  ${isConnected 
                    ? 'text-green-700 dark:text-green-400' 
                    : 'text-red-700 dark:text-red-400'
                  }
                `}>
                  {isLoading ? 'Checking...' : isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}


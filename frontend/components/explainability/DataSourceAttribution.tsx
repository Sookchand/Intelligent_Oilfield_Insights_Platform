'use client';

import { DataSource } from '@/lib/api';
import { Database, Network, FileText, HardDrive } from 'lucide-react';

interface DataSourceAttributionProps {
  dataSources: DataSource[];
  confidence: number;
}

const databaseIcons: Record<string, any> = {
  'PostgreSQL': Database,
  'Neo4j': Network,
  'Qdrant': FileText,
  'MinIO': HardDrive,
};

const databaseColors: Record<string, string> = {
  'PostgreSQL': 'from-blue-500 to-blue-600',
  'Neo4j': 'from-purple-500 to-purple-600',
  'Qdrant': 'from-green-500 to-green-600',
  'MinIO': 'from-orange-500 to-orange-600',
};

export default function DataSourceAttribution({ dataSources, confidence }: DataSourceAttributionProps) {
  const totalWeight = dataSources.reduce((sum, source) => sum + source.weight, 0);

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">
        Data Source Attribution
      </h2>

      {/* Source List */}
      <div className="space-y-4 mb-6">
        {dataSources.map((source, idx) => {
          const Icon = databaseIcons[source.database] || Database;
          const colorClass = databaseColors[source.database] || 'from-gray-500 to-gray-600';
          const percentage = totalWeight > 0 ? (source.weight / totalWeight) * 100 : 0;

          return (
            <div key={idx} className="border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <div className="flex items-start space-x-3 mb-3">
                <div className={`w-10 h-10 bg-gradient-to-br ${colorClass} rounded-lg flex items-center justify-center flex-shrink-0`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="font-semibold text-slate-900 dark:text-white">
                      {source.database}
                    </h3>
                    <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
                      {percentage.toFixed(0)}%
                    </span>
                  </div>
                  
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                    {source.type}
                  </p>

                  {/* Weight Bar */}
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden mb-2">
                    <div
                      className={`h-full bg-gradient-to-r ${colorClass} transition-all duration-500`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>

                  {/* Contribution */}
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {source.contribution}
                  </p>
                </div>
              </div>

              {/* Metadata */}
              <div className="flex items-center space-x-4 text-xs text-slate-500 dark:text-slate-400 pt-3 border-t border-slate-200 dark:border-slate-700">
                {source.records !== undefined && (
                  <div>
                    <span className="font-medium">Records:</span> {source.records}
                  </div>
                )}
                {source.paths !== undefined && (
                  <div>
                    <span className="font-medium">Paths:</span> {source.paths}
                  </div>
                )}
                <div>
                  <span className="font-medium">Weight:</span> {source.weight.toFixed(2)}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">
            Total Sources
          </p>
          <p className="text-2xl font-bold text-slate-900 dark:text-white">
            {dataSources.length}
          </p>
        </div>

        <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">
            Total Records
          </p>
          <p className="text-2xl font-bold text-slate-900 dark:text-white">
            {dataSources.reduce((sum, s) => sum + (s.records || s.paths || 0), 0)}
          </p>
        </div>
      </div>

      {/* Data Quality Indicator */}
      <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-1">
              Data Quality Score
            </p>
            <p className="text-xs text-blue-700 dark:text-blue-400">
              Based on source diversity and coverage
            </p>
          </div>
          <div className="text-right">
            <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
              {Math.round(confidence * 100)}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


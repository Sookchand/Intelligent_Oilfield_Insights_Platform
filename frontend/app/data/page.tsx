'use client';

import { Database } from 'lucide-react';

export default function DataPage() {
  return (
    <div className="max-w-7xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12 text-center">
        <Database className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white mb-2">
          Data Explorer
        </h1>
        <p className="text-slate-600 dark:text-slate-400">
          Coming soon - Browse and explore data across PostgreSQL, Neo4j, Qdrant, and MinIO
        </p>
      </div>
    </div>
  );
}


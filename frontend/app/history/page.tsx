'use client';

import { useState, useEffect } from 'react';
import { Clock, CheckCircle, XCircle, Archive, Download, Search, Filter, AlertCircle, Database } from 'lucide-react';
import { auditAPI, QueryAudit } from '@/lib/api';
import { getMockAuditHistory } from '@/lib/mockAuditData';

export default function QueryHistoryPage() {
  const [queries, setQueries] = useState<QueryAudit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [usingMockData, setUsingMockData] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  useEffect(() => {
    fetchQueryHistory();
  }, []);

  const fetchQueryHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      setUsingMockData(false);
      const data = await auditAPI.getQueryHistory(50, 0);
      setQueries(data.queries || []);
    } catch (error) {
      console.error('Failed to fetch query history:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch query history');
      // Don't auto-load mock data - let user decide
    } finally {
      setLoading(false);
    }
  };

  const loadMockData = () => {
    const mockData = getMockAuditHistory(50, 0);
    setQueries(mockData.queries as QueryAudit[]);
    setUsingMockData(true);
    setError(null);
  };

  const archiveQuery = async (queryId: number) => {
    try {
      await auditAPI.archiveQuery(queryId);
      fetchQueryHistory(); // Refresh
    } catch (error) {
      console.error('Failed to archive query:', error);
      setError('Failed to archive query');
    }
  };

  const filteredQueries = queries.filter(q => {
    const matchesSearch = q.query_text.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || q.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-yellow-500" />;
    }
  };

  const getConfidenceBadge = (confidence: number) => {
    const percentage = Math.round(confidence * 100);
    let colorClass = 'bg-gray-100 text-gray-800';

    if (percentage >= 80) colorClass = 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
    else if (percentage >= 60) colorClass = 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
    else colorClass = 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colorClass}`}>
        {percentage}%
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
              Query Audit Trail
            </h1>
            <p className="text-slate-600 dark:text-slate-400 mt-2">
              Complete history of all AI queries for compliance and governance
            </p>
          </div>
          <button className="px-4 py-2 bg-halliburton-red hover:bg-halliburton-red-dark text-white rounded-lg font-medium transition-colors flex items-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>

        {/* Filters */}
        <div className="mt-6 flex space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Search queries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-halliburton-red focus:border-transparent bg-white dark:bg-slate-700 text-slate-900 dark:text-white"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-halliburton-red bg-white dark:bg-slate-700 text-slate-900 dark:text-white"
          >
            <option value="all">All Status</option>
            <option value="success">Success</option>
            <option value="failed">Failed</option>
            <option value="partial">Partial</option>
          </select>
        </div>
      </div>

      {/* Mock Data Banner */}
      {usingMockData && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Database className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              <div>
                <h3 className="text-blue-800 dark:text-blue-400 font-semibold">
                  Using Demo Data
                </h3>
                <p className="text-blue-600 dark:text-blue-300 mt-1">
                  Showing mock queries for demonstration purposes
                </p>
              </div>
            </div>
            <button
              onClick={fetchQueryHistory}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              Try Real Data
            </button>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && !usingMockData && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400" />
              <div>
                <h3 className="text-red-800 dark:text-red-400 font-semibold">
                  Error Loading Query History
                </h3>
                <p className="text-red-600 dark:text-red-300 mt-1">
                  {error}
                </p>
                <p className="text-sm text-red-500 dark:text-red-400 mt-2">
                  Make sure the backend is running on http://localhost:8000
                </p>
              </div>
            </div>
            <button
              onClick={loadMockData}
              className="px-4 py-2 bg-halliburton-red hover:bg-halliburton-red-dark text-white rounded-lg text-sm font-medium transition-colors whitespace-nowrap"
            >
              Load Demo Data
            </button>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700">
              <tr>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Query
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Time (ms)
                </th>
                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Sources
                </th>
                <th className="px-6 py-4 text-right text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
              {loading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-slate-500">
                    Loading query history...
                  </td>
                </tr>
              ) : filteredQueries.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center space-y-3">
                      <Clock className="w-12 h-12 text-slate-300 dark:text-slate-600" />
                      <div>
                        <p className="text-slate-600 dark:text-slate-400 font-medium">
                          {queries.length === 0 ? 'No queries logged yet' : 'No queries match your filters'}
                        </p>
                        <p className="text-sm text-slate-500 dark:text-slate-500 mt-1">
                          {queries.length === 0
                            ? 'Submit a query on the main page to see it logged here'
                            : 'Try adjusting your search or filter criteria'}
                        </p>
                      </div>
                    </div>
                  </td>
                </tr>
              ) : (
                filteredQueries.map((query) => (
                  <tr key={query.id} className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="max-w-md">
                        <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                          {query.query_text}
                        </p>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 truncate">
                          {query.result_summary}
                        </p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400 whitespace-nowrap">
                      {new Date(query.timestamp).toLocaleString()}
                    </td>
                    <td className="px-6 py-4">
                      {getConfidenceBadge(query.confidence_score)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(query.status)}
                        <span className="text-sm text-slate-600 dark:text-slate-400 capitalize">
                          {query.status}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400">
                      {query.processing_time_ms}ms
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {query.data_sources_used?.map((source, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded text-xs font-medium"
                          >
                            {source}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => archiveQuery(query.id)}
                        className="text-slate-400 hover:text-halliburton-red transition-colors"
                        title="Archive query"
                      >
                        <Archive className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}


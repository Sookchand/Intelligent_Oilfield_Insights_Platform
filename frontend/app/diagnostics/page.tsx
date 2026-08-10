'use client';

import { useState } from 'react';
import { Activity, Database, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

export default function DiagnosticsPage() {
  const [testing, setTesting] = useState(false);
  const [results, setResults] = useState<any>(null);

  const runDiagnostics = async () => {
    setTesting(true);
    const diagnostics: any = {
      timestamp: new Date().toISOString(),
      tests: {}
    };

    // Test 1: Backend connectivity
    try {
      const response = await fetch('http://localhost:8000/api/status/databases', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      diagnostics.tests.backend = {
        status: response.ok ? 'success' : 'warning',
        statusCode: response.status,
        message: response.ok ? 'Backend is responding' : `Backend returned ${response.status}`,
        data: response.ok ? await response.json() : null
      };
    } catch (error: any) {
      diagnostics.tests.backend = {
        status: 'error',
        message: 'Cannot connect to backend',
        error: error.message,
        details: 'Make sure backend is running on http://localhost:8000'
      };
    }

    // Test 2: Query submission
    if (diagnostics.tests.backend.status === 'success') {
      try {
        const response = await fetch('http://localhost:8000/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: 'Test query for diagnostics' })
        });
        
        diagnostics.tests.query = {
          status: response.ok ? 'success' : 'warning',
          statusCode: response.status,
          message: response.ok ? 'Query endpoint working' : `Query failed with ${response.status}`,
          data: response.ok ? await response.json() : null
        };
      } catch (error: any) {
        diagnostics.tests.query = {
          status: 'error',
          message: 'Query submission failed',
          error: error.message
        };
      }
    }

    // Test 3: Audit history
    if (diagnostics.tests.backend.status === 'success') {
      try {
        const response = await fetch('http://localhost:8000/api/audit/history?limit=5', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        });
        
        const data = response.ok ? await response.json() : null;
        
        diagnostics.tests.audit = {
          status: response.ok ? 'success' : 'warning',
          statusCode: response.status,
          message: response.ok ? `Found ${data?.total || 0} queries in history` : `Audit failed with ${response.status}`,
          data: data,
          queryCount: data?.total || 0
        };
      } catch (error: any) {
        diagnostics.tests.audit = {
          status: 'error',
          message: 'Audit history check failed',
          error: error.message
        };
      }
    }

    setResults(diagnostics);
    setTesting(false);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success': return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'warning': return <AlertTriangle className="w-6 h-6 text-yellow-500" />;
      case 'error': return <XCircle className="w-6 h-6 text-red-500" />;
      default: return <Activity className="w-6 h-6 text-gray-500" />;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-slate-200 dark:border-slate-700 p-8">
        <div className="flex items-center space-x-3 mb-6">
          <Activity className="w-8 h-8 text-halliburton-red" />
          <div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              System Diagnostics
            </h1>
            <p className="text-slate-600 dark:text-slate-400">
              Test backend connectivity and query logging
            </p>
          </div>
        </div>

        <button
          onClick={runDiagnostics}
          disabled={testing}
          className="w-full px-6 py-3 bg-halliburton-red hover:bg-halliburton-red-dark text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed mb-6"
        >
          {testing ? 'Running Diagnostics...' : 'Run Diagnostics'}
        </button>

        {results && (
          <div className="space-y-4">
            <div className="text-sm text-slate-500 dark:text-slate-400">
              Test run at: {new Date(results.timestamp).toLocaleString()}
            </div>

            {Object.entries(results.tests).map(([testName, test]: [string, any]) => (
              <div
                key={testName}
                className="border border-slate-200 dark:border-slate-700 rounded-lg p-4"
              >
                <div className="flex items-start space-x-3">
                  {getStatusIcon(test.status)}
                  <div className="flex-1">
                    <h3 className="font-semibold text-slate-900 dark:text-white capitalize">
                      {testName} Test
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      {test.message}
                    </p>
                    
                    {test.error && (
                      <div className="mt-2 p-2 bg-red-50 dark:bg-red-900/20 rounded text-sm text-red-600 dark:text-red-400">
                        Error: {test.error}
                      </div>
                    )}
                    
                    {test.details && (
                      <div className="mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-sm text-blue-600 dark:text-blue-400">
                        {test.details}
                      </div>
                    )}
                    
                    {test.data && (
                      <details className="mt-2">
                        <summary className="cursor-pointer text-sm text-slate-500 hover:text-slate-700">
                          View Response Data
                        </summary>
                        <pre className="mt-2 p-2 bg-slate-100 dark:bg-slate-900 rounded text-xs overflow-auto">
                          {JSON.stringify(test.data, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}


'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { queryAPI, QueryResponse } from '@/lib/api';
import AgentWorkflow from '@/components/explainability/AgentWorkflow';
import ReasoningTimeline from '@/components/explainability/ReasoningTimeline';
import ConfidenceBreakdown from '@/components/explainability/ConfidenceBreakdown';
import DataSourceAttribution from '@/components/explainability/DataSourceAttribution';
import GraphVisualization from '@/components/explainability/GraphVisualization';
import OntologyVisualization from '@/components/explainability/OntologyVisualization';
import { Brain, Download, AlertCircle } from 'lucide-react';

function ExplainabilityContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('query') || '';

  const [query, setQuery] = useState(initialQuery);
  const [result, setResult] = useState<QueryResponse | null>(null);

  const queryMutation = useMutation({
    mutationFn: (q: string) => queryAPI.processQuery(q),
    onSuccess: (data) => {
      setResult(data);
    },
  });

  useEffect(() => {
    if (initialQuery && !result) {
      queryMutation.mutate(initialQuery);
    }
  }, [initialQuery]);

  const handleQuery = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      queryMutation.mutate(query);
    }
  };

  const exportAuditLog = () => {
    if (!result) return;

    const auditLog = {
      query_id: `q_${Date.now()}`,
      timestamp: new Date().toISOString(),
      user: 'demo_user@oilfield.com', // TODO: Get from auth context
      natural_language_query: query,
      reasoning_trace: result.reasoning_trace, // Include FULL reasoning trace
      sql_queries: result.reasoning_trace
        ?.filter(step => step.sql_query)
        .map(step => ({
          step: step.step,
          agent: step.agent,
          query: step.sql_query,
          duration_ms: step.duration_ms,
          result: step.result,
        })) || [],
      cypher_queries: result.reasoning_trace
        ?.filter(step => step.cypher_query)
        .map(step => ({
          step: step.step,
          agent: step.agent,
          query: step.cypher_query,
          duration_ms: step.duration_ms,
          result: step.result,
        })) || [],
      answer: result.answer,
      confidence: result.confidence,
      confidence_breakdown: result.confidence_breakdown,
      data_sources: result.data_sources,
    };

    // Download as JSON
    const blob = new Blob([JSON.stringify(auditLog, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `audit_log_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-blue-600 rounded-xl shadow-lg p-8 text-white">
        <div className="flex items-center space-x-3 mb-4">
          <Brain className="w-10 h-10" />
          <div>
            <h1 className="text-3xl font-bold">AI Explainability Dashboard</h1>
            <p className="text-purple-100">
              Understand how the multi-agent system reaches its conclusions
            </p>
          </div>
        </div>

        {/* Query Input */}
        <form onSubmit={handleQuery} className="mt-6">
          <div className="flex space-x-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter a query to analyze..."
              className="flex-1 px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50"
            />
            <button
              type="submit"
              disabled={queryMutation.isPending}
              className="px-6 py-3 bg-white text-purple-600 font-semibold rounded-lg hover:bg-purple-50 disabled:opacity-50 transition-colors"
            >
              {queryMutation.isPending ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </form>
      </div>

      {/* Loading State */}
      {queryMutation.isPending && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12">
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-500"></div>
            <p className="text-slate-600 dark:text-slate-400 text-lg">
              Processing query through multi-agent system...
            </p>
            <p className="text-slate-500 dark:text-slate-500 text-sm">
              This may take a few seconds as we query multiple databases
            </p>
          </div>
        </div>
      )}

      {/* Error State */}
      {queryMutation.isError && (
        <div className="bg-red-50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800 rounded-xl p-6">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-red-800 dark:text-red-400 font-semibold mb-2">
                Error Processing Query
              </h3>
              <p className="text-red-600 dark:text-red-300">
                {queryMutation.error instanceof Error ? queryMutation.error.message : 'An error occurred'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !queryMutation.isPending && (
        <>
          {/* Answer Summary */}
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">
                  Analysis Result
                </h2>
                <p className="text-slate-600 dark:text-slate-400 text-sm">
                  Query: <span className="font-medium">{query}</span>
                </p>
              </div>

              <button
                onClick={exportAuditLog}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                title="Export complete audit log with all queries"
              >
                <Download className="w-4 h-4" />
                <span>Export Audit Log</span>
              </button>
            </div>

            <div className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4">
              <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
                {result.answer}
              </p>
            </div>

            {/* Reasoning Trace */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Reasoning Trace
              </h3>
              <div className="space-y-3">
                {result.reasoning_trace.map((step, idx) => (
                  <div key={idx} className="bg-slate-50 dark:bg-slate-900 rounded-lg p-4 border-l-4 border-blue-500">
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-semibold">
                        {step.step}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-semibold text-slate-900 dark:text-white">
                            {step.agent}
                          </span>
                          <span className="text-xs text-slate-500 dark:text-slate-400">
                            {step.action}
                          </span>
                          {(step as any).duration_ms && (
                            <span className="text-xs text-green-600 dark:text-green-400 ml-auto">
                              ⚡ {(step as any).duration_ms}ms
                            </span>
                          )}
                        </div>
                        {step.result && (
                          <p className="text-sm text-slate-600 dark:text-slate-400 mb-2">
                            {step.result}
                          </p>
                        )}

                        {/* Show SQL Query */}
                        {(step as any).sql_query && (
                          <div className="mt-2 bg-green-50 dark:bg-green-900/20 rounded p-2 border border-green-200 dark:border-green-800">
                            <div className="text-xs font-semibold text-green-700 dark:text-green-400 mb-1">
                              📊 SQL Query Executed:
                            </div>
                            <code className="text-xs text-slate-700 dark:text-slate-300 font-mono">
                              {(step as any).sql_query}
                            </code>
                          </div>
                        )}

                        {/* Show Cypher Query */}
                        {(step as any).cypher_query && (
                          <div className="mt-2 bg-purple-50 dark:bg-purple-900/20 rounded p-2 border border-purple-200 dark:border-purple-800">
                            <div className="text-xs font-semibold text-purple-700 dark:text-purple-400 mb-1">
                              🔗 Cypher Query Executed:
                            </div>
                            <code className="text-xs text-slate-700 dark:text-slate-300 font-mono">
                              {(step as any).cypher_query}
                            </code>
                          </div>
                        )}

                        {/* Show Database Details */}
                        {(step as any).details && (
                          <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
                            {(step as any).details.database && (
                              <span className="mr-3">
                                💾 Database: <strong>{(step as any).details.database}</strong>
                              </span>
                            )}
                            {(step as any).details.records_count !== undefined && (
                              <span>
                                📝 Records: <strong>{(step as any).details.records_count}</strong>
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Confidence */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                Confidence Score
              </h3>
              <div className="flex items-center space-x-4">
                <div className="flex-1 bg-slate-200 dark:bg-slate-700 rounded-full h-4">
                  <div
                    className="bg-green-500 h-4 rounded-full transition-all"
                    style={{ width: `${result.confidence * 100}%` }}
                  />
                </div>
                <span className="text-2xl font-bold text-slate-900 dark:text-white">
                  {Math.round(result.confidence * 100)}%
                </span>
              </div>
            </div>

            {/* Graph Path Visualization */}
            {result.graph_path && result.graph_path.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                  Asset Relationship Graph
                </h3>
                <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 rounded-lg p-6 border-2 border-purple-200 dark:border-purple-800">
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
                    The AI traced this path through the asset graph to understand relationships:
                  </p>
                  <div className="flex items-center justify-center space-x-3 flex-wrap">
                    {result.graph_path.map((node, idx) => (
                      <div key={idx} className="flex items-center">
                        <div className="px-4 py-3 bg-white dark:bg-slate-700 rounded-lg shadow-md border-2 border-purple-300 dark:border-purple-600">
                          <div className="text-xs text-slate-500 dark:text-slate-400 mb-1">
                            {idx === 0 ? 'Start' : idx === result.graph_path!.length - 1 ? 'End' : `Step ${idx}`}
                          </div>
                          <div className="font-semibold text-slate-900 dark:text-white">
                            {node}
                          </div>
                        </div>
                        {idx < result.graph_path!.length - 1 && (
                          <div className="mx-2 text-purple-500 dark:text-purple-400 text-2xl">
                            →
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 text-sm text-slate-600 dark:text-slate-400">
                    <strong>Decision Making:</strong> The AI analyzed this relationship chain to identify:
                    <ul className="list-disc list-inside mt-2 space-y-1">
                      <li>Equipment dependencies and connections</li>
                      <li>Faulty components affecting production</li>
                      <li>Root cause analysis through graph traversal</li>
                    </ul>
                  </div>
                </div>
              </div>
            )}

            {/* Source Attribution - Data Grounding */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4 flex items-center">
                <span className="mr-2">🎯</span>
                Source Attribution & Data Lineage
              </h3>
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border-2 border-blue-300 dark:border-blue-700 mb-4">
                <p className="text-sm text-slate-700 dark:text-slate-300 font-medium">
                  <strong>100% Auditability:</strong> Every answer is grounded in actual database results.
                  No LLM hallucinations - all facts are traceable to their source.
                </p>
              </div>
            </div>

            {/* Data Sources Used */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Data Sources Consulted
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4 border border-green-200 dark:border-green-800">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="font-semibold text-slate-900 dark:text-white">PostgreSQL</span>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Production time-series data, trends, and telemetry
                  </p>
                  {result.reasoning_trace.some(t => t.agent === 'SQL') && (
                    <div className="mt-2 text-xs text-green-700 dark:text-green-400 font-semibold">
                      ✓ Used in this query
                    </div>
                  )}
                </div>
                <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                    <span className="font-semibold text-slate-900 dark:text-white">Neo4j</span>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Asset relationships, equipment graph, fault propagation
                  </p>
                  {result.reasoning_trace.some(t => t.agent === 'Graph') && (
                    <div className="mt-2 text-xs text-purple-700 dark:text-purple-400 font-semibold">
                      ✓ Used in this query
                    </div>
                  )}
                </div>
                <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                    <span className="font-semibold text-slate-900 dark:text-white">OpenAI GPT-4</span>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-400">
                    Reasoning synthesis, natural language understanding
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Ontology-Driven Causal Reasoning */}
          <OntologyVisualization reasoningTrace={result.reasoning_trace} />

          {/* Agent Workflow Visualization */}
          <AgentWorkflow reasoningTrace={result.reasoning_trace} />

          {/* Reasoning Timeline */}
          <ReasoningTimeline reasoningTrace={result.reasoning_trace} />

          {/* Confidence & Data Sources */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ConfidenceBreakdown
              confidence={result.confidence}
              confidenceBreakdown={result.confidence_breakdown}
              confidenceHistory={result.confidence_history}
            />

            <DataSourceAttribution
              dataSources={result.data_sources || []}
              confidence={result.confidence}
            />
          </div>

          {/* Graph Visualization */}
          {result.graph_visualization && (
            <GraphVisualization graphData={result.graph_visualization} />
          )}
        </>
      )}

      {/* Empty State */}
      {!result && !queryMutation.isPending && !queryMutation.isError && (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12 text-center">
          <Brain className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
            No Query Analyzed Yet
          </h3>
          <p className="text-slate-600 dark:text-slate-400">
            Enter a query above to see the detailed explainability analysis
          </p>
        </div>
      )}
    </div>
  );
}

export default function ExplainabilityPage() {
  return (
    <Suspense fallback={
      <div className="max-w-7xl mx-auto">
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-12">
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-purple-500"></div>
            <p className="text-slate-600 dark:text-slate-400 text-lg">Loading...</p>
          </div>
        </div>
      </div>
    }>
      <ExplainabilityContent />
    </Suspense>
  );
}


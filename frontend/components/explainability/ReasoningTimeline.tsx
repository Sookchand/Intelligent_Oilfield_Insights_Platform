'use client';

import { useState } from 'react';
import { ReasoningStep } from '@/lib/api';
import { ChevronDown, ChevronUp, Code, Database as DatabaseIcon, Copy, Check } from 'lucide-react';

interface ReasoningTimelineProps {
  reasoningTrace: ReasoningStep[];
}

export default function ReasoningTimeline({ reasoningTrace }: ReasoningTimelineProps) {
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());
  const [copiedQuery, setCopiedQuery] = useState<string | null>(null);

  const toggleStep = (stepNumber: number) => {
    const newExpanded = new Set(expandedSteps);
    if (newExpanded.has(stepNumber)) {
      newExpanded.delete(stepNumber);
    } else {
      newExpanded.add(stepNumber);
    }
    setExpandedSteps(newExpanded);
  };

  const copyToClipboard = async (text: string, queryType: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedQuery(queryType);
      setTimeout(() => setCopiedQuery(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">
        Detailed Reasoning Timeline
      </h2>

      <div className="space-y-4">
        {reasoningTrace.map((step, idx) => {
          const isExpanded = expandedSteps.has(step.step);
          const hasQuery = step.sql_query || step.cypher_query;

          return (
            <div
              key={idx}
              className="border-l-4 border-blue-500 bg-slate-50 dark:bg-slate-900 rounded-r-lg overflow-hidden"
            >
              {/* Step Header */}
              <button
                onClick={() => toggleStep(step.step)}
                className="w-full px-4 py-3 flex items-center justify-between hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold text-sm">
                    {step.step}
                  </div>

                  <div className="text-left">
                    <h3 className="font-semibold text-slate-900 dark:text-white">
                      {step.agent} Agent
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                      {step.action}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  {step.duration_ms && (
                    <span className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                      {step.duration_ms.toFixed(0)}ms
                    </span>
                  )}

                  {hasQuery && (
                    <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-xs font-medium rounded">
                      Has Query
                    </span>
                  )}

                  {isExpanded ? (
                    <ChevronUp className="w-5 h-5 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-slate-400" />
                  )}
                </div>
              </button>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="px-4 pb-4 space-y-3">
                  {/* Result */}
                  <div>
                    <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase mb-2">
                      Result
                    </h4>
                    <p className="text-sm text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 rounded p-3">
                      {step.result}
                    </p>
                  </div>

                  {/* SQL Query */}
                  {step.sql_query && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <DatabaseIcon className="w-4 h-4 text-green-600 dark:text-green-400" />
                          <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">
                            SQL Query (PostgreSQL)
                          </h4>
                        </div>
                        <button
                          onClick={() => copyToClipboard(step.sql_query!, `sql-${step.step}`)}
                          className="flex items-center space-x-1 px-2 py-1 text-xs bg-slate-700 hover:bg-slate-600 text-white rounded transition-colors"
                          title="Copy SQL query"
                        >
                          {copiedQuery === `sql-${step.step}` ? (
                            <>
                              <Check className="w-3 h-3" />
                              <span>Copied!</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy</span>
                            </>
                          )}
                        </button>
                      </div>
                      <pre className="text-xs bg-slate-900 text-green-400 rounded p-3 overflow-x-auto">
                        <code>{step.sql_query}</code>
                      </pre>
                    </div>
                  )}

                  {/* Cypher Query */}
                  {step.cypher_query && (
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <Code className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                          <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">
                            Cypher Query (Neo4j)
                          </h4>
                        </div>
                        <button
                          onClick={() => copyToClipboard(step.cypher_query!, `cypher-${step.step}`)}
                          className="flex items-center space-x-1 px-2 py-1 text-xs bg-slate-700 hover:bg-slate-600 text-white rounded transition-colors"
                          title="Copy Cypher query"
                        >
                          {copiedQuery === `cypher-${step.step}` ? (
                            <>
                              <Check className="w-3 h-3" />
                              <span>Copied!</span>
                            </>
                          ) : (
                            <>
                              <Copy className="w-3 h-3" />
                              <span>Copy</span>
                            </>
                          )}
                        </button>
                      </div>
                      <pre className="text-xs bg-slate-900 text-purple-400 rounded p-3 overflow-x-auto">
                        <code>{step.cypher_query}</code>
                      </pre>
                    </div>
                  )}

                  {/* Sample Results */}
                  {step.sample_results && step.sample_results.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase mb-2">
                        Sample Results (First {step.sample_results.length} of {step.details?.records_count || step.details?.items_found || step.sample_results.length})
                      </h4>
                      <div className="bg-white dark:bg-slate-800 rounded p-3 overflow-x-auto">
                        <table className="min-w-full text-xs">
                          <thead>
                            <tr className="border-b border-slate-200 dark:border-slate-700">
                              {Object.keys(step.sample_results[0]).map((key) => (
                                <th key={key} className="text-left py-2 px-3 font-semibold text-slate-600 dark:text-slate-400">
                                  {key}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {step.sample_results.map((row, idx) => (
                              <tr key={idx} className="border-b border-slate-100 dark:border-slate-800">
                                {Object.values(row).map((value: any, colIdx) => (
                                  <td key={colIdx} className="py-2 px-3 text-slate-700 dark:text-slate-300">
                                    {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Causal Explanation (Ontology Reasoning) */}
                  {step.causal_explanation && (
                    <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 border-l-4 border-amber-500 rounded p-4">
                      <div className="flex items-start space-x-3">
                        <div className="flex-shrink-0">
                          <svg className="w-6 h-6 text-amber-600 dark:text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                          </svg>
                        </div>
                        <div className="flex-1">
                          <h4 className="text-sm font-bold text-amber-900 dark:text-amber-200 mb-2 flex items-center">
                            🧠 Causal Reasoning (Ontology-Driven)
                          </h4>
                          <p className="text-sm text-amber-800 dark:text-amber-300 mb-3 leading-relaxed">
                            {step.causal_explanation}
                          </p>
                          {step.domain_knowledge && (
                            <div className="mt-3 pt-3 border-t border-amber-200 dark:border-amber-700">
                              <p className="text-xs font-semibold text-amber-700 dark:text-amber-400 mb-1">
                                📚 Domain Knowledge:
                              </p>
                              <p className="text-xs text-amber-700 dark:text-amber-400 italic">
                                {step.domain_knowledge}
                              </p>
                            </div>
                          )}
                          {step.details?.rule_name && (
                            <div className="mt-2 flex items-center space-x-2 text-xs text-amber-600 dark:text-amber-500">
                              <span className="font-mono bg-amber-100 dark:bg-amber-900/40 px-2 py-1 rounded">
                                Rule: {step.details.rule_id}
                              </span>
                              <span>•</span>
                              <span>Confidence: {(step.details.confidence * 100).toFixed(0)}%</span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Additional Details */}
                  {step.details && (
                    <div>
                      <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase mb-2">
                        Additional Details
                      </h4>
                      <pre className="text-xs bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded p-3 overflow-x-auto">
                        {JSON.stringify(step.details, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Expand/Collapse All */}
      <div className="mt-4 flex justify-center">
        <button
          onClick={() => {
            if (expandedSteps.size === reasoningTrace.length) {
              setExpandedSteps(new Set());
            } else {
              setExpandedSteps(new Set(reasoningTrace.map(s => s.step)));
            }
          }}
          className="px-4 py-2 text-sm text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
        >
          {expandedSteps.size === reasoningTrace.length ? 'Collapse All' : 'Expand All'}
        </button>
      </div>
    </div>
  );
}


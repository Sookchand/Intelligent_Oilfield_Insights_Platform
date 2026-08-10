'use client';

import { QueryResponse } from '@/lib/api';
import { Brain, Download, Share2, ExternalLink } from 'lucide-react';
import Link from 'next/link';
import { useEffect, useState } from 'react';

interface ResultsDisplayProps {
  query: string;
  result: QueryResponse;
}

export default function ResultsDisplay({ query, result }: ResultsDisplayProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  // Typewriter effect for answer
  useEffect(() => {
    setDisplayedText('');
    setIsTyping(true);
    let currentIndex = 0;

    const interval = setInterval(() => {
      if (currentIndex < result.answer.length) {
        setDisplayedText(result.answer.slice(0, currentIndex + 1));
        currentIndex++;
      } else {
        setIsTyping(false);
        clearInterval(interval);
      }
    }, 20);

    return () => clearInterval(interval);
  }, [result.answer]);

  const confidenceColor =
    result.confidence >= 0.8 ? 'text-green-600 dark:text-green-400' :
      result.confidence >= 0.6 ? 'text-yellow-600 dark:text-yellow-400' :
        'text-red-600 dark:text-red-400';

  const confidenceBg =
    result.confidence >= 0.8 ? 'bg-green-100 dark:bg-green-900/30' :
      result.confidence >= 0.6 ? 'bg-yellow-100 dark:bg-yellow-900/30' :
        'bg-red-100 dark:bg-red-900/30';

  return (
    <div className="space-y-6">
      {/* Main Answer Card */}
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Brain className="w-6 h-6 text-white" />
              <div>
                <h2 className="text-white font-semibold">AI Analysis Result</h2>
                <p className="text-blue-100 text-sm">Query: {query}</p>
              </div>
            </div>

            <div className={`px-4 py-2 ${confidenceBg} rounded-lg`}>
              <span className={`text-sm font-bold ${confidenceColor}`}>
                {Math.round(result.confidence * 100)}% Confidence
              </span>
            </div>
          </div>
        </div>

        {/* Answer */}
        <div className="p-6">
          <div className="prose dark:prose-invert max-w-none">
            <p className="text-lg text-slate-700 dark:text-slate-300 leading-relaxed">
              {displayedText}
              {isTyping && <span className="animate-pulse">|</span>}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3 mt-6 pt-6 border-t border-slate-200 dark:border-slate-700">
            <Link
              href={`/explainability?query=${encodeURIComponent(query)}`}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              <Brain className="w-4 h-4" />
              <span>View Explainability</span>
              <ExternalLink className="w-3 h-3" />
            </Link>

            <button className="flex items-center space-x-2 px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors">
              <Download className="w-4 h-4" />
              <span>Download Report</span>
            </button>

            <button className="flex items-center space-x-2 px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors">
              <Share2 className="w-4 h-4" />
              <span>Share</span>
            </button>
          </div>
        </div>
      </div>

      {/* Quick Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Data Sources */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-3">
            Data Sources Used
          </h3>
          <div className="space-y-2">
            {result.data_sources?.map((source, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <span className="text-sm text-slate-700 dark:text-slate-300">
                  {source.database}
                </span>
                <span className="text-xs text-slate-500 dark:text-slate-400">
                  {source.records || source.paths} records
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Reasoning Steps */}
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-4">
          <h3 className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-3">
            Processing Steps
          </h3>
          <div className="space-y-2">
            {result.reasoning_trace.slice(0, 5).map((step, idx) => (
              <div key={idx} className="flex items-center space-x-2">
                <div className="w-6 h-6 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-xs font-bold">
                  {step.step}
                </div>
                <span className="text-sm text-slate-700 dark:text-slate-300">
                  {step.agent}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Graph Path */}
        {result.graph_path && (
          <div className="bg-white dark:bg-slate-800 rounded-lg shadow p-4">
            <h3 className="text-sm font-semibold text-slate-600 dark:text-slate-400 mb-3">
              Equipment Path
            </h3>
            <div className="flex items-center space-x-2">
              {result.graph_path.map((node, idx) => (
                <div key={idx} className="flex items-center">
                  <span className="px-2 py-1 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded text-xs font-medium">
                    {node}
                  </span>
                  {idx < result.graph_path!.length - 1 && (
                    <span className="mx-1 text-slate-400">→</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Professional Footer Note */}
      <div className="bg-slate-50 dark:bg-slate-800/50 rounded-lg p-4 border border-slate-200 dark:border-slate-700">
        <p className="text-xs text-slate-600 dark:text-slate-400 text-center">
          💡 <strong>Tip:</strong> Use the main search bar above to ask follow-up questions or explore related topics
        </p>
      </div>
    </div>
  );
}


'use client';

import { ConfidenceBreakdown as ConfidenceBreakdownType, ConfidenceHistory } from '@/lib/api';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ConfidenceBreakdownProps {
  confidence: number;
  confidenceBreakdown?: ConfidenceBreakdownType;
  confidenceHistory?: ConfidenceHistory[];
}

export default function ConfidenceBreakdown({ 
  confidence, 
  confidenceBreakdown,
  confidenceHistory 
}: ConfidenceBreakdownProps) {
  const getConfidenceColor = (value: number) => {
    if (value >= 0.8) return 'text-green-600 dark:text-green-400';
    if (value >= 0.6) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  const getConfidenceBg = (value: number) => {
    if (value >= 0.8) return 'bg-green-500';
    if (value >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const breakdownItems = confidenceBreakdown ? [
    { label: 'Data Freshness', value: confidenceBreakdown.data_freshness },
    { label: 'Source Reliability', value: confidenceBreakdown.source_reliability },
    { label: 'Query Clarity', value: confidenceBreakdown.query_clarity },
    { label: 'Data Coverage', value: confidenceBreakdown.data_coverage },
  ] : [];

  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-6">
        Confidence Analysis
      </h2>

      {/* Overall Confidence */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-slate-600 dark:text-slate-400">
            Overall Confidence
          </span>
          <span className={`text-2xl font-bold ${getConfidenceColor(confidence)}`}>
            {Math.round(confidence * 100)}%
          </span>
        </div>
        
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3 overflow-hidden">
          <div
            className={`h-full ${getConfidenceBg(confidence)} transition-all duration-500`}
            style={{ width: `${confidence * 100}%` }}
          ></div>
        </div>

        <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
          {confidence >= 0.8 && 'High confidence - Result is highly reliable'}
          {confidence >= 0.6 && confidence < 0.8 && 'Medium confidence - Result is reasonably reliable'}
          {confidence < 0.6 && 'Low confidence - Result should be verified'}
        </p>
      </div>

      {/* Breakdown Factors */}
      {breakdownItems.length > 0 && (
        <div className="space-y-4 mb-6">
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            Contributing Factors
          </h3>
          
          {breakdownItems.map((item, idx) => (
            <div key={idx}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm text-slate-600 dark:text-slate-400">
                  {item.label}
                </span>
                <span className={`text-sm font-semibold ${getConfidenceColor(item.value)}`}>
                  {Math.round(item.value * 100)}%
                </span>
              </div>
              
              <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                <div
                  className={`h-full ${getConfidenceBg(item.value)} transition-all duration-500`}
                  style={{ width: `${item.value * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Confidence History */}
      {confidenceHistory && confidenceHistory.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
            Confidence Evolution
          </h3>
          
          <div className="space-y-2">
            {confidenceHistory.map((history, idx) => {
              const prevConfidence = idx > 0 ? confidenceHistory[idx - 1].confidence : history.confidence;
              const change = history.confidence - prevConfidence;
              
              return (
                <div
                  key={idx}
                  className="flex items-start space-x-3 p-3 bg-slate-50 dark:bg-slate-900 rounded-lg"
                >
                  <div className="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
                    {history.step}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        {history.agent}
                      </span>
                      
                      <div className="flex items-center space-x-2">
                        <span className={`text-sm font-semibold ${getConfidenceColor(history.confidence)}`}>
                          {Math.round(history.confidence * 100)}%
                        </span>
                        
                        {change !== 0 && (
                          <span className={`flex items-center text-xs ${
                            change > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                          }`}>
                            {change > 0 ? (
                              <TrendingUp className="w-3 h-3" />
                            ) : change < 0 ? (
                              <TrendingDown className="w-3 h-3" />
                            ) : (
                              <Minus className="w-3 h-3" />
                            )}
                            {Math.abs(change * 100).toFixed(0)}%
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      {history.reason}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}


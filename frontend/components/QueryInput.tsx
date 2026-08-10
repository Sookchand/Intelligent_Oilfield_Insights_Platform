'use client';

import { useState, useEffect } from 'react';
import { Search, Bookmark, Clock } from 'lucide-react';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

export default function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [query, setQuery] = useState('');
  const [queryHistory, setQueryHistory] = useState<string[]>([]);
  const [bookmarks, setBookmarks] = useState<string[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // Load history and bookmarks from localStorage
  useEffect(() => {
    const history = localStorage.getItem('queryHistory');
    const savedBookmarks = localStorage.getItem('queryBookmarks');
    
    if (history) setQueryHistory(JSON.parse(history));
    if (savedBookmarks) setBookmarks(JSON.parse(savedBookmarks));
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    // Add to history
    const newHistory = [query, ...queryHistory.filter(q => q !== query)].slice(0, 10);
    setQueryHistory(newHistory);
    localStorage.setItem('queryHistory', JSON.stringify(newHistory));

    onSubmit(query);
  };

  const handleBookmark = () => {
    if (!query.trim()) return;
    
    const newBookmarks = bookmarks.includes(query)
      ? bookmarks.filter(b => b !== query)
      : [query, ...bookmarks];
    
    setBookmarks(newBookmarks);
    localStorage.setItem('queryBookmarks', JSON.stringify(newBookmarks));
  };

  const selectFromHistory = (historicalQuery: string) => {
    setQuery(historicalQuery);
    setShowHistory(false);
  };

  return (
    <div className="relative">
      <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onFocus={() => setShowHistory(true)}
              onBlur={() => setTimeout(() => setShowHistory(false), 200)}
              placeholder="Ask about production, equipment, safety, or forecasts..."
              className="w-full pl-12 pr-4 py-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-900 dark:text-white placeholder-slate-400"
              disabled={isLoading}
            />

            {/* History Dropdown */}
            {showHistory && (queryHistory.length > 0 || bookmarks.length > 0) && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-xl z-10 max-h-64 overflow-y-auto">
                {bookmarks.length > 0 && (
                  <div className="p-2 border-b border-slate-200 dark:border-slate-700">
                    <div className="flex items-center space-x-2 px-2 py-1 text-xs font-semibold text-slate-500 dark:text-slate-400">
                      <Bookmark className="w-3 h-3" />
                      <span>BOOKMARKS</span>
                    </div>
                    {bookmarks.map((bookmark, idx) => (
                      <button
                        key={`bookmark-${idx}`}
                        onClick={() => selectFromHistory(bookmark)}
                        className="w-full text-left px-3 py-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded text-sm text-slate-700 dark:text-slate-300"
                      >
                        {bookmark}
                      </button>
                    ))}
                  </div>
                )}
                
                {queryHistory.length > 0 && (
                  <div className="p-2">
                    <div className="flex items-center space-x-2 px-2 py-1 text-xs font-semibold text-slate-500 dark:text-slate-400">
                      <Clock className="w-3 h-3" />
                      <span>RECENT</span>
                    </div>
                    {queryHistory.map((histQuery, idx) => (
                      <button
                        key={`history-${idx}`}
                        onClick={() => selectFromHistory(histQuery)}
                        className="w-full text-left px-3 py-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded text-sm text-slate-700 dark:text-slate-300"
                      >
                        {histQuery}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          <button
            type="button"
            onClick={handleBookmark}
            className={`p-4 rounded-lg transition-colors ${
              bookmarks.includes(query)
                ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-600 dark:text-yellow-400'
                : 'bg-slate-100 dark:bg-slate-700 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'
            }`}
            disabled={!query.trim()}
          >
            <Bookmark className="w-5 h-5" />
          </button>

          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="px-8 py-4 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg font-semibold hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl"
          >
            {isLoading ? 'Processing...' : 'Ask AI'}
          </button>
        </div>
      </form>
    </div>
  );
}


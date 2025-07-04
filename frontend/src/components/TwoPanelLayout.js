import React, { useState } from 'react';

const TwoPanelLayout = ({ 
  leftPanel, 
  rightPanel, 
  leftPanelTitle, 
  rightPanelTitle,
  leftPanelActions,
  rightPanelActions,
  searchable = true,
  onSearch
}) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (query) => {
    setSearchQuery(query);
    if (onSearch) {
      onSearch(query);
    }
  };

  return (
    <div className="flex h-full bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      {/* Left Panel */}
      <div className="w-3/5 border-r border-gray-200 flex flex-col">
        {/* Left Panel Header */}
        <div className="bg-gray-50 border-b border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-semibold text-gray-900">{leftPanelTitle}</h3>
            {leftPanelActions && (
              <div className="flex space-x-2">
                {leftPanelActions}
              </div>
            )}
          </div>
          
          {searchable && (
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-gray-400">🔍</span>
              </div>
              <input
                type="text"
                placeholder="Search..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
            </div>
          )}
        </div>
        
        {/* Left Panel Content */}
        <div className="flex-1 overflow-y-auto">
          {leftPanel}
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-2/5 flex flex-col">
        {/* Right Panel Header */}
        <div className="bg-gray-50 border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">{rightPanelTitle}</h3>
            {rightPanelActions && (
              <div className="flex space-x-2">
                {rightPanelActions}
              </div>
            )}
          </div>
        </div>
        
        {/* Right Panel Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {rightPanel}
        </div>
      </div>
    </div>
  );
};

export default TwoPanelLayout;
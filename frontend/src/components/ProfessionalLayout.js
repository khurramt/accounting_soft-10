import React, { useState } from 'react';
import GlobalSearch from './GlobalSearch';

const ProfessionalLayout = ({ children, currentPage, onPageChange, companyName }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [showGlobalSearch, setShowGlobalSearch] = useState(false);

  const handleSearchNavigation = (page, id) => {
    onPageChange(page);
    setShowGlobalSearch(false);
    // Additional logic to select specific item if needed
  };

  const menuItems = [
    {
      category: 'Home',
      items: [
        { id: 'dashboard', label: 'Company Snapshot', icon: '📊' },
      ]
    },
    {
      category: 'Lists',
      items: [
        { id: 'accounts', label: 'Chart of Accounts', icon: '💼' },
        { id: 'items', label: 'Items & Services', icon: '📦' },
        { id: 'lists', label: 'All Lists', icon: '📝' },
      ]
    },
    {
      category: 'Customers',
      items: [
        { id: 'customers', label: 'Customer Center', icon: '👥' },
        { id: 'invoices', label: 'Create Invoices', icon: '📄' },
        { id: 'sales-receipts', label: 'Sales Receipts', icon: '🧾' },
        { id: 'estimates', label: 'Estimates', icon: '📋' },
        { id: 'receive-payments', label: 'Receive Payments', icon: '💰' },
      ]
    },
    {
      category: 'Vendors',
      items: [
        { id: 'vendors', label: 'Vendor Center', icon: '🏢' },
        { id: 'bills', label: 'Enter Bills', icon: '📋' },
        { id: 'pay-bills', label: 'Pay Bills', icon: '💳' },
        { id: 'purchase-orders', label: 'Purchase Orders', icon: '📑' },
        { id: 'checks', label: 'Write Checks', icon: '✏️' },
      ]
    },
    {
      category: 'Employees',
      items: [
        { id: 'employees', label: 'Employee Center', icon: '👤' },
        { id: 'payroll', label: 'Payroll', icon: '💰' },
        { id: 'time-tracking', label: 'Time Tracking', icon: '⏱️' },
      ]
    },
    {
      category: 'Banking',
      items: [
        { id: 'transfers', label: 'Transfer Funds', icon: '🔄' },
        { id: 'deposits', label: 'Make Deposits', icon: '🏦' },
        { id: 'reconcile', label: 'Reconcile', icon: '⚖️' },
        { id: 'bank-feeds', label: 'Bank Feeds', icon: '🔗' },
      ]
    },
    {
      category: 'Reports',
      items: [
        { id: 'reports', label: 'Reports Center', icon: '📊' },
        { id: 'budgets', label: 'Budgets', icon: '📈' },
      ]
    },
    {
      category: 'Company',
      items: [
        { id: 'memorized-transactions', label: 'Memorized Transactions', icon: '💾' },
        { id: 'calendar', label: 'Calendar', icon: '📅' },
        { id: 'audit-trail', label: 'Audit Trail', icon: '🔍' },
        { id: 'users', label: 'Users & Roles', icon: '👥' },
        { id: 'preferences', label: 'Preferences', icon: '⚙️' },
      ]
    }
  ];

  const toolbarItems = [
    { id: 'dashboard', label: 'Home', icon: '🏠' },
    { id: 'customers', label: 'Customers', icon: '👥' },
    { id: 'vendors', label: 'Vendors', icon: '🏢' },
    { id: 'employees', label: 'Employees', icon: '👤' },
    { id: 'items', label: 'Items & Services', icon: '📦' },
    { id: 'accounts', label: 'Chart of Accounts', icon: '💼' },
    { id: 'banking', label: 'Banking', icon: '🏦' },
    { id: 'reports', label: 'Reports', icon: '📊' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Menu Bar */}
      <div className="bg-white border-b border-gray-200 px-6 py-1">
        <div className="flex items-center space-x-6 text-sm">
          <div className="font-medium text-gray-900">File</div>
          <div className="font-medium text-gray-900">Edit</div>
          <div className="font-medium text-gray-900">View</div>
          <div className="font-medium text-gray-900">Lists</div>
          <div className="font-medium text-gray-900">Company</div>
          <div className="font-medium text-gray-900">Customers</div>
          <div className="font-medium text-gray-900">Vendors</div>
          <div className="font-medium text-gray-900">Employees</div>
          <div className="font-medium text-gray-900">Banking</div>
          <div className="font-medium text-gray-900">Reports</div>
          <div className="font-medium text-gray-900">Window</div>
          <div className="font-medium text-gray-900">Help</div>
        </div>
      </div>

      {/* Title Bar */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-white bg-opacity-20 rounded-lg flex items-center justify-center">
              <span className="text-sm font-bold">QB</span>
            </div>
            <div>
              <div className="font-bold text-lg">
                {companyName || 'QBClone'} – QBClone Pro
              </div>
              <div className="text-xs text-blue-100">
                Professional Accounting Software
              </div>
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Global Search */}
          <div className="relative">
            <button
              onClick={() => setShowGlobalSearch(!showGlobalSearch)}
              className="p-2 bg-white bg-opacity-20 rounded-lg hover:bg-opacity-30 transition-all"
            >
              🔍
            </button>
          </div>
          
          <div className="flex items-center space-x-2">
            <span className="text-sm">Admin User</span>
            <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <span className="text-sm font-medium">A</span>
            </div>
          </div>
        </div>
      </div>

      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="flex items-center space-x-1">
          {toolbarItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-lg transition-all text-xs ${
                currentPage === item.id
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
          
          <div className="flex-1"></div>
          
          <button
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            {sidebarCollapsed ? '▶️' : '◀️'}
          </button>
        </div>
      </div>

      <div className="flex flex-1">
        {/* Navigation Sidebar */}
        <nav className={`bg-white border-r border-gray-200 transition-all duration-300 ${
          sidebarCollapsed ? 'w-16' : 'w-64'
        }`}>
          <div className="p-4 h-full overflow-y-auto">
            {!sidebarCollapsed && (
              <div className="space-y-6">
                {menuItems.map((section) => (
                  <div key={section.category}>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-3 py-2">
                      {section.category}
                    </div>
                    <div className="space-y-1">
                      {section.items.map((item) => (
                        <button
                          key={item.id}
                          onClick={() => onPageChange(item.id)}
                          className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-all text-sm ${
                            currentPage === item.id
                              ? 'bg-blue-100 text-blue-700 font-medium'
                              : 'text-gray-600 hover:bg-gray-100'
                          }`}
                        >
                          <span className="text-base">{item.icon}</span>
                          <span>{item.label}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {sidebarCollapsed && (
              <div className="space-y-2">
                {toolbarItems.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => onPageChange(item.id)}
                    className={`w-full flex items-center justify-center p-3 rounded-lg transition-all ${
                      currentPage === item.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                    title={item.label}
                  >
                    <span className="text-lg">{item.icon}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Status Bar */}
      <div className="bg-gray-100 border-t border-gray-200 px-6 py-2">
        <div className="flex items-center justify-between text-xs text-gray-600">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Online</span>
            </div>
            <div>Company: {companyName || 'QBClone'}.qbw</div>
            <div>User: Admin</div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div>{new Date().toLocaleString()}</div>
            <div>Memory: 125 MB</div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Single User</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessionalLayout;
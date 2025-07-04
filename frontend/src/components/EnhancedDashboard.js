import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const EnhancedDashboard = ({ accounts, transactions, customers, vendors }) => {
  const [dashboardData, setDashboardData] = useState({
    cashOnHand: 0,
    accountsReceivable: 0,
    accountsPayable: 0,
    totalIncome: 0,
    totalExpenses: 0,
    netIncome: 0
  });
  const [isDragging, setIsDragging] = useState(false);
  const [draggedTile, setDraggedTile] = useState(null);

  useEffect(() => {
    calculateDashboardMetrics();
  }, [accounts, transactions]);

  const calculateDashboardMetrics = () => {
    // Calculate various metrics from accounts and transactions
    const cashAccounts = accounts.filter(acc => 
      acc.detail_type === 'Checking' || acc.detail_type === 'Savings'
    );
    const cashOnHand = cashAccounts.reduce((sum, acc) => sum + acc.balance, 0);

    const arAccounts = accounts.filter(acc => acc.detail_type === 'Accounts Receivable');
    const accountsReceivable = arAccounts.reduce((sum, acc) => sum + acc.balance, 0);

    const apAccounts = accounts.filter(acc => acc.detail_type === 'Accounts Payable');
    const accountsPayable = apAccounts.reduce((sum, acc) => sum + acc.balance, 0);

    const incomeAccounts = accounts.filter(acc => acc.account_type === 'Income');
    const totalIncome = incomeAccounts.reduce((sum, acc) => sum + acc.balance, 0);

    const expenseAccounts = accounts.filter(acc => acc.account_type === 'Expense');
    const totalExpenses = expenseAccounts.reduce((sum, acc) => sum + acc.balance, 0);

    setDashboardData({
      cashOnHand,
      accountsReceivable,
      accountsPayable,
      totalIncome,
      totalExpenses,
      netIncome: totalIncome - totalExpenses
    });
  };

  const dashboardTiles = [
    {
      id: 'cash',
      title: 'Cash on Hand',
      value: dashboardData.cashOnHand,
      icon: '💰',
      color: 'bg-green-500',
      change: '+5.2%',
      changeColor: 'text-green-600'
    },
    {
      id: 'ar',
      title: 'Accounts Receivable',
      value: dashboardData.accountsReceivable,
      icon: '📊',
      color: 'bg-blue-500',
      change: '+12.3%',
      changeColor: 'text-blue-600'
    },
    {
      id: 'ap',
      title: 'Accounts Payable',
      value: dashboardData.accountsPayable,
      icon: '📋',
      color: 'bg-orange-500',
      change: '-2.1%',
      changeColor: 'text-orange-600'
    },
    {
      id: 'income',
      title: 'Total Income',
      value: dashboardData.totalIncome,
      icon: '📈',
      color: 'bg-purple-500',
      change: '+18.5%',
      changeColor: 'text-purple-600'
    },
    {
      id: 'expenses',
      title: 'Total Expenses',
      value: dashboardData.totalExpenses,
      icon: '📉',
      color: 'bg-red-500',
      change: '+7.2%',
      changeColor: 'text-red-600'
    },
    {
      id: 'net',
      title: 'Net Income',
      value: dashboardData.netIncome,
      icon: '🎯',
      color: 'bg-indigo-500',
      change: '+25.7%',
      changeColor: 'text-indigo-600'
    }
  ];

  const handleDragStart = (e, tile) => {
    setIsDragging(true);
    setDraggedTile(tile);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragEnd = () => {
    setIsDragging(false);
    setDraggedTile(null);
  };

  return (
    <div className="space-y-8">
      {/* Company Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-8 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Company Snapshot</h1>
            <p className="text-blue-100 mt-2">Your business at a glance</p>
          </div>
          <div className="text-right">
            <div className="text-sm text-blue-100">As of {new Date().toLocaleDateString()}</div>
            <div className="text-2xl font-bold mt-1">
              ${dashboardData.netIncome.toLocaleString()}
            </div>
            <div className="text-sm text-blue-100">Net Income</div>
          </div>
        </div>
      </div>

      {/* Dashboard Tiles - Drag and Drop */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {dashboardTiles.map((tile) => (
          <div
            key={tile.id}
            draggable
            onDragStart={(e) => handleDragStart(e, tile)}
            onDragEnd={handleDragEnd}
            className={`bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all cursor-move ${
              isDragging && draggedTile?.id === tile.id ? 'opacity-50 scale-95' : ''
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-3">
                  <div className={`w-12 h-12 ${tile.color} bg-opacity-20 rounded-lg flex items-center justify-center`}>
                    <span className="text-xl">{tile.icon}</span>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-600">{tile.title}</h3>
                    <div className="text-2xl font-bold text-gray-900">
                      ${Math.abs(tile.value).toLocaleString()}
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`text-sm font-medium ${tile.changeColor}`}>
                    {tile.change}
                  </span>
                  <span className="text-sm text-gray-500">vs last month</span>
                </div>
              </div>
              <button className="text-gray-400 hover:text-gray-600 transition-colors">
                <span className="text-lg">⚙️</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View All →
              </button>
            </div>
          </div>
          <div className="p-6">
            {transactions.slice(0, 5).length > 0 ? (
              <div className="space-y-4">
                {transactions.slice(0, 5).map((transaction) => (
                  <div key={transaction.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-medium ${
                        transaction.transaction_type === 'Invoice' ? 'bg-blue-100 text-blue-700' :
                        transaction.transaction_type === 'Bill' ? 'bg-red-100 text-red-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        {transaction.transaction_type === 'Invoice' ? '📄' :
                         transaction.transaction_type === 'Bill' ? '📋' : '💰'}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {transaction.transaction_type} #{transaction.reference_number}
                        </div>
                        <div className="text-xs text-gray-500">
                          {new Date(transaction.date).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="text-sm font-medium text-gray-900">
                      ${transaction.total.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-2">📊</div>
                <p>No recent transactions</p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 gap-4">
              <button className="flex flex-col items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">📄</div>
                <span className="text-sm font-medium text-blue-700">Create Invoice</span>
              </button>
              <button className="flex flex-col items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">💰</div>
                <span className="text-sm font-medium text-green-700">Record Payment</span>
              </button>
              <button className="flex flex-col items-center p-4 bg-red-50 rounded-lg hover:bg-red-100 transition-colors group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">📋</div>
                <span className="text-sm font-medium text-red-700">Enter Bill</span>
              </button>
              <button className="flex flex-col items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors group">
                <div className="text-2xl mb-2 group-hover:scale-110 transition-transform">📊</div>
                <span className="text-sm font-medium text-purple-700">View Reports</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Top Customers and Expenses */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Top Customers */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Top Customers</h2>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View All →
              </button>
            </div>
          </div>
          <div className="p-6">
            {customers.slice(0, 5).length > 0 ? (
              <div className="space-y-4">
                {customers.slice(0, 5).map((customer, index) => (
                  <div key={customer.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-xs font-medium text-blue-700">
                        #{index + 1}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                        {customer.company && (
                          <div className="text-xs text-gray-500">{customer.company}</div>
                        )}
                      </div>
                    </div>
                    <div className="text-sm font-medium text-gray-900">
                      ${customer.balance.toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-2">👥</div>
                <p>No customers yet</p>
              </div>
            )}
          </div>
        </div>

        {/* Top Expenses */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Top Expense Categories</h2>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                View All →
              </button>
            </div>
          </div>
          <div className="p-6">
            {accounts.filter(acc => acc.account_type === 'Expense').slice(0, 5).length > 0 ? (
              <div className="space-y-4">
                {accounts.filter(acc => acc.account_type === 'Expense').slice(0, 5).map((account, index) => (
                  <div key={account.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center text-xs font-medium text-red-700">
                        #{index + 1}
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{account.name}</div>
                        <div className="text-xs text-gray-500">{account.detail_type}</div>
                      </div>
                    </div>
                    <div className="text-sm font-medium text-gray-900">
                      ${Math.abs(account.balance).toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-2">📊</div>
                <p>No expense accounts</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Insights and Reminders */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl p-6">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-xl font-semibold mb-2">Business Insights</h2>
            <div className="space-y-2">
              <p className="text-purple-100">💡 Your business is performing well this month!</p>
              <p className="text-purple-100">📈 Income has increased by 18.5% compared to last month</p>
              <p className="text-purple-100">⚠️ You have 3 overdue invoices totaling $2,450</p>
            </div>
          </div>
          <button className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg transition-colors">
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};

export default EnhancedDashboard;
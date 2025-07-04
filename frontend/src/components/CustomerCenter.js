import React, { useState } from 'react';
import axios from 'axios';
import TwoPanelLayout from './TwoPanelLayout';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CustomerCenter = ({ customers, terms, onRefresh }) => {
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [filteredCustomers, setFilteredCustomers] = useState(customers);
  const [showNewCustomerModal, setShowNewCustomerModal] = useState(false);
  const [activeTab, setActiveTab] = useState('summary');

  const handleSearch = (query) => {
    if (!query) {
      setFilteredCustomers(customers);
    } else {
      const filtered = customers.filter(customer =>
        customer.name.toLowerCase().includes(query.toLowerCase()) ||
        (customer.company && customer.company.toLowerCase().includes(query.toLowerCase())) ||
        (customer.email && customer.email.toLowerCase().includes(query.toLowerCase()))
      );
      setFilteredCustomers(filtered);
    }
  };

  const leftPanelActions = (
    <div className="flex space-x-2">
      <button
        onClick={() => setShowNewCustomerModal(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
      >
        + New Customer
      </button>
      <button className="px-3 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors text-sm">
        Import
      </button>
      <button className="px-3 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors text-sm">
        Export
      </button>
    </div>
  );

  const rightPanelActions = selectedCustomer && (
    <div className="flex space-x-2">
      <button className="px-3 py-2 text-blue-600 bg-blue-100 rounded-lg hover:bg-blue-200 transition-colors text-sm">
        Edit Customer
      </button>
      <button className="px-3 py-2 text-green-600 bg-green-100 rounded-lg hover:bg-green-200 transition-colors text-sm">
        Create Invoice
      </button>
    </div>
  );

  const leftPanel = (
    <div className="h-full">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 sticky top-0">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <input type="checkbox" className="rounded" />
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                Name ↕️
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                Type ↕️
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                Balance ↕️
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100">
                Total Sales ↕️
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredCustomers.map((customer) => (
              <tr 
                key={customer.id} 
                className={`hover:bg-blue-50 cursor-pointer transition-colors ${
                  selectedCustomer?.id === customer.id ? 'bg-blue-100' : ''
                }`}
                onClick={() => setSelectedCustomer(customer)}
              >
                <td className="px-4 py-3 whitespace-nowrap">
                  <input type="checkbox" className="rounded" onClick={(e) => e.stopPropagation()} />
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex flex-col">
                    <div className="text-sm font-medium text-gray-900">{customer.name}</div>
                    {customer.company && (
                      <div className="text-xs text-gray-500">{customer.company}</div>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                  Customer
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                  ${customer.balance.toLocaleString()}
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                  $0.00
                </td>
                <td className="px-4 py-3 whitespace-nowrap text-sm">
                  <div className="flex space-x-1">
                    <button 
                      className="text-blue-600 hover:text-blue-800 p-1 rounded hover:bg-blue-100"
                      onClick={(e) => e.stopPropagation()}
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button 
                      className="text-green-600 hover:text-green-800 p-1 rounded hover:bg-green-100"
                      onClick={(e) => e.stopPropagation()}
                      title="Create Invoice"
                    >
                      📄
                    </button>
                    <button 
                      className="text-gray-600 hover:text-gray-800 p-1 rounded hover:bg-gray-100"
                      onClick={(e) => e.stopPropagation()}
                      title="More Actions"
                    >
                      ⋯
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  const rightPanel = selectedCustomer ? (
    <div className="h-full">
      {/* Customer Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between">
          <div>
            <h3 className="text-xl font-bold text-gray-900">{selectedCustomer.name}</h3>
            {selectedCustomer.company && (
              <p className="text-gray-600">{selectedCustomer.company}</p>
            )}
            <div className="flex items-center space-x-4 mt-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                selectedCustomer.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {selectedCustomer.active ? 'Active' : 'Inactive'}
              </span>
              <span className="text-sm text-gray-500">
                Customer since {new Date(selectedCustomer.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">
              ${selectedCustomer.balance.toLocaleString()}
            </div>
            <div className="text-sm text-gray-500">Current Balance</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {['summary', 'transactions', 'notes', 'todos'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`py-2 px-1 border-b-2 font-medium text-sm capitalize ${
                activeTab === tab
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === 'summary' && (
          <div className="space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">$0.00</div>
                <div className="text-sm text-blue-800">Total Sales</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="text-2xl font-bold text-green-600">0</div>
                <div className="text-sm text-green-800">Open Invoices</div>
              </div>
            </div>

            {/* Contact Information */}
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Contact Information</h4>
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                {selectedCustomer.email && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Email:</span>
                    <span className="text-gray-900">{selectedCustomer.email}</span>
                  </div>
                )}
                {selectedCustomer.phone && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Phone:</span>
                    <span className="text-gray-900">{selectedCustomer.phone}</span>
                  </div>
                )}
                {selectedCustomer.address && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Address:</span>
                    <div className="text-right text-gray-900">
                      <div>{selectedCustomer.address}</div>
                      {(selectedCustomer.city || selectedCustomer.state || selectedCustomer.zip_code) && (
                        <div>
                          {selectedCustomer.city}{selectedCustomer.city && ', '}{selectedCustomer.state} {selectedCustomer.zip_code}
                        </div>
                      )}
                    </div>
                  </div>
                )}
                {selectedCustomer.terms && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Terms:</span>
                    <span className="text-gray-900">{selectedCustomer.terms}</span>
                  </div>
                )}
                {selectedCustomer.credit_limit && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Credit Limit:</span>
                    <span className="text-gray-900">${selectedCustomer.credit_limit.toLocaleString()}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Recent Activity */}
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Recent Activity</h4>
              <div className="bg-gray-50 p-4 rounded-lg text-center text-gray-500">
                No recent transactions
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transactions' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="text-lg font-semibold text-gray-900">Transactions</h4>
              <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                + New Transaction
              </button>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg text-center text-gray-500">
              No transactions found for this customer
            </div>
          </div>
        )}

        {activeTab === 'notes' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="text-lg font-semibold text-gray-900">Notes</h4>
              <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                + Add Note
              </button>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg text-center text-gray-500">
              No notes for this customer
            </div>
          </div>
        )}

        {activeTab === 'todos' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="text-lg font-semibold text-gray-900">To-Dos</h4>
              <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                + Add To-Do
              </button>
            </div>
            <div className="bg-gray-50 p-8 rounded-lg text-center text-gray-500">
              No to-dos for this customer
            </div>
          </div>
        )}
      </div>
    </div>
  ) : (
    <div className="h-full flex items-center justify-center text-gray-500">
      <div className="text-center">
        <div className="text-6xl mb-4">👥</div>
        <p className="text-lg">Select a customer to view details</p>
        <p className="text-sm">Choose a customer from the list to see their information and transactions</p>
      </div>
    </div>
  );

  return (
    <div className="h-[calc(100vh-200px)]">
      <TwoPanelLayout
        leftPanel={leftPanel}
        rightPanel={rightPanel}
        leftPanelTitle={`Customer Center (${filteredCustomers.length})`}
        rightPanelTitle={selectedCustomer ? selectedCustomer.name : "Customer Details"}
        leftPanelActions={leftPanelActions}
        rightPanelActions={rightPanelActions}
        searchable={true}
        onSearch={handleSearch}
      />

      {/* New Customer Modal - Placeholder */}
      {showNewCustomerModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">New Customer</h3>
            <p className="text-gray-600">Customer creation form will be implemented here...</p>
            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={() => setShowNewCustomerModal(false)}
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Create Customer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerCenter;
import React, { useState } from 'react';
import TransactionForm from './TransactionForm';
import TwoPanelLayout from './TwoPanelLayout';

const TransactionFormPage = ({ 
  transactionType, 
  customers = [], 
  vendors = [], 
  items = [], 
  accounts = [],
  classes = [],
  locations = [],
  terms = [],
  onRefresh
}) => {
  const [showForm, setShowForm] = useState(false);
  const [transactions, setTransactions] = useState([]);
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  const leftPanelActions = (
    <div className="flex space-x-2">
      <button
        onClick={() => setShowForm(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
      >
        + New {transactionType}
      </button>
      <button className="px-3 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors text-sm">
        Import
      </button>
      <button className="px-3 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors text-sm">
        Export
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
                Date
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {transactionType === 'Invoice' ? 'Invoice #' : 
                 transactionType === 'Bill' ? 'Ref #' :
                 transactionType === 'Estimate' ? 'Estimate #' :
                 transactionType === 'Purchase Order' ? 'PO #' : 'Number'}
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {['Invoice', 'Sales Receipt', 'Estimate'].includes(transactionType) ? 'Customer' : 'Vendor'}
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Amount
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-gray-500">
                  <div className="flex flex-col items-center">
                    <div className="text-4xl mb-2">
                      {transactionType === 'Invoice' ? '📄' :
                       transactionType === 'Bill' ? '📋' :
                       transactionType === 'Estimate' ? '📋' :
                       transactionType === 'Purchase Order' ? '📑' :
                       transactionType === 'Sales Receipt' ? '🧾' : '📄'}
                    </div>
                    <p>No {transactionType.toLowerCase()}s found</p>
                    <p className="text-sm">Create your first {transactionType.toLowerCase()} to get started</p>
                  </div>
                </td>
              </tr>
            ) : (
              transactions.map((transaction) => (
                <tr 
                  key={transaction.id} 
                  className="hover:bg-blue-50 cursor-pointer transition-colors"
                  onClick={() => setSelectedTransaction(transaction)}
                >
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                    {new Date(transaction.date).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                    {transaction.reference_number || 'AUTO'}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                    {transaction.customer_name || transaction.vendor_name || '-'}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                    ${transaction.total?.toLocaleString() || '0.00'}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-green-100 text-green-800">
                      {transaction.status || 'Active'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );

  const rightPanel = selectedTransaction ? (
    <div className="h-full">
      <div className="space-y-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {transactionType} Details
          </h3>
          <div className="bg-gray-50 p-4 rounded-lg space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Number:</span>
              <span className="text-gray-900">{selectedTransaction.reference_number}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Date:</span>
              <span className="text-gray-900">{new Date(selectedTransaction.date).toLocaleDateString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Amount:</span>
              <span className="text-gray-900 font-semibold">${selectedTransaction.total?.toLocaleString()}</span>
            </div>
          </div>
        </div>

        <div className="flex space-x-2">
          <button className="flex-1 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
            Edit
          </button>
          <button className="flex-1 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm">
            Print
          </button>
        </div>
      </div>
    </div>
  ) : (
    <div className="h-full flex items-center justify-center text-gray-500">
      <div className="text-center">
        <div className="text-6xl mb-4">
          {transactionType === 'Invoice' ? '📄' :
           transactionType === 'Bill' ? '📋' :
           transactionType === 'Estimate' ? '📋' :
           transactionType === 'Purchase Order' ? '📑' :
           transactionType === 'Sales Receipt' ? '🧾' : '📄'}
        </div>
        <p className="text-lg">Select a {transactionType.toLowerCase()}</p>
        <p className="text-sm">Choose from the list to view details</p>
      </div>
    </div>
  );

  if (showForm) {
    return (
      <TransactionForm
        transactionType={transactionType}
        customers={customers}
        vendors={vendors}
        items={items}
        accounts={accounts}
        classes={classes}
        locations={locations}
        terms={terms}
        onSave={() => {
          setShowForm(false);
          if (onRefresh) onRefresh();
        }}
        onCancel={() => setShowForm(false)}
      />
    );
  }

  return (
    <div className="h-[calc(100vh-200px)]">
      <TwoPanelLayout
        leftPanel={leftPanel}
        rightPanel={rightPanel}
        leftPanelTitle={`${transactionType} Center`}
        rightPanelTitle={selectedTransaction ? `${transactionType} Details` : `${transactionType} Information`}
        leftPanelActions={leftPanelActions}
        searchable={true}
      />
    </div>
  );
};

export default TransactionFormPage;
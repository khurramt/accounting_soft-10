import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const GlobalSearch = ({ isOpen, onClose, onNavigate }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    if (query.length >= 2) {
      performSearch();
    } else {
      setResults([]);
    }
    setSelectedIndex(-1);
  }, [query]);

  const performSearch = async () => {
    setLoading(true);
    try {
      // Simulate search across different entities
      const searchResults = [];

      // Search customers
      const customersResponse = await axios.get(`${API}/customers`);
      const customers = customersResponse.data.filter(customer =>
        customer.name.toLowerCase().includes(query.toLowerCase()) ||
        (customer.company && customer.company.toLowerCase().includes(query.toLowerCase())) ||
        (customer.email && customer.email.toLowerCase().includes(query.toLowerCase()))
      );
      
      customers.forEach(customer => {
        searchResults.push({
          type: 'customer',
          icon: '👥',
          title: customer.name,
          subtitle: customer.company || customer.email || 'Customer',
          action: () => onNavigate('customers', customer.id),
          data: customer
        });
      });

      // Search vendors
      const vendorsResponse = await axios.get(`${API}/vendors`);
      const vendors = vendorsResponse.data.filter(vendor =>
        vendor.name.toLowerCase().includes(query.toLowerCase()) ||
        (vendor.company && vendor.company.toLowerCase().includes(query.toLowerCase()))
      );
      
      vendors.forEach(vendor => {
        searchResults.push({
          type: 'vendor',
          icon: '🏢',
          title: vendor.name,
          subtitle: vendor.company || 'Vendor',
          action: () => onNavigate('vendors', vendor.id),
          data: vendor
        });
      });

      // Search accounts
      const accountsResponse = await axios.get(`${API}/accounts`);
      const accounts = accountsResponse.data.filter(account =>
        account.name.toLowerCase().includes(query.toLowerCase()) ||
        account.account_number?.includes(query)
      );
      
      accounts.forEach(account => {
        searchResults.push({
          type: 'account',
          icon: '💼',
          title: account.name,
          subtitle: `${account.account_type} - ${account.detail_type}`,
          action: () => onNavigate('accounts', account.id),
          data: account
        });
      });

      // Search transactions
      const transactionsResponse = await axios.get(`${API}/transactions`);
      const transactions = transactionsResponse.data.filter(transaction =>
        transaction.reference_number?.toLowerCase().includes(query.toLowerCase()) ||
        transaction.memo?.toLowerCase().includes(query.toLowerCase())
      );
      
      transactions.forEach(transaction => {
        searchResults.push({
          type: 'transaction',
          icon: getTransactionIcon(transaction.transaction_type),
          title: `${transaction.transaction_type} #${transaction.reference_number}`,
          subtitle: `$${transaction.total?.toLocaleString()} - ${new Date(transaction.date).toLocaleDateString()}`,
          action: () => onNavigate(getTransactionPage(transaction.transaction_type), transaction.id),
          data: transaction
        });
      });

      // Search items
      const itemsResponse = await axios.get(`${API}/items`);
      const items = itemsResponse.data.filter(item =>
        item.name.toLowerCase().includes(query.toLowerCase()) ||
        (item.description && item.description.toLowerCase().includes(query.toLowerCase()))
      );
      
      items.forEach(item => {
        searchResults.push({
          type: 'item',
          icon: '📦',
          title: item.name,
          subtitle: item.description || `${item.item_type} - $${item.price}`,
          action: () => onNavigate('items', item.id),
          data: item
        });
      });

      setResults(searchResults.slice(0, 10)); // Limit to 10 results
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const getTransactionIcon = (type) => {
    switch (type) {
      case 'Invoice': return '📄';
      case 'Bill': return '📋';
      case 'Sales Receipt': return '🧾';
      case 'Estimate': return '📋';
      case 'Purchase Order': return '📑';
      case 'Payment': return '💰';
      default: return '📄';
    }
  };

  const getTransactionPage = (type) => {
    switch (type) {
      case 'Invoice': return 'invoices';
      case 'Bill': return 'bills';
      case 'Sales Receipt': return 'sales-receipts';
      case 'Estimate': return 'estimates';
      case 'Purchase Order': return 'purchase-orders';
      case 'Payment': return 'receive-payments';
      default: return 'dashboard';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => (prev < results.length - 1 ? prev + 1 : prev));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => (prev > 0 ? prev - 1 : -1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && results[selectedIndex]) {
        results[selectedIndex].action();
        onClose();
      }
    }
  };

  const handleResultClick = (result) => {
    result.action();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-2xl mx-4">
        {/* Search Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <span className="text-gray-400 text-lg">🔍</span>
            </div>
            <input
              ref={inputRef}
              type="text"
              placeholder="Search customers, vendors, transactions, accounts..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full pl-10 pr-4 py-3 border-0 rounded-lg text-lg focus:ring-0 focus:outline-none"
            />
            <button
              onClick={onClose}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
            >
              <span className="text-lg">✕</span>
            </button>
          </div>
        </div>

        {/* Search Results */}
        <div className="max-h-96 overflow-y-auto">
          {loading && (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Searching...</p>
            </div>
          )}

          {!loading && query.length >= 2 && results.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              <div className="text-4xl mb-2">🔍</div>
              <p className="text-lg">No results found</p>
              <p className="text-sm">Try a different search term</p>
            </div>
          )}

          {!loading && results.length > 0 && (
            <div className="py-2">
              {results.map((result, index) => (
                <div
                  key={`${result.type}-${index}`}
                  onClick={() => handleResultClick(result)}
                  className={`px-4 py-3 cursor-pointer transition-colors ${
                    index === selectedIndex ? 'bg-blue-50' : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                      <span className="text-lg">{result.icon}</span>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {result.title}
                        </p>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                          result.type === 'customer' ? 'bg-blue-100 text-blue-800' :
                          result.type === 'vendor' ? 'bg-green-100 text-green-800' :
                          result.type === 'account' ? 'bg-purple-100 text-purple-800' :
                          result.type === 'transaction' ? 'bg-orange-100 text-orange-800' :
                          result.type === 'item' ? 'bg-gray-100 text-gray-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {result.type}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 truncate">
                        {result.subtitle}
                      </p>
                    </div>
                    <div className="text-gray-400">
                      <span className="text-sm">Enter ↵</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {query.length < 2 && (
            <div className="p-8 text-center text-gray-500">
              <div className="text-4xl mb-2">⌨️</div>
              <p className="text-lg">Start typing to search</p>
              <p className="text-sm">Search across customers, vendors, transactions, and more</p>
              
              <div className="mt-6 text-left max-w-md mx-auto">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Quick tips:</h4>
                <ul className="text-xs text-gray-500 space-y-1">
                  <li>• Use ↑ ↓ arrows to navigate results</li>
                  <li>• Press Enter to select</li>
                  <li>• Press Escape to close</li>
                  <li>• Search by name, number, or email</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default GlobalSearch;
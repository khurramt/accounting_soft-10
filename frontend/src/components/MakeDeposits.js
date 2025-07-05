import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MakeDeposits = ({ accounts, onRefresh }) => {
  const [undepositedPayments, setUndepositedPayments] = useState([]);
  const [selectedPayments, setSelectedPayments] = useState([]);
  const [formData, setFormData] = useState({
    deposit_date: new Date().toISOString().split('T')[0],
    deposit_to_account_id: '',
    memo: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [filters, setFilters] = useState({
    payment_method: '',
    date_range: 'all', // all, today, this_week, this_month
    search: ''
  });

  useEffect(() => {
    fetchUndepositedPayments();
  }, []);

  useEffect(() => {
    // Auto-select default checking account
    const checkingAccount = accounts.find(acc => 
      acc.detail_type === 'Checking' && acc.account_type === 'Asset'
    );
    if (checkingAccount && !formData.deposit_to_account_id) {
      setFormData(prev => ({ ...prev, deposit_to_account_id: checkingAccount.id }));
    }
  }, [accounts, formData.deposit_to_account_id]);

  const fetchUndepositedPayments = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/payments/undeposited`);
      const payments = response.data.map(payment => ({
        ...payment,
        customer_name: payment.customer_id || 'Cash Sale',
        check_number: payment.reference_number || payment.transaction_number
      }));
      setUndepositedPayments(payments);
    } catch (error) {
      console.error('Error fetching undeposited payments:', error);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredPayments = () => {
    let filtered = [...undepositedPayments];
    
    // Payment method filter
    if (filters.payment_method) {
      filtered = filtered.filter(payment => payment.payment_method === filters.payment_method);
    }
    
    // Search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(payment => 
        (payment.customer_name || '').toLowerCase().includes(searchLower) ||
        (payment.check_number || '').toLowerCase().includes(searchLower) ||
        (payment.memo || '').toLowerCase().includes(searchLower)
      );
    }
    
    // Date range filter
    const today = new Date();
    if (filters.date_range !== 'all') {
      filtered = filtered.filter(payment => {
        const paymentDate = new Date(payment.date);
        switch (filters.date_range) {
          case 'today':
            return paymentDate.toDateString() === today.toDateString();
          case 'this_week':
            const weekStart = new Date(today);
            weekStart.setDate(today.getDate() - today.getDay());
            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekStart.getDate() + 6);
            return paymentDate >= weekStart && paymentDate <= weekEnd;
          case 'this_month':
            return paymentDate.getMonth() === today.getMonth() && 
                   paymentDate.getFullYear() === today.getFullYear();
          default:
            return true;
        }
      });
    }
    
    return filtered.sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  const togglePaymentSelection = (payment) => {
    const isSelected = selectedPayments.find(p => p.id === payment.id);
    if (isSelected) {
      setSelectedPayments(selectedPayments.filter(p => p.id !== payment.id));
    } else {
      setSelectedPayments([...selectedPayments, payment]);
    }
  };

  const getTotalDepositAmount = () => {
    return selectedPayments.reduce((sum, payment) => sum + (payment.total || 0), 0);
  };

  const selectAllPayments = () => {
    const unselectedPayments = getFilteredPayments().filter(payment => 
      !selectedPayments.find(sp => sp.id === payment.id)
    );
    setSelectedPayments([...selectedPayments, ...unselectedPayments]);
  };

  const clearSelection = () => {
    setSelectedPayments([]);
  };

  const selectByPaymentMethod = (method) => {
    const methodPayments = getFilteredPayments().filter(payment => 
      payment.payment_method === method && !selectedPayments.find(sp => sp.id === payment.id)
    );
    setSelectedPayments([...selectedPayments, ...methodPayments]);
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (selectedPayments.length === 0) {
      newErrors.payments = 'Please select at least one payment to deposit';
    }
    
    if (!formData.deposit_date) {
      newErrors.deposit_date = 'Deposit date is required';
    }
    
    if (!formData.deposit_to_account_id) {
      newErrors.deposit_to_account_id = 'Deposit account is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const paymentItems = selectedPayments.map(payment => ({
        payment_id: payment.id,
        amount: payment.total
      }));

      const submitData = {
        deposit_date: new Date(formData.deposit_date),
        deposit_to_account_id: formData.deposit_to_account_id,
        payment_items: paymentItems,
        memo: formData.memo
      };

      await axios.post(`${API}/deposits`, submitData);
      
      // Reset form
      setSelectedPayments([]);
      setFormData({
        deposit_date: new Date().toISOString().split('T')[0],
        deposit_to_account_id: formData.deposit_to_account_id, // Keep selected account
        memo: ''
      });
      
      // Refresh data
      fetchUndepositedPayments();
      if (onRefresh) onRefresh();
      
    } catch (error) {
      console.error('Error processing deposit:', error);
      setErrors({ submit: 'Failed to process deposit. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const getPaymentMethodIcon = (method) => {
    switch (method) {
      case 'Cash': return '💵';
      case 'Check': return '📝';
      case 'Credit Card': return '💳';
      case 'Electronic': return '🔗';
      default: return '💰';
    }
  };

  const getPaymentMethodColor = (method) => {
    switch (method) {
      case 'Cash': return 'bg-green-100 text-green-800';
      case 'Check': return 'bg-blue-100 text-blue-800';
      case 'Credit Card': return 'bg-purple-100 text-purple-800';
      case 'Electronic': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredPayments = getFilteredPayments();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">Make Deposits</h2>
        <p className="text-blue-100">Deposit payments from Undeposited Funds to bank accounts</p>
      </div>

      {/* Filters and Quick Actions */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Payment Method</label>
            <select
              value={filters.payment_method}
              onChange={(e) => setFilters(prev => ({ ...prev, payment_method: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Methods</option>
              <option value="Cash">Cash</option>
              <option value="Check">Check</option>
              <option value="Credit Card">Credit Card</option>
              <option value="Electronic">Electronic</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date Range</label>
            <select
              value={filters.date_range}
              onChange={(e) => setFilters(prev => ({ ...prev, date_range: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Dates</option>
              <option value="today">Today</option>
              <option value="this_week">This Week</option>
              <option value="this_month">This Month</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              placeholder="Search payments..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div className="flex items-end">
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                onClick={selectAllPayments}
                className="px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm"
              >
                Select All
              </button>
              <button
                type="button"
                onClick={clearSelection}
                className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {/* Quick Select by Payment Method */}
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-gray-600 mr-2">Quick select:</span>
          {['Cash', 'Check', 'Credit Card', 'Electronic'].map(method => (
            <button
              key={method}
              type="button"
              onClick={() => selectByPaymentMethod(method)}
              className={`px-3 py-1 rounded-full text-xs ${getPaymentMethodColor(method)} hover:opacity-80`}
            >
              {getPaymentMethodIcon(method)} {method}
            </button>
          ))}
        </div>
      </div>

      {/* Undeposited Payments */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Undeposited Funds ({filteredPayments.length})
          </h3>
          {selectedPayments.length > 0 && (
            <p className="text-sm text-gray-600 mt-1">
              {selectedPayments.length} selected • Total: ${getTotalDepositAmount().toFixed(2)}
            </p>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left">
                  <input
                    type="checkbox"
                    onChange={(e) => {
                      if (e.target.checked) {
                        selectAllPayments();
                      } else {
                        clearSelection();
                      }
                    }}
                    checked={filteredPayments.length > 0 && selectedPayments.length === filteredPayments.length}
                    className="h-4 w-4 text-blue-600 rounded border-gray-300"
                  />
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Method</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Check/Ref #</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Memo</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredPayments.map((payment) => {
                const isSelected = selectedPayments.find(p => p.id === payment.id);
                
                return (
                  <tr 
                    key={payment.id} 
                    className={`hover:bg-gray-50 cursor-pointer ${isSelected ? 'bg-blue-50' : ''}`}
                    onClick={() => togglePaymentSelection(payment)}
                  >
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={!!isSelected}
                        onChange={() => togglePaymentSelection(payment)}
                        className="h-4 w-4 text-blue-600 rounded border-gray-300"
                      />
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {new Date(payment.date).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {payment.customer_name}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${getPaymentMethodColor(payment.payment_method)}`}>
                        <span className="mr-1">{getPaymentMethodIcon(payment.payment_method)}</span>
                        {payment.payment_method}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {payment.check_number || '-'}
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      ${payment.total.toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600 max-w-xs truncate">
                      {payment.memo || '-'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredPayments.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            {undepositedPayments.length === 0 
              ? "No undeposited payments found. All payments have been deposited."
              : "No payments match your current filters."
            }
          </div>
        )}
      </div>

      {/* Deposit Form */}
      {selectedPayments.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Deposit Details</h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Deposit Date *
                </label>
                <input
                  type="date"
                  value={formData.deposit_date}
                  onChange={(e) => setFormData(prev => ({ ...prev, deposit_date: e.target.value }))}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.deposit_date ? 'border-red-300' : 'border-gray-300'
                  }`}
                />
                {errors.deposit_date && <p className="text-red-500 text-sm mt-1">{errors.deposit_date}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Deposit To Account *
                </label>
                <select
                  value={formData.deposit_to_account_id}
                  onChange={(e) => setFormData(prev => ({ ...prev, deposit_to_account_id: e.target.value }))}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                    errors.deposit_to_account_id ? 'border-red-300' : 'border-gray-300'
                  }`}
                >
                  <option value="">Select Account</option>
                  {accounts.filter(acc => ['Asset'].includes(acc.account_type) && 
                    ['Checking', 'Savings'].includes(acc.detail_type)).map(account => (
                    <option key={account.id} value={account.id}>
                      {account.name} - ${account.balance?.toFixed(2) || '0.00'}
                    </option>
                  ))}
                </select>
                {errors.deposit_to_account_id && <p className="text-red-500 text-sm mt-1">{errors.deposit_to_account_id}</p>}
              </div>
            </div>

            {/* Deposit Summary */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 className="font-medium text-blue-900 mb-3">Deposit Summary</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-blue-700">Total Items:</span>
                  <div className="font-semibold">{selectedPayments.length}</div>
                </div>
                <div>
                  <span className="text-blue-700">Cash:</span>
                  <div className="font-semibold">
                    ${selectedPayments.filter(p => p.payment_method === 'Cash').reduce((sum, p) => sum + p.total, 0).toFixed(2)}
                  </div>
                </div>
                <div>
                  <span className="text-blue-700">Checks:</span>
                  <div className="font-semibold">
                    ${selectedPayments.filter(p => p.payment_method === 'Check').reduce((sum, p) => sum + p.total, 0).toFixed(2)}
                  </div>
                </div>
                <div>
                  <span className="text-blue-700">Total Deposit:</span>
                  <div className="font-bold text-lg">${getTotalDepositAmount().toFixed(2)}</div>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Memo
              </label>
              <textarea
                value={formData.memo}
                onChange={(e) => setFormData(prev => ({ ...prev, memo: e.target.value }))}
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Deposit notes..."
              />
            </div>

            {/* Error Display */}
            {(errors.payments || errors.submit) && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                {errors.payments && <p className="text-red-700 text-sm">{errors.payments}</p>}
                {errors.submit && <p className="text-red-700 text-sm">{errors.submit}</p>}
              </div>
            )}

            {/* Submit Buttons */}
            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={clearSelection}
                className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                disabled={loading}
              >
                Cancel
              </button>
              
              <button
                type="submit"
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  `Make Deposit - $${getTotalDepositAmount().toFixed(2)}`
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default MakeDeposits;
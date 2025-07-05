import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PayBills = ({ vendors, accounts, onRefresh }) => {
  const [selectedBills, setSelectedBills] = useState([]);
  const [allOpenBills, setAllOpenBills] = useState([]);
  const [formData, setFormData] = useState({
    payment_date: new Date().toISOString().split('T')[0],
    payment_account_id: '',
    payment_method: 'Check',
    memo: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [filters, setFilters] = useState({
    vendor_id: '',
    due_date_filter: 'all', // all, overdue, due_soon
    search: ''
  });

  useEffect(() => {
    fetchAllOpenBills();
  }, []);

  const fetchAllOpenBills = async () => {
    try {
      setLoading(true);
      const billPromises = vendors.map(vendor => 
        axios.get(`${API}/vendors/${vendor.id}/open-bills`)
          .then(response => response.data.map(bill => ({ ...bill, vendor_name: vendor.name })))
          .catch(() => [])
      );
      
      const allBillsArrays = await Promise.all(billPromises);
      const flattenedBills = allBillsArrays.flat();
      setAllOpenBills(flattenedBills);
    } catch (error) {
      console.error('Error fetching open bills:', error);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredBills = () => {
    let filtered = [...allOpenBills];
    
    // Vendor filter
    if (filters.vendor_id) {
      filtered = filtered.filter(bill => bill.vendor_id === filters.vendor_id);
    }
    
    // Search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(bill => 
        bill.vendor_name.toLowerCase().includes(searchLower) ||
        (bill.transaction_number || '').toLowerCase().includes(searchLower) ||
        (bill.reference_number || '').toLowerCase().includes(searchLower)
      );
    }
    
    // Due date filter
    const today = new Date();
    if (filters.due_date_filter === 'overdue') {
      filtered = filtered.filter(bill => {
        const dueDate = new Date(bill.due_date);
        return dueDate < today;
      });
    } else if (filters.due_date_filter === 'due_soon') {
      const nextWeek = new Date();
      nextWeek.setDate(today.getDate() + 7);
      filtered = filtered.filter(bill => {
        const dueDate = new Date(bill.due_date);
        return dueDate >= today && dueDate <= nextWeek;
      });
    }
    
    return filtered.sort((a, b) => {
      // Sort by due date, then by vendor name
      const dateA = new Date(a.due_date || a.date);
      const dateB = new Date(b.due_date || b.date);
      if (dateA !== dateB) return dateA - dateB;
      return a.vendor_name.localeCompare(b.vendor_name);
    });
  };

  const toggleBillSelection = (bill) => {
    const isSelected = selectedBills.find(b => b.id === bill.id);
    if (isSelected) {
      setSelectedBills(selectedBills.filter(b => b.id !== bill.id));
    } else {
      setSelectedBills([...selectedBills, { 
        ...bill, 
        payment_amount: bill.balance || bill.total 
      }]);
    }
  };

  const updateBillPaymentAmount = (billId, amount) => {
    setSelectedBills(selectedBills.map(bill => 
      bill.id === billId 
        ? { ...bill, payment_amount: parseFloat(amount) || 0 }
        : bill
    ));
  };

  const getTotalPaymentAmount = () => {
    return selectedBills.reduce((sum, bill) => sum + (bill.payment_amount || 0), 0);
  };

  const selectAllOverdue = () => {
    const today = new Date();
    const overdueBills = getFilteredBills().filter(bill => {
      const dueDate = new Date(bill.due_date);
      return dueDate < today && !selectedBills.find(sb => sb.id === bill.id);
    });
    
    const newSelectedBills = overdueBills.map(bill => ({
      ...bill,
      payment_amount: bill.balance || bill.total
    }));
    
    setSelectedBills([...selectedBills, ...newSelectedBills]);
  };

  const clearSelection = () => {
    setSelectedBills([]);
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (selectedBills.length === 0) {
      newErrors.bills = 'Please select at least one bill to pay';
    }
    
    if (!formData.payment_date) {
      newErrors.payment_date = 'Payment date is required';
    }
    
    if (!formData.payment_account_id) {
      newErrors.payment_account_id = 'Payment account is required';
    }

    // Check if payment amounts are valid
    const invalidPayments = selectedBills.filter(bill => {
      const amount = bill.payment_amount || 0;
      const balance = bill.balance || bill.total;
      return amount <= 0 || amount > balance;
    });

    if (invalidPayments.length > 0) {
      newErrors.amounts = 'Payment amounts must be greater than 0 and not exceed bill balance';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const billPayments = selectedBills.map(bill => ({
        bill_id: bill.id,
        amount: bill.payment_amount
      }));

      const submitData = {
        payment_date: new Date(formData.payment_date),
        payment_account_id: formData.payment_account_id,
        payment_method: formData.payment_method,
        bill_payments: billPayments,
        memo: formData.memo
      };

      await axios.post(`${API}/payments/pay-bills`, submitData);
      
      // Reset form
      setSelectedBills([]);
      setFormData({
        payment_date: new Date().toISOString().split('T')[0],
        payment_account_id: '',
        payment_method: 'Check',
        memo: ''
      });
      
      // Refresh data
      fetchAllOpenBills();
      if (onRefresh) onRefresh();
      
    } catch (error) {
      console.error('Error processing bill payments:', error);
      setErrors({ submit: 'Failed to process bill payments. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const getDueDateStatus = (dueDate) => {
    const today = new Date();
    const due = new Date(dueDate);
    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return { status: 'overdue', text: `${Math.abs(diffDays)} days overdue`, class: 'text-red-600' };
    if (diffDays === 0) return { status: 'due', text: 'Due today', class: 'text-orange-600' };
    if (diffDays <= 7) return { status: 'due_soon', text: `Due in ${diffDays} days`, class: 'text-yellow-600' };
    return { status: 'future', text: `Due in ${diffDays} days`, class: 'text-gray-600' };
  };

  const filteredBills = getFilteredBills();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-red-600 to-pink-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">Pay Bills</h2>
        <p className="text-red-100">Select and pay vendor bills</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Vendor</label>
            <select
              value={filters.vendor_id}
              onChange={(e) => setFilters(prev => ({ ...prev, vendor_id: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
            >
              <option value="">All Vendors</option>
              {vendors.map(vendor => (
                <option key={vendor.id} value={vendor.id}>{vendor.name}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <select
              value={filters.due_date_filter}
              onChange={(e) => setFilters(prev => ({ ...prev, due_date_filter: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
            >
              <option value="all">All Bills</option>
              <option value="overdue">Overdue</option>
              <option value="due_soon">Due Within 7 Days</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              placeholder="Search bills..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500"
            />
          </div>
          
          <div className="flex items-end space-x-2">
            <button
              type="button"
              onClick={selectAllOverdue}
              className="px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm"
            >
              Select Overdue
            </button>
            <button
              type="button"
              onClick={clearSelection}
              className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
            >
              Clear All
            </button>
          </div>
        </div>
      </div>

      {/* Bills List */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            Open Bills ({filteredBills.length})
          </h3>
          {selectedBills.length > 0 && (
            <p className="text-sm text-gray-600 mt-1">
              {selectedBills.length} selected • Total: ${getTotalPaymentAmount().toFixed(2)}
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
                        const unselectedBills = filteredBills.filter(bill => 
                          !selectedBills.find(sb => sb.id === bill.id)
                        );
                        const newSelections = unselectedBills.map(bill => ({
                          ...bill,
                          payment_amount: bill.balance || bill.total
                        }));
                        setSelectedBills([...selectedBills, ...newSelections]);
                      } else {
                        clearSelection();
                      }
                    }}
                    className="h-4 w-4 text-red-600 rounded border-gray-300"
                  />
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vendor</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bill #</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount Due</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Payment Amount</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredBills.map((bill) => {
                const isSelected = selectedBills.find(b => b.id === bill.id);
                const dueDateInfo = getDueDateStatus(bill.due_date);
                const balance = bill.balance || bill.total;
                
                return (
                  <tr 
                    key={bill.id} 
                    className={`hover:bg-gray-50 ${isSelected ? 'bg-red-50' : ''}`}
                  >
                    <td className="px-4 py-3">
                      <input
                        type="checkbox"
                        checked={!!isSelected}
                        onChange={() => toggleBillSelection(bill)}
                        className="h-4 w-4 text-red-600 rounded border-gray-300"
                      />
                    </td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {bill.vendor_name}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {bill.transaction_number || bill.reference_number || `BILL-${bill.id.slice(-8)}`}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(bill.date).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 text-sm">
                      <div>
                        <div className="text-gray-900">
                          {bill.due_date ? new Date(bill.due_date).toLocaleDateString() : '-'}
                        </div>
                        {bill.due_date && (
                          <div className={`text-xs ${dueDateInfo.class}`}>
                            {dueDateInfo.text}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 font-medium">
                      ${balance.toFixed(2)}
                    </td>
                    <td className="px-4 py-3">
                      {isSelected ? (
                        <input
                          type="number"
                          step="0.01"
                          min="0"
                          max={balance}
                          value={isSelected.payment_amount || ''}
                          onChange={(e) => updateBillPaymentAmount(bill.id, e.target.value)}
                          className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                          placeholder="0.00"
                        />
                      ) : (
                        <span className="text-gray-400 text-sm">-</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {filteredBills.length === 0 && (
          <div className="p-8 text-center text-gray-500">
            No open bills found matching your criteria.
          </div>
        )}
      </div>

      {/* Payment Form */}
      {selectedBills.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Payment Details</h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Date *
                </label>
                <input
                  type="date"
                  value={formData.payment_date}
                  onChange={(e) => setFormData(prev => ({ ...prev, payment_date: e.target.value }))}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent ${
                    errors.payment_date ? 'border-red-300' : 'border-gray-300'
                  }`}
                />
                {errors.payment_date && <p className="text-red-500 text-sm mt-1">{errors.payment_date}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Account *
                </label>
                <select
                  value={formData.payment_account_id}
                  onChange={(e) => setFormData(prev => ({ ...prev, payment_account_id: e.target.value }))}
                  className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent ${
                    errors.payment_account_id ? 'border-red-300' : 'border-gray-300'
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
                {errors.payment_account_id && <p className="text-red-500 text-sm mt-1">{errors.payment_account_id}</p>}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Method
                </label>
                <select
                  value={formData.payment_method}
                  onChange={(e) => setFormData(prev => ({ ...prev, payment_method: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                >
                  <option value="Check">Check</option>
                  <option value="Electronic">Electronic</option>
                  <option value="Credit Card">Credit Card</option>
                  <option value="Cash">Cash</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Total Payment Amount
                </label>
                <div className="w-full px-4 py-3 border border-gray-300 rounded-lg bg-gray-50 text-lg font-semibold">
                  ${getTotalPaymentAmount().toFixed(2)}
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
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                placeholder="Payment notes..."
              />
            </div>

            {/* Error Display */}
            {(errors.bills || errors.amounts || errors.submit) && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                {errors.bills && <p className="text-red-700 text-sm">{errors.bills}</p>}
                {errors.amounts && <p className="text-red-700 text-sm">{errors.amounts}</p>}
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
                className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
                disabled={loading}
              >
                {loading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </div>
                ) : (
                  `Pay ${selectedBills.length} Bill${selectedBills.length !== 1 ? 's' : ''}`
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default PayBills;
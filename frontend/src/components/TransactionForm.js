import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const TransactionForm = ({ 
  transactionType, 
  initialData = null, 
  customers = [], 
  vendors = [], 
  items = [], 
  accounts = [],
  classes = [],
  locations = [],
  terms = [],
  onSave,
  onCancel
}) => {
  const [formData, setFormData] = useState({
    transaction_type: transactionType,
    customer_id: '',
    vendor_id: '',
    reference_number: '',
    date: new Date().toISOString().split('T')[0],
    due_date: '',
    terms: '',
    memo: '',
    subtotal: 0,
    tax_rate: 0,
    tax_amount: 0,
    total: 0,
    line_items: [{
      item_id: '',
      description: '',
      quantity: 1,
      rate: 0,
      amount: 0,
      account_id: '',
      class_id: '',
      location_id: ''
    }],
    // Additional fields for specific transaction types
    payment_method: '',
    deposit_to: '',
    ship_to_address: '',
    billing_address: '',
    status: 'Active'
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({ ...initialData });
    }
  }, [initialData]);

  const updateFormData = (field, value) => {
    setFormData(prev => {
      const updated = { ...prev, [field]: value };
      
      // Auto-calculate totals
      if (field.includes('line_items') || field === 'tax_rate') {
        const subtotal = updated.line_items.reduce((sum, item) => sum + (item.amount || 0), 0);
        const taxAmount = subtotal * (updated.tax_rate / 100);
        updated.subtotal = subtotal;
        updated.tax_amount = taxAmount;
        updated.total = subtotal + taxAmount;
      }
      
      return updated;
    });
  };

  const updateLineItem = (index, field, value) => {
    const newLineItems = [...formData.line_items];
    newLineItems[index] = { ...newLineItems[index], [field]: value };
    
    // Auto-calculate amount
    if (field === 'quantity' || field === 'rate') {
      const quantity = field === 'quantity' ? parseFloat(value) || 0 : newLineItems[index].quantity;
      const rate = field === 'rate' ? parseFloat(value) || 0 : newLineItems[index].rate;
      newLineItems[index].amount = quantity * rate;
    }
    
    updateFormData('line_items', newLineItems);
  };

  const addLineItem = () => {
    const newLineItem = {
      item_id: '',
      description: '',
      quantity: 1,
      rate: 0,
      amount: 0,
      account_id: '',
      class_id: '',
      location_id: ''
    };
    updateFormData('line_items', [...formData.line_items, newLineItem]);
  };

  const removeLineItem = (index) => {
    if (formData.line_items.length > 1) {
      const newLineItems = formData.line_items.filter((_, i) => i !== index);
      updateFormData('line_items', newLineItems);
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Basic validation
    if (!formData.date) newErrors.date = 'Date is required';
    
    if (['Invoice', 'Sales Receipt', 'Estimate', 'Sales Order'].includes(transactionType) && !formData.customer_id) {
      newErrors.customer_id = 'Customer is required';
    }
    
    if (['Bill', 'Purchase Order'].includes(transactionType) && !formData.vendor_id) {
      newErrors.vendor_id = 'Vendor is required';
    }

    // Line items validation
    formData.line_items.forEach((item, index) => {
      if (!item.description) {
        newErrors[`line_item_${index}_description`] = 'Description is required';
      }
      if (!item.account_id && ['Bill', 'Check'].includes(transactionType)) {
        newErrors[`line_item_${index}_account`] = 'Account is required';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/transactions`, formData);
      if (onSave) onSave();
    } catch (error) {
      console.error('Error saving transaction:', error);
      setErrors({ submit: 'Failed to save transaction. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const getEntityOptions = () => {
    if (['Invoice', 'Sales Receipt', 'Estimate', 'Sales Order', 'Credit Memo'].includes(transactionType)) {
      return customers;
    } else if (['Bill', 'Purchase Order'].includes(transactionType)) {
      return vendors;
    }
    return [];
  };

  const getEntityLabel = () => {
    if (['Invoice', 'Sales Receipt', 'Estimate', 'Sales Order', 'Credit Memo'].includes(transactionType)) {
      return 'Customer';
    } else if (['Bill', 'Purchase Order'].includes(transactionType)) {
      return 'Vendor';
    }
    return 'Entity';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Transaction Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">{transactionType}</h2>
            <p className="text-blue-100">Create new {transactionType.toLowerCase()}</p>
          </div>
          <div className="text-right">
            <div className="text-sm text-blue-100">#{formData.reference_number || 'AUTO'}</div>
            <div className="text-lg font-semibold">${formData.total.toFixed(2)}</div>
          </div>
        </div>
      </div>

      {/* Form Toolbar */}
      <div className="bg-gray-50 border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            <button className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors">
              📄 Previous
            </button>
            <button className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors">
              📄 Next
            </button>
            <button className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors">
              📋 Copy
            </button>
            <button className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors">
              🖨️ Print
            </button>
            <button className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors">
              📧 Email
            </button>
          </div>
          <div className="flex space-x-2">
            <button className="px-3 py-1 text-sm bg-purple-100 text-purple-700 rounded hover:bg-purple-200 transition-colors">
              💾 Memorize
            </button>
            <button className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors">
              📎 Attach
            </button>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-6">
        {/* Transaction Header Fields */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Left Column */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {getEntityLabel()} *
              </label>
              <select
                value={['Invoice', 'Sales Receipt', 'Estimate', 'Sales Order', 'Credit Memo'].includes(transactionType) ? formData.customer_id : formData.vendor_id}
                onChange={(e) => updateFormData(['Invoice', 'Sales Receipt', 'Estimate', 'Sales Order', 'Credit Memo'].includes(transactionType) ? 'customer_id' : 'vendor_id', e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.customer_id || errors.vendor_id ? 'border-red-300' : 'border-gray-300'
                }`}
              >
                <option value="">Select {getEntityLabel()}</option>
                {getEntityOptions().map(entity => (
                  <option key={entity.id} value={entity.id}>{entity.name}</option>
                ))}
              </select>
              {(errors.customer_id || errors.vendor_id) && (
                <p className="text-red-500 text-sm mt-1">{errors.customer_id || errors.vendor_id}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date *
              </label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => updateFormData('date', e.target.value)}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.date ? 'border-red-300' : 'border-gray-300'
                }`}
              />
              {errors.date && (
                <p className="text-red-500 text-sm mt-1">{errors.date}</p>
              )}
            </div>

            {transactionType === 'Sales Receipt' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Method
                </label>
                <select
                  value={formData.payment_method}
                  onChange={(e) => updateFormData('payment_method', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select Payment Method</option>
                  <option value="Cash">Cash</option>
                  <option value="Check">Check</option>
                  <option value="Credit Card">Credit Card</option>
                  <option value="Electronic">Electronic</option>
                </select>
              </div>
            )}
          </div>

          {/* Right Column */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {transactionType === 'Invoice' ? 'Invoice #' : 
                 transactionType === 'Bill' ? 'Ref #' :
                 transactionType === 'Estimate' ? 'Estimate #' :
                 transactionType === 'Purchase Order' ? 'PO #' : 'Reference #'}
              </label>
              <input
                type="text"
                value={formData.reference_number}
                onChange={(e) => updateFormData('reference_number', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Auto-generated"
              />
            </div>

            {['Invoice', 'Bill'].includes(transactionType) && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Terms
                  </label>
                  <select
                    value={formData.terms}
                    onChange={(e) => updateFormData('terms', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Terms</option>
                    {terms.map(term => (
                      <option key={term.id} value={term.name}>{term.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Due Date
                  </label>
                  <input
                    type="date"
                    value={formData.due_date}
                    onChange={(e) => updateFormData('due_date', e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </>
            )}

            {transactionType === 'Sales Receipt' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Deposit To
                </label>
                <select
                  value={formData.deposit_to}
                  onChange={(e) => updateFormData('deposit_to', e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select Account</option>
                  {accounts.filter(acc => acc.account_type === 'Asset').map(account => (
                    <option key={account.id} value={account.id}>{account.name}</option>
                  ))}
                </select>
              </div>
            )}
          </div>
        </div>

        {/* Line Items Section */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Line Items</h3>
            <button
              type="button"
              onClick={addLineItem}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              + Add Line
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Item</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Qty</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rate</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Account</th>
                    <th className="px-4 py-3"></th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {formData.line_items.map((item, index) => (
                    <tr key={index}>
                      <td className="px-4 py-3">
                        <select
                          value={item.item_id}
                          onChange={(e) => updateLineItem(index, 'item_id', e.target.value)}
                          className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                        >
                          <option value="">Select Item</option>
                          {items.map(item => (
                            <option key={item.id} value={item.id}>{item.name}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-4 py-3">
                        <input
                          type="text"
                          value={item.description}
                          onChange={(e) => updateLineItem(index, 'description', e.target.value)}
                          className={`w-full px-2 py-1 border rounded text-sm ${
                            errors[`line_item_${index}_description`] ? 'border-red-300' : 'border-gray-300'
                          }`}
                          placeholder="Description"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="0.01"
                          value={item.quantity}
                          onChange={(e) => updateLineItem(index, 'quantity', e.target.value)}
                          className="w-20 px-2 py-1 border border-gray-300 rounded text-sm"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="0.01"
                          value={item.rate}
                          onChange={(e) => updateLineItem(index, 'rate', e.target.value)}
                          className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                        />
                      </td>
                      <td className="px-4 py-3">
                        <div className="w-24 px-2 py-1 bg-gray-50 border border-gray-300 rounded text-sm">
                          ${item.amount.toFixed(2)}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <select
                          value={item.account_id}
                          onChange={(e) => updateLineItem(index, 'account_id', e.target.value)}
                          className={`w-full px-2 py-1 border rounded text-sm ${
                            errors[`line_item_${index}_account`] ? 'border-red-300' : 'border-gray-300'
                          }`}
                        >
                          <option value="">Select Account</option>
                          {accounts.map(account => (
                            <option key={account.id} value={account.id}>{account.name}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-4 py-3">
                        {formData.line_items.length > 1 && (
                          <button
                            type="button"
                            onClick={() => removeLineItem(index)}
                            className="text-red-600 hover:text-red-800 text-sm"
                          >
                            Remove
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Totals Section */}
        <div className="flex justify-end mb-8">
          <div className="w-80 space-y-3">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Subtotal:</span>
              <span className="text-sm font-medium">${formData.subtotal.toFixed(2)}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Tax Rate:</span>
              <div className="flex items-center space-x-2">
                <input
                  type="number"
                  step="0.01"
                  value={formData.tax_rate}
                  onChange={(e) => updateFormData('tax_rate', parseFloat(e.target.value) || 0)}
                  className="w-16 px-2 py-1 border border-gray-300 rounded text-sm text-right"
                />
                <span className="text-sm text-gray-600">%</span>
              </div>
            </div>
            
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Tax Amount:</span>
              <span className="text-sm font-medium">${formData.tax_amount.toFixed(2)}</span>
            </div>
            
            <div className="flex justify-between border-t pt-3">
              <span className="text-lg font-semibold">Total:</span>
              <span className="text-lg font-bold text-blue-600">${formData.total.toFixed(2)}</span>
            </div>
          </div>
        </div>

        {/* Memo Section */}
        <div className="mb-8">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Memo
          </label>
          <textarea
            value={formData.memo}
            onChange={(e) => updateFormData('memo', e.target.value)}
            rows={3}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter memo or notes..."
          />
        </div>

        {/* Error Display */}
        {errors.submit && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            {errors.submit}
          </div>
        )}

        {/* Form Actions */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={onCancel}
            className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            disabled={loading}
          >
            Cancel
          </button>
          
          <button
            type="button"
            className="px-6 py-3 text-blue-700 bg-blue-100 border border-blue-300 rounded-lg hover:bg-blue-200 transition-colors"
            disabled={loading}
          >
            Save & New
          </button>
          
          <button
            type="submit"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            disabled={loading}
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Saving...
              </div>
            ) : (
              'Save & Close'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TransactionForm;
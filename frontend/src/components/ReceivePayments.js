import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ReceivePayments = ({ customers, accounts, onRefresh }) => {
  const [formData, setFormData] = useState({
    customer_id: '',
    payment_amount: '',
    payment_method: 'Check',
    payment_date: new Date().toISOString().split('T')[0],
    deposit_to_account_id: '',
    memo: '',
    invoice_applications: []
  });

  const [openInvoices, setOpenInvoices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  // Get undeposited funds account by default
  const defaultDepositAccount = accounts.find(acc => 
    acc.detail_type === 'Undeposited Funds' || acc.name.toLowerCase().includes('undeposited')
  );

  useEffect(() => {
    if (defaultDepositAccount && !formData.deposit_to_account_id) {
      setFormData(prev => ({ ...prev, deposit_to_account_id: defaultDepositAccount.id }));
    }
  }, [defaultDepositAccount, formData.deposit_to_account_id]);

  useEffect(() => {
    if (formData.customer_id) {
      fetchOpenInvoices(formData.customer_id);
    } else {
      setOpenInvoices([]);
      setFormData(prev => ({ ...prev, invoice_applications: [] }));
    }
  }, [formData.customer_id]);

  const fetchOpenInvoices = async (customerId) => {
    try {
      const response = await axios.get(`${API}/customers/${customerId}/open-invoices`);
      const invoices = response.data.map(invoice => ({
        ...invoice,
        applied_amount: 0
      }));
      setOpenInvoices(invoices);
      setFormData(prev => ({ 
        ...prev, 
        invoice_applications: invoices.map(inv => ({
          invoice_id: inv.id,
          amount: 0,
          balance: inv.balance || inv.total
        }))
      }));
    } catch (error) {
      console.error('Error fetching open invoices:', error);
    }
  };

  const updateInvoiceApplication = (invoiceId, appliedAmount) => {
    const newApplications = formData.invoice_applications.map(app => 
      app.invoice_id === invoiceId 
        ? { ...app, amount: parseFloat(appliedAmount) || 0 }
        : app
    );
    setFormData(prev => ({ ...prev, invoice_applications: newApplications }));
  };

  const autoApplyPayment = () => {
    let remainingPayment = parseFloat(formData.payment_amount) || 0;
    const newApplications = [...formData.invoice_applications];

    // Sort invoices by date (oldest first)
    const sortedInvoices = [...openInvoices].sort((a, b) => new Date(a.date) - new Date(b.date));

    for (let invoice of sortedInvoices) {
      if (remainingPayment <= 0) break;
      
      const invoiceBalance = invoice.balance || invoice.total;
      const applicationIndex = newApplications.findIndex(app => app.invoice_id === invoice.id);
      
      if (applicationIndex !== -1) {
        const amountToApply = Math.min(remainingPayment, invoiceBalance);
        newApplications[applicationIndex].amount = amountToApply;
        remainingPayment -= amountToApply;
      }
    }

    setFormData(prev => ({ ...prev, invoice_applications: newApplications }));
  };

  const getTotalApplied = () => {
    return formData.invoice_applications.reduce((sum, app) => sum + (app.amount || 0), 0);
  };

  const getUnappliedAmount = () => {
    return (parseFloat(formData.payment_amount) || 0) - getTotalApplied();
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.customer_id) newErrors.customer_id = 'Customer is required';
    if (!formData.payment_amount || parseFloat(formData.payment_amount) <= 0) {
      newErrors.payment_amount = 'Payment amount must be greater than 0';
    }
    if (!formData.payment_date) newErrors.payment_date = 'Payment date is required';
    if (!formData.deposit_to_account_id) newErrors.deposit_to_account_id = 'Deposit account is required';

    const totalApplied = getTotalApplied();
    const paymentAmount = parseFloat(formData.payment_amount) || 0;
    if (totalApplied > paymentAmount) {
      newErrors.applications = 'Total applied amount cannot exceed payment amount';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      const submitData = {
        customer_id: formData.customer_id,
        payment_amount: parseFloat(formData.payment_amount),
        payment_method: formData.payment_method,
        payment_date: new Date(formData.payment_date),
        deposit_to_account_id: formData.deposit_to_account_id,
        invoice_applications: formData.invoice_applications.filter(app => app.amount > 0),
        memo: formData.memo
      };

      await axios.post(`${API}/payments/receive`, submitData);
      
      // Reset form
      setFormData({
        customer_id: '',
        payment_amount: '',
        payment_method: 'Check',
        payment_date: new Date().toISOString().split('T')[0],
        deposit_to_account_id: defaultDepositAccount?.id || '',
        memo: '',
        invoice_applications: []
      });
      setOpenInvoices([]);
      
      if (onRefresh) onRefresh();
      
    } catch (error) {
      console.error('Error processing payment:', error);
      setErrors({ submit: 'Failed to process payment. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const selectedCustomer = customers.find(c => c.id === formData.customer_id);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">Receive Payments</h2>
        <p className="text-green-100">Record customer payments and apply to invoices</p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Payment Header */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Customer *
              </label>
              <select
                value={formData.customer_id}
                onChange={(e) => setFormData(prev => ({ ...prev, customer_id: e.target.value }))}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent ${
                  errors.customer_id ? 'border-red-300' : 'border-gray-300'
                }`}
              >
                <option value="">Select Customer</option>
                {customers.map(customer => (
                  <option key={customer.id} value={customer.id}>{customer.name}</option>
                ))}
              </select>
              {errors.customer_id && <p className="text-red-500 text-sm mt-1">{errors.customer_id}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Amount *
              </label>
              <input
                type="number"
                step="0.01"
                value={formData.payment_amount}
                onChange={(e) => setFormData(prev => ({ ...prev, payment_amount: e.target.value }))}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent ${
                  errors.payment_amount ? 'border-red-300' : 'border-gray-300'
                }`}
                placeholder="0.00"
              />
              {errors.payment_amount && <p className="text-red-500 text-sm mt-1">{errors.payment_amount}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Method
              </label>
              <select
                value={formData.payment_method}
                onChange={(e) => setFormData(prev => ({ ...prev, payment_method: e.target.value }))}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="Cash">Cash</option>
                <option value="Check">Check</option>
                <option value="Credit Card">Credit Card</option>
                <option value="Electronic">Electronic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Payment Date *
              </label>
              <input
                type="date"
                value={formData.payment_date}
                onChange={(e) => setFormData(prev => ({ ...prev, payment_date: e.target.value }))}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent ${
                  errors.payment_date ? 'border-red-300' : 'border-gray-300'
                }`}
              />
              {errors.payment_date && <p className="text-red-500 text-sm mt-1">{errors.payment_date}</p>}
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Deposit To *
              </label>
              <select
                value={formData.deposit_to_account_id}
                onChange={(e) => setFormData(prev => ({ ...prev, deposit_to_account_id: e.target.value }))}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent ${
                  errors.deposit_to_account_id ? 'border-red-300' : 'border-gray-300'
                }`}
              >
                <option value="">Select Account</option>
                {accounts.filter(acc => ['Asset'].includes(acc.account_type)).map(account => (
                  <option key={account.id} value={account.id}>
                    {account.name} ({account.detail_type})
                  </option>
                ))}
              </select>
              {errors.deposit_to_account_id && <p className="text-red-500 text-sm mt-1">{errors.deposit_to_account_id}</p>}
            </div>
          </div>

          {/* Customer Info Display */}
          {selectedCustomer && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-medium text-blue-900 mb-2">Customer Information</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-blue-700">Name:</span> {selectedCustomer.name}
                </div>
                <div>
                  <span className="text-blue-700">Balance:</span> ${selectedCustomer.balance?.toFixed(2) || '0.00'}
                </div>
                {selectedCustomer.email && (
                  <div>
                    <span className="text-blue-700">Email:</span> {selectedCustomer.email}
                  </div>
                )}
                {selectedCustomer.phone && (
                  <div>
                    <span className="text-blue-700">Phone:</span> {selectedCustomer.phone}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Open Invoices */}
          {openInvoices.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Apply to Invoices</h3>
                <button
                  type="button"
                  onClick={autoApplyPayment}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  disabled={!formData.payment_amount}
                >
                  Auto Apply
                </button>
              </div>

              <div className="border border-gray-200 rounded-lg overflow-hidden">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Original Amount</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Balance Due</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Payment</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {openInvoices.map((invoice) => {
                      const application = formData.invoice_applications.find(app => app.invoice_id === invoice.id);
                      const balance = invoice.balance || invoice.total;
                      return (
                        <tr key={invoice.id}>
                          <td className="px-4 py-3 text-sm font-medium text-gray-900">
                            {invoice.transaction_number || invoice.reference_number || `INV-${invoice.id.slice(-8)}`}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            {new Date(invoice.date).toLocaleDateString()}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            ${invoice.total.toFixed(2)}
                          </td>
                          <td className="px-4 py-3 text-sm text-gray-600">
                            ${balance.toFixed(2)}
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              step="0.01"
                              min="0"
                              max={balance}
                              value={application?.amount || ''}
                              onChange={(e) => updateInvoiceApplication(invoice.id, e.target.value)}
                              className="w-24 px-2 py-1 border border-gray-300 rounded text-sm"
                              placeholder="0.00"
                            />
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {/* Payment Summary */}
              <div className="mt-4 bg-gray-50 p-4 rounded-lg">
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Payment Amount:</span>
                    <div className="font-semibold">${(parseFloat(formData.payment_amount) || 0).toFixed(2)}</div>
                  </div>
                  <div>
                    <span className="text-gray-600">Total Applied:</span>
                    <div className="font-semibold">${getTotalApplied().toFixed(2)}</div>
                  </div>
                  <div>
                    <span className="text-gray-600">Unapplied Amount:</span>
                    <div className={`font-semibold ${getUnappliedAmount() < 0 ? 'text-red-600' : 'text-gray-900'}`}>
                      ${getUnappliedAmount().toFixed(2)}
                    </div>
                  </div>
                </div>
                {errors.applications && <p className="text-red-500 text-sm mt-2">{errors.applications}</p>}
              </div>
            </div>
          )}

          {/* Memo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Memo
            </label>
            <textarea
              value={formData.memo}
              onChange={(e) => setFormData(prev => ({ ...prev, memo: e.target.value }))}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="Payment notes..."
            />
          </div>

          {/* Error Display */}
          {errors.submit && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              {errors.submit}
            </div>
          )}

          {/* Submit Buttons */}
          <div className="flex justify-end space-x-4">
            <button
              type="button"
              className="px-6 py-3 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              disabled={loading}
            >
              Cancel
            </button>
            
            <button
              type="submit"
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
              disabled={loading}
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Processing...
                </div>
              ) : (
                'Save Payment'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReceivePayments;
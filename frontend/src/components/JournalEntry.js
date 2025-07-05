import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const JournalEntry = ({ accounts, onRefresh, onCancel }) => {
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split('T')[0],
    reference_number: '',
    memo: '',
    entries: [
      { account_id: '', description: '', debit: '', credit: '' },
      { account_id: '', description: '', debit: '', credit: '' }
    ]
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const addEntry = () => {
    setFormData(prev => ({
      ...prev,
      entries: [...prev.entries, { account_id: '', description: '', debit: '', credit: '' }]
    }));
  };

  const removeEntry = (index) => {
    if (formData.entries.length > 2) {
      setFormData(prev => ({
        ...prev,
        entries: prev.entries.filter((_, i) => i !== index)
      }));
    }
  };

  const updateEntry = (index, field, value) => {
    const newEntries = [...formData.entries];
    newEntries[index] = { ...newEntries[index], [field]: value };
    
    // Clear opposite field when one is entered
    if (field === 'debit' && value) {
      newEntries[index].credit = '';
    } else if (field === 'credit' && value) {
      newEntries[index].debit = '';
    }
    
    setFormData(prev => ({ ...prev, entries: newEntries }));
  };

  const getTotalDebits = () => {
    return formData.entries.reduce((sum, entry) => {
      return sum + (parseFloat(entry.debit) || 0);
    }, 0);
  };

  const getTotalCredits = () => {
    return formData.entries.reduce((sum, entry) => {
      return sum + (parseFloat(entry.credit) || 0);
    }, 0);
  };

  const getOutOfBalance = () => {
    return getTotalDebits() - getTotalCredits();
  };

  const isBalanced = () => {
    return Math.abs(getOutOfBalance()) < 0.01;
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.date) {
      newErrors.date = 'Date is required';
    }
    
    // Check if at least two entries have accounts and amounts
    const validEntries = formData.entries.filter(entry => 
      entry.account_id && entry.description && (entry.debit || entry.credit)
    );
    
    if (validEntries.length < 2) {
      newErrors.entries = 'At least two entries with account, description, and amount are required';
    }
    
    // Check for duplicate accounts
    const accountIds = validEntries.map(entry => entry.account_id);
    const duplicateAccounts = accountIds.filter((id, index) => accountIds.indexOf(id) !== index);
    if (duplicateAccounts.length > 0) {
      newErrors.duplicates = 'Duplicate accounts are not allowed in the same journal entry';
    }
    
    // Check if balanced
    if (!isBalanced()) {
      newErrors.balance = 'Journal entry must be balanced (total debits must equal total credits)';
    }
    
    // Validate individual entries
    formData.entries.forEach((entry, index) => {
      if (entry.account_id || entry.description || entry.debit || entry.credit) {
        if (!entry.account_id) {
          newErrors[`entry_${index}_account`] = 'Account is required';
        }
        if (!entry.description) {
          newErrors[`entry_${index}_description`] = 'Description is required';
        }
        if (!entry.debit && !entry.credit) {
          newErrors[`entry_${index}_amount`] = 'Either debit or credit amount is required';
        }
        if (entry.debit && entry.credit) {
          newErrors[`entry_${index}_both`] = 'Cannot have both debit and credit amounts';
        }
        if ((entry.debit && parseFloat(entry.debit) <= 0) || (entry.credit && parseFloat(entry.credit) <= 0)) {
          newErrors[`entry_${index}_negative`] = 'Amount must be greater than 0';
        }
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    try {
      // Filter out empty entries
      const validEntries = formData.entries.filter(entry => 
        entry.account_id && entry.description && (entry.debit || entry.credit)
      );

      // Create journal entries directly
      const journalEntries = validEntries.map(entry => ({
        account_id: entry.account_id,
        debit: parseFloat(entry.debit) || 0,
        credit: parseFloat(entry.credit) || 0,
        description: entry.description,
        date: new Date(formData.date)
      }));

      // Create a transaction record for the journal entry
      const transactionData = {
        transaction_type: 'Journal',
        date: new Date(formData.date),
        reference_number: formData.reference_number,
        memo: formData.memo,
        line_items: validEntries.map(entry => ({
          description: entry.description,
          account_id: entry.account_id,
          amount: parseFloat(entry.debit) || parseFloat(entry.credit) || 0
        })),
        total: getTotalDebits()
      };

      // Create the transaction first
      const transactionResponse = await axios.post(`${API}/transactions`, transactionData);
      const transactionId = transactionResponse.data.id;

      // Then create individual journal entries
      for (const entry of journalEntries) {
        await axios.post(`${API}/journal-entries`, {
          ...entry,
          transaction_id: transactionId
        });
      }
      
      // Reset form
      setFormData({
        date: new Date().toISOString().split('T')[0],
        reference_number: '',
        memo: '',
        entries: [
          { account_id: '', description: '', debit: '', credit: '' },
          { account_id: '', description: '', debit: '', credit: '' }
        ]
      });
      
      if (onRefresh) onRefresh();
      
    } catch (error) {
      console.error('Error creating journal entry:', error);
      setErrors({ submit: 'Failed to create journal entry. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const getAccountById = (accountId) => {
    return accounts.find(acc => acc.id === accountId);
  };

  const getAccountTypeColor = (account) => {
    if (!account) return 'text-gray-600';
    switch (account.account_type) {
      case 'Asset': return 'text-blue-600';
      case 'Liability': return 'text-red-600';
      case 'Equity': return 'text-purple-600';
      case 'Income': return 'text-green-600';
      case 'Expense': return 'text-orange-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">Journal Entry</h2>
        <p className="text-purple-100">Create manual accounting adjustments with proper double-entry bookkeeping</p>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Header Information */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Date *
              </label>
              <input
                type="date"
                value={formData.date}
                onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.date ? 'border-red-300' : 'border-gray-300'
                }`}
              />
              {errors.date && <p className="text-red-500 text-sm mt-1">{errors.date}</p>}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Reference Number
              </label>
              <input
                type="text"
                value={formData.reference_number}
                onChange={(e) => setFormData(prev => ({ ...prev, reference_number: e.target.value }))}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="JE-001"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Balance Status
              </label>
              <div className={`w-full px-4 py-3 border rounded-lg font-semibold ${
                isBalanced() 
                  ? 'border-green-300 bg-green-50 text-green-800' 
                  : 'border-red-300 bg-red-50 text-red-800'
              }`}>
                {isBalanced() ? '✓ Balanced' : '⚠ Out of Balance'}
              </div>
            </div>
          </div>

          {/* Journal Entries */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Journal Entries</h3>
              <button
                type="button"
                onClick={addEntry}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                + Add Line
              </button>
            </div>

            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-1/4">Account</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-1/3">Description</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-1/6">Debit</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase w-1/6">Credit</th>
                      <th className="px-4 py-3 w-12"></th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {formData.entries.map((entry, index) => {
                      const selectedAccount = getAccountById(entry.account_id);
                      return (
                        <tr key={index}>
                          <td className="px-4 py-3">
                            <select
                              value={entry.account_id}
                              onChange={(e) => updateEntry(index, 'account_id', e.target.value)}
                              className={`w-full px-2 py-2 border rounded text-sm ${
                                errors[`entry_${index}_account`] ? 'border-red-300' : 'border-gray-300'
                              }`}
                            >
                              <option value="">Select Account</option>
                              {accounts.map(account => (
                                <option key={account.id} value={account.id}>
                                  {account.account_number ? `${account.account_number} - ` : ''}{account.name}
                                </option>
                              ))}
                            </select>
                            {selectedAccount && (
                              <div className={`text-xs mt-1 ${getAccountTypeColor(selectedAccount)}`}>
                                {selectedAccount.account_type} • {selectedAccount.detail_type}
                              </div>
                            )}
                            {errors[`entry_${index}_account`] && (
                              <p className="text-red-500 text-xs mt-1">{errors[`entry_${index}_account`]}</p>
                            )}
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="text"
                              value={entry.description}
                              onChange={(e) => updateEntry(index, 'description', e.target.value)}
                              className={`w-full px-2 py-2 border rounded text-sm ${
                                errors[`entry_${index}_description`] ? 'border-red-300' : 'border-gray-300'
                              }`}
                              placeholder="Description"
                            />
                            {errors[`entry_${index}_description`] && (
                              <p className="text-red-500 text-xs mt-1">{errors[`entry_${index}_description`]}</p>
                            )}
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              step="0.01"
                              min="0"
                              value={entry.debit}
                              onChange={(e) => updateEntry(index, 'debit', e.target.value)}
                              className={`w-full px-2 py-2 border rounded text-sm text-right ${
                                errors[`entry_${index}_amount`] || errors[`entry_${index}_both`] || errors[`entry_${index}_negative`]
                                  ? 'border-red-300' : 'border-gray-300'
                              }`}
                              placeholder="0.00"
                              disabled={!!entry.credit}
                            />
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              step="0.01"
                              min="0"
                              value={entry.credit}
                              onChange={(e) => updateEntry(index, 'credit', e.target.value)}
                              className={`w-full px-2 py-2 border rounded text-sm text-right ${
                                errors[`entry_${index}_amount`] || errors[`entry_${index}_both`] || errors[`entry_${index}_negative`]
                                  ? 'border-red-300' : 'border-gray-300'
                              }`}
                              placeholder="0.00"
                              disabled={!!entry.debit}
                            />
                            {(errors[`entry_${index}_amount`] || errors[`entry_${index}_both`] || errors[`entry_${index}_negative`]) && (
                              <p className="text-red-500 text-xs mt-1">
                                {errors[`entry_${index}_amount`] || errors[`entry_${index}_both`] || errors[`entry_${index}_negative`]}
                              </p>
                            )}
                          </td>
                          <td className="px-4 py-3">
                            {formData.entries.length > 2 && (
                              <button
                                type="button"
                                onClick={() => removeEntry(index)}
                                className="text-red-600 hover:text-red-800 text-sm"
                                title="Remove entry"
                              >
                                ✕
                              </button>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                  <tfoot className="bg-gray-50">
                    <tr>
                      <td colSpan="2" className="px-4 py-3 text-sm font-medium text-gray-900">
                        Totals:
                      </td>
                      <td className="px-4 py-3 text-sm font-bold text-right">
                        ${getTotalDebits().toFixed(2)}
                      </td>
                      <td className="px-4 py-3 text-sm font-bold text-right">
                        ${getTotalCredits().toFixed(2)}
                      </td>
                      <td className="px-4 py-3"></td>
                    </tr>
                    <tr>
                      <td colSpan="2" className="px-4 py-2 text-sm font-medium text-gray-700">
                        Difference:
                      </td>
                      <td colSpan="2" className={`px-4 py-2 text-sm font-bold text-right ${
                        isBalanced() ? 'text-green-600' : 'text-red-600'
                      }`}>
                        ${Math.abs(getOutOfBalance()).toFixed(2)} {!isBalanced() && (getOutOfBalance() > 0 ? '(Debit)' : '(Credit)')}
                      </td>
                      <td className="px-4 py-2"></td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>
          </div>

          {/* Memo */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Memo
            </label>
            <textarea
              value={formData.memo}
              onChange={(e) => setFormData(prev => ({ ...prev, memo: e.target.value }))}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Journal entry explanation..."
            />
          </div>

          {/* Error Display */}
          {(errors.entries || errors.duplicates || errors.balance || errors.submit) && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              {errors.entries && <p className="text-red-700 text-sm mb-2">{errors.entries}</p>}
              {errors.duplicates && <p className="text-red-700 text-sm mb-2">{errors.duplicates}</p>}
              {errors.balance && <p className="text-red-700 text-sm mb-2">{errors.balance}</p>}
              {errors.submit && <p className="text-red-700 text-sm">{errors.submit}</p>}
            </div>
          )}

          {/* Help Text */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Journal Entry Guidelines</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Total debits must equal total credits</li>
              <li>• Each line must have either a debit OR credit amount (not both)</li>
              <li>• All accounts and descriptions are required</li>
              <li>• Use this for adjusting entries, corrections, and manual bookkeeping</li>
            </ul>
          </div>

          {/* Submit Buttons */}
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
              type="submit"
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
              disabled={loading || !isBalanced()}
            >
              {loading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Creating...
                </div>
              ) : (
                'Create Journal Entry'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JournalEntry;
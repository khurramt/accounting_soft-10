import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main App Component
function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [accounts, setAccounts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch data on component mount
  useEffect(() => {
    fetchAccounts();
    fetchCustomers();
    fetchVendors();
    fetchTransactions();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await axios.get(`${API}/accounts`);
      setAccounts(response.data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    }
  };

  const fetchCustomers = async () => {
    try {
      const response = await axios.get(`${API}/customers`);
      setCustomers(response.data);
    } catch (error) {
      console.error('Error fetching customers:', error);
    }
  };

  const fetchVendors = async () => {
    try {
      const response = await axios.get(`${API}/vendors`);
      setVendors(response.data);
    } catch (error) {
      console.error('Error fetching vendors:', error);
    }
  };

  const fetchTransactions = async () => {
    try {
      const response = await axios.get(`${API}/transactions`);
      setTransactions(response.data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">QBClone Accounting</h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Welcome, Admin</span>
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">A</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar Navigation */}
        <nav className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen">
          <div className="p-4">
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => setCurrentPage('dashboard')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'dashboard' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📊 Dashboard
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('accounts')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'accounts' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  💼 Chart of Accounts
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('customers')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'customers' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  👥 Customers
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('vendors')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'vendors' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  🏢 Vendors
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('transactions')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'transactions' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📄 Transactions
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('reports')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'reports' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📈 Reports
                </button>
              </li>
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {currentPage === 'dashboard' && <Dashboard accounts={accounts} transactions={transactions} />}
          {currentPage === 'accounts' && <AccountsPage accounts={accounts} onRefresh={fetchAccounts} />}
          {currentPage === 'customers' && <CustomersPage customers={customers} onRefresh={fetchCustomers} />}
          {currentPage === 'vendors' && <VendorsPage vendors={vendors} onRefresh={fetchVendors} />}
          {currentPage === 'transactions' && <TransactionsPage transactions={transactions} accounts={accounts} customers={customers} vendors={vendors} onRefresh={fetchTransactions} />}
          {currentPage === 'reports' && <ReportsPage />}
        </main>
      </div>
    </div>
  );
}

// Dashboard Component
const Dashboard = ({ accounts, transactions }) => {
  const [reports, setReports] = useState({
    totalAssets: 0,
    totalLiabilities: 0,
    totalEquity: 0,
    totalIncome: 0,
    totalExpenses: 0,
    netIncome: 0
  });

  useEffect(() => {
    // Calculate basic metrics
    const assets = accounts.filter(acc => acc.account_type === 'Asset').reduce((sum, acc) => sum + acc.balance, 0);
    const liabilities = accounts.filter(acc => acc.account_type === 'Liability').reduce((sum, acc) => sum + acc.balance, 0);
    const equity = accounts.filter(acc => acc.account_type === 'Equity').reduce((sum, acc) => sum + acc.balance, 0);
    const income = accounts.filter(acc => acc.account_type === 'Income').reduce((sum, acc) => sum + acc.balance, 0);
    const expenses = accounts.filter(acc => acc.account_type === 'Expense').reduce((sum, acc) => sum + acc.balance, 0);

    setReports({
      totalAssets: assets,
      totalLiabilities: liabilities,
      totalEquity: equity,
      totalIncome: income,
      totalExpenses: expenses,
      netIncome: income - expenses
    });
  }, [accounts]);

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Total Assets</h3>
          <p className="text-2xl font-bold text-green-600">${reports.totalAssets.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Total Liabilities</h3>
          <p className="text-2xl font-bold text-red-600">${reports.totalLiabilities.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Total Equity</h3>
          <p className="text-2xl font-bold text-blue-600">${reports.totalEquity.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Net Income</h3>
          <p className={`text-2xl font-bold ${reports.netIncome >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${reports.netIncome.toLocaleString()}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Transactions</h3>
          <div className="space-y-3">
            {transactions.slice(0, 5).map((transaction) => (
              <div key={transaction.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{transaction.transaction_number}</p>
                  <p className="text-sm text-gray-600">{transaction.transaction_type}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-gray-900">${transaction.total.toLocaleString()}</p>
                  <p className="text-sm text-gray-600">{new Date(transaction.date).toLocaleDateString()}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Summary</h3>
          <div className="space-y-3">
            {['Asset', 'Liability', 'Equity', 'Income', 'Expense'].map((type) => {
              const accountsOfType = accounts.filter(acc => acc.account_type === type);
              const totalBalance = accountsOfType.reduce((sum, acc) => sum + acc.balance, 0);
              return (
                <div key={type} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium text-gray-900">{type} Accounts</p>
                    <p className="text-sm text-gray-600">{accountsOfType.length} accounts</p>
                  </div>
                  <p className="font-medium text-gray-900">${totalBalance.toLocaleString()}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

// Accounts Page Component
const AccountsPage = ({ accounts, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    account_type: 'Asset',
    detail_type: 'Checking',
    account_number: '',
    opening_balance: 0,
    opening_balance_date: new Date().toISOString().split('T')[0]
  });

  const accountTypes = {
    Asset: ['Checking', 'Savings', 'Accounts Receivable', 'Inventory', 'Fixed Assets'],
    Liability: ['Accounts Payable', 'Credit Card', 'Loan'],
    Equity: ['Owner\'s Equity', 'Retained Earnings'],
    Income: ['Sales', 'Service Income'],
    Expense: ['Office Expenses', 'Travel', 'Meals & Entertainment']
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/accounts`, {
        ...formData,
        opening_balance: parseFloat(formData.opening_balance),
        opening_balance_date: formData.opening_balance_date ? new Date(formData.opening_balance_date) : null
      });
      setShowModal(false);
      setFormData({
        name: '',
        account_type: 'Asset',
        detail_type: 'Checking',
        account_number: '',
        opening_balance: 0,
        opening_balance_date: new Date().toISOString().split('T')[0]
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating account:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Chart of Accounts</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Account
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detail Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Account #</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Balance</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {accounts.map((account) => (
              <tr key={account.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {account.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {account.account_type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {account.detail_type}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {account.account_number || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${account.balance.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Account</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Account Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Account Type</label>
                <select
                  value={formData.account_type}
                  onChange={(e) => setFormData({...formData, account_type: e.target.value, detail_type: accountTypes[e.target.value][0]})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {Object.keys(accountTypes).map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Detail Type</label>
                <select
                  value={formData.detail_type}
                  onChange={(e) => setFormData({...formData, detail_type: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  {accountTypes[formData.account_type].map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Account Number</label>
                <input
                  type="text"
                  value={formData.account_number}
                  onChange={(e) => setFormData({...formData, account_number: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Opening Balance</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.opening_balance}
                  onChange={(e) => setFormData({...formData, opening_balance: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Opening Balance Date</label>
                <input
                  type="date"
                  value={formData.opening_balance_date}
                  onChange={(e) => setFormData({...formData, opening_balance_date: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create Account
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Customers Page Component
const CustomersPage = ({ customers, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/customers`, formData);
      setShowModal(false);
      setFormData({
        name: '',
        company: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        zip_code: ''
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating customer:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Customers</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Customer
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Balance</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {customers.map((customer) => (
              <tr key={customer.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {customer.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {customer.company || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {customer.email || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {customer.phone || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${customer.balance.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Customer</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => setFormData({...formData, city: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => setFormData({...formData, state: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code</label>
                <input
                  type="text"
                  value={formData.zip_code}
                  onChange={(e) => setFormData({...formData, zip_code: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create Customer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Vendors Page Component
const VendorsPage = ({ vendors, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/vendors`, formData);
      setShowModal(false);
      setFormData({
        name: '',
        company: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        zip_code: ''
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating vendor:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Vendors</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Vendor
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Company</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Balance</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {vendors.map((vendor) => (
              <tr key={vendor.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {vendor.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {vendor.company || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {vendor.email || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {vendor.phone || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  ${vendor.balance.toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Vendor</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => setFormData({...formData, company: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                <input
                  type="text"
                  value={formData.address}
                  onChange={(e) => setFormData({...formData, address: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => setFormData({...formData, city: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => setFormData({...formData, state: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code</label>
                <input
                  type="text"
                  value={formData.zip_code}
                  onChange={(e) => setFormData({...formData, zip_code: e.target.value})}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create Vendor
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Transactions Page Component
const TransactionsPage = ({ transactions, accounts, customers, vendors, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    transaction_type: 'Invoice',
    customer_id: '',
    vendor_id: '',
    date: new Date().toISOString().split('T')[0],
    due_date: '',
    line_items: [{ description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }],
    tax_rate: 0,
    memo: ''
  });

  const handleAddLineItem = () => {
    setFormData({
      ...formData,
      line_items: [...formData.line_items, { description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }]
    });
  };

  const handleLineItemChange = (index, field, value) => {
    const newLineItems = [...formData.line_items];
    newLineItems[index][field] = value;
    
    if (field === 'quantity' || field === 'rate') {
      newLineItems[index].amount = parseFloat(newLineItems[index].quantity) * parseFloat(newLineItems[index].rate);
    }
    
    setFormData({ ...formData, line_items: newLineItems });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/transactions`, {
        ...formData,
        date: new Date(formData.date),
        due_date: formData.due_date ? new Date(formData.due_date) : null,
        tax_rate: parseFloat(formData.tax_rate),
        line_items: formData.line_items.map(item => ({
          ...item,
          quantity: parseFloat(item.quantity),
          rate: parseFloat(item.rate),
          amount: parseFloat(item.amount)
        }))
      });
      setShowModal(false);
      setFormData({
        transaction_type: 'Invoice',
        customer_id: '',
        vendor_id: '',
        date: new Date().toISOString().split('T')[0],
        due_date: '',
        line_items: [{ description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }],
        tax_rate: 0,
        memo: ''
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating transaction:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Transactions</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Transaction
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Number</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer/Vendor</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((transaction) => {
              const customerName = customers.find(c => c.id === transaction.customer_id)?.name;
              const vendorName = vendors.find(v => v.id === transaction.vendor_id)?.name;
              
              return (
                <tr key={transaction.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {transaction.transaction_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {transaction.transaction_type}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {new Date(transaction.date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {customerName || vendorName || '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${transaction.total.toLocaleString()}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Transaction</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Transaction Type</label>
                  <select
                    value={formData.transaction_type}
                    onChange={(e) => setFormData({...formData, transaction_type: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="Invoice">Invoice</option>
                    <option value="Bill">Bill</option>
                    <option value="Payment">Payment</option>
                    <option value="Journal">Journal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {formData.transaction_type === 'Invoice' ? 'Customer' : 'Vendor'}
                  </label>
                  <select
                    value={formData.transaction_type === 'Invoice' ? formData.customer_id : formData.vendor_id}
                    onChange={(e) => setFormData({
                      ...formData,
                      customer_id: formData.transaction_type === 'Invoice' ? e.target.value : '',
                      vendor_id: formData.transaction_type === 'Bill' ? e.target.value : ''
                    })}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select...</option>
                    {(formData.transaction_type === 'Invoice' ? customers : vendors).map((entity) => (
                      <option key={entity.id} value={entity.id}>{entity.name}</option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                  <input
                    type="date"
                    value={formData.due_date}
                    onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Line Items</label>
                <div className="space-y-2">
                  {formData.line_items.map((item, index) => (
                    <div key={index} className="grid grid-cols-6 gap-2 p-3 border border-gray-200 rounded-lg">
                      <div className="col-span-2">
                        <input
                          type="text"
                          placeholder="Description"
                          value={item.description}
                          onChange={(e) => handleLineItemChange(index, 'description', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                      </div>
                      <div>
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Qty"
                          value={item.quantity}
                          onChange={(e) => handleLineItemChange(index, 'quantity', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                      </div>
                      <div>
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Rate"
                          value={item.rate}
                          onChange={(e) => handleLineItemChange(index, 'rate', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        />
                      </div>
                      <div>
                        <input
                          type="number"
                          step="0.01"
                          placeholder="Amount"
                          value={item.amount}
                          readOnly
                          className="w-full p-2 border border-gray-300 rounded-lg bg-gray-50"
                        />
                      </div>
                      <div>
                        <select
                          value={item.account_id}
                          onChange={(e) => handleLineItemChange(index, 'account_id', e.target.value)}
                          className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        >
                          <option value="">Select Account</option>
                          {accounts
                            .filter(acc => formData.transaction_type === 'Invoice' ? acc.account_type === 'Income' : acc.account_type === 'Expense')
                            .map((account) => (
                              <option key={account.id} value={account.id}>{account.name}</option>
                            ))}
                        </select>
                      </div>
                    </div>
                  ))}
                </div>
                <button
                  type="button"
                  onClick={handleAddLineItem}
                  className="mt-2 text-blue-600 hover:text-blue-800"
                >
                  + Add Line Item
                </button>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tax Rate (%)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.tax_rate}
                    onChange={(e) => setFormData({...formData, tax_rate: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Memo</label>
                  <input
                    type="text"
                    value={formData.memo}
                    onChange={(e) => setFormData({...formData, memo: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create Transaction
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Reports Page Component
const ReportsPage = () => {
  const [currentReport, setCurrentReport] = useState('trial-balance');
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadReport = async (reportType) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/reports/${reportType}`);
      setReportData(response.data);
    } catch (error) {
      console.error('Error loading report:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReport(currentReport);
  }, [currentReport]);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Reports</h2>
        <div className="flex space-x-2">
          <button
            onClick={() => setCurrentReport('trial-balance')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              currentReport === 'trial-balance'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Trial Balance
          </button>
          <button
            onClick={() => setCurrentReport('balance-sheet')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              currentReport === 'balance-sheet'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Balance Sheet
          </button>
          <button
            onClick={() => setCurrentReport('income-statement')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              currentReport === 'income-statement'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Income Statement
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading report...</p>
          </div>
        ) : (
          <div className="p-6">
            {currentReport === 'trial-balance' && reportData && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Trial Balance</h3>
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-2">Account Name</th>
                      <th className="text-right py-2">Debit</th>
                      <th className="text-right py-2">Credit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reportData.trial_balance.map((account, index) => (
                      <tr key={index} className="border-b border-gray-100">
                        <td className="py-2">{account.account_name}</td>
                        <td className="py-2 text-right">${account.debit.toLocaleString()}</td>
                        <td className="py-2 text-right">${account.credit.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr className="border-t-2 border-gray-300 font-semibold">
                      <td className="py-2">Total</td>
                      <td className="py-2 text-right">${reportData.total_debits.toLocaleString()}</td>
                      <td className="py-2 text-right">${reportData.total_credits.toLocaleString()}</td>
                    </tr>
                  </tfoot>
                </table>
                <p className={`mt-4 text-sm ${reportData.balanced ? 'text-green-600' : 'text-red-600'}`}>
                  {reportData.balanced ? '✓ Books are balanced' : '✗ Books are not balanced'}
                </p>
              </div>
            )}

            {currentReport === 'balance-sheet' && reportData && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Balance Sheet</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Assets</h4>
                    {reportData.assets.map((asset, index) => (
                      <div key={index} className="flex justify-between py-1">
                        <span>{asset.name}</span>
                        <span>${asset.balance.toLocaleString()}</span>
                      </div>
                    ))}
                    <div className="border-t border-gray-300 mt-2 pt-2 font-semibold">
                      <div className="flex justify-between">
                        <span>Total Assets</span>
                        <span>${reportData.total_assets.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Liabilities & Equity</h4>
                    <div className="mb-4">
                      <h5 className="font-medium text-gray-700 mb-1">Liabilities</h5>
                      {reportData.liabilities.map((liability, index) => (
                        <div key={index} className="flex justify-between py-1">
                          <span>{liability.name}</span>
                          <span>${liability.balance.toLocaleString()}</span>
                        </div>
                      ))}
                      <div className="border-t border-gray-200 mt-1 pt-1 font-medium">
                        <div className="flex justify-between">
                          <span>Total Liabilities</span>
                          <span>${reportData.total_liabilities.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h5 className="font-medium text-gray-700 mb-1">Equity</h5>
                      {reportData.equity.map((equity, index) => (
                        <div key={index} className="flex justify-between py-1">
                          <span>{equity.name}</span>
                          <span>${equity.balance.toLocaleString()}</span>
                        </div>
                      ))}
                      <div className="border-t border-gray-200 mt-1 pt-1 font-medium">
                        <div className="flex justify-between">
                          <span>Total Equity</span>
                          <span>${reportData.total_equity.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>
                    <div className="border-t border-gray-300 mt-2 pt-2 font-semibold">
                      <div className="flex justify-between">
                        <span>Total Liabilities & Equity</span>
                        <span>${(reportData.total_liabilities + reportData.total_equity).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <p className={`mt-4 text-sm ${reportData.balanced ? 'text-green-600' : 'text-red-600'}`}>
                  {reportData.balanced ? '✓ Balance sheet is balanced' : '✗ Balance sheet is not balanced'}
                </p>
              </div>
            )}

            {currentReport === 'income-statement' && reportData && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Income Statement</h3>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Income</h4>
                    {reportData.income.map((income, index) => (
                      <div key={index} className="flex justify-between py-1">
                        <span>{income.name}</span>
                        <span>${income.balance.toLocaleString()}</span>
                      </div>
                    ))}
                    <div className="border-t border-gray-300 mt-2 pt-2 font-semibold">
                      <div className="flex justify-between">
                        <span>Total Income</span>
                        <span>${reportData.total_income.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Expenses</h4>
                    {reportData.expenses.map((expense, index) => (
                      <div key={index} className="flex justify-between py-1">
                        <span>{expense.name}</span>
                        <span>${expense.balance.toLocaleString()}</span>
                      </div>
                    ))}
                    <div className="border-t border-gray-300 mt-2 pt-2 font-semibold">
                      <div className="flex justify-between">
                        <span>Total Expenses</span>
                        <span>${reportData.total_expenses.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>
                  <div className="border-t-2 border-gray-300 pt-4">
                    <div className={`flex justify-between text-lg font-bold ${reportData.net_income >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      <span>Net Income</span>
                      <span>${reportData.net_income.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
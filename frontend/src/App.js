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
  const [employees, setEmployees] = useState([]);
  const [items, setItems] = useState([]);
  const [classes, setClasses] = useState([]);
  const [locations, setLocations] = useState([]);
  const [terms, setTerms] = useState([]);
  const [priceLevels, setPriceLevels] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [memorizedTransactions, setMemorizedTransactions] = useState([]);
  const [todos, setTodos] = useState([]);
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch all data on component mount
  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchAccounts(),
        fetchCustomers(),
        fetchVendors(),
        fetchEmployees(),
        fetchItems(),
        fetchClasses(),
        fetchLocations(),
        fetchTerms(),
        fetchPriceLevels(),
        fetchTransactions(),
        fetchMemorizedTransactions(),
        fetchTodos(),
        fetchUsers(),
        fetchRoles()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

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

  const fetchEmployees = async () => {
    try {
      const response = await axios.get(`${API}/employees`);
      setEmployees(response.data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const fetchItems = async () => {
    try {
      const response = await axios.get(`${API}/items`);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await axios.get(`${API}/classes`);
      setClasses(response.data);
    } catch (error) {
      console.error('Error fetching classes:', error);
    }
  };

  const fetchLocations = async () => {
    try {
      const response = await axios.get(`${API}/locations`);
      setLocations(response.data);
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const fetchTerms = async () => {
    try {
      const response = await axios.get(`${API}/terms`);
      setTerms(response.data);
    } catch (error) {
      console.error('Error fetching terms:', error);
    }
  };

  const fetchPriceLevels = async () => {
    try {
      const response = await axios.get(`${API}/price-levels`);
      setPriceLevels(response.data);
    } catch (error) {
      console.error('Error fetching price levels:', error);
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

  const fetchMemorizedTransactions = async () => {
    try {
      const response = await axios.get(`${API}/memorized-transactions`);
      setMemorizedTransactions(response.data);
    } catch (error) {
      console.error('Error fetching memorized transactions:', error);
    }
  };

  const fetchTodos = async () => {
    try {
      const response = await axios.get(`${API}/todos`);
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API}/users`);
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const fetchRoles = async () => {
    try {
      const response = await axios.get(`${API}/roles`);
      setRoles(response.data);
    } catch (error) {
      console.error('Error fetching roles:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        <p className="ml-4 text-lg text-gray-600">Loading QBClone...</p>
      </div>
    );
  }

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
              {/* Dashboard */}
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
              
              {/* Lists */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Lists</div>
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
                  onClick={() => setCurrentPage('items')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'items' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📦 Items & Services
                </button>
              </li>
              
              {/* People */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">People</div>
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
                  onClick={() => setCurrentPage('employees')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'employees' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  👤 Employees
                </button>
              </li>
              
              {/* Sales */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Sales</div>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('invoices')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'invoices' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📄 Invoices
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('sales-receipts')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'sales-receipts' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  🧾 Sales Receipts
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('estimates')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'estimates' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📋 Estimates
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('receive-payments')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'receive-payments' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  💰 Receive Payments
                </button>
              </li>
              
              {/* Purchases */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Purchases</div>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('bills')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'bills' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📋 Enter Bills
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('pay-bills')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'pay-bills' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  💳 Pay Bills
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('purchase-orders')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'purchase-orders' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📝 Purchase Orders
                </button>
              </li>
              
              {/* Banking */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Banking</div>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('checks')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'checks' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  ✏️ Write Checks
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('transfers')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'transfers' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  🔄 Transfer Funds
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('reconcile')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'reconcile' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  ⚖️ Reconcile
                </button>
              </li>
              
              {/* Reports */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Reports</div>
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
              
              {/* Company */}
              <li className="pt-2">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-4 py-1">Company</div>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('memorized-transactions')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'memorized-transactions' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  🔄 Memorized Transactions
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('calendar')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'calendar' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📅 Calendar & To-Dos
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('audit-trail')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'audit-trail' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📊 Audit Trail
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('users')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'users' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  👥 Users & Roles
                </button>
              </li>
              <li>
                <button
                  onClick={() => setCurrentPage('lists')}
                  className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
                    currentPage === 'lists' 
                      ? 'bg-blue-100 text-blue-700 font-medium' 
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  📝 Classes & Locations
                </button>
              </li>
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {currentPage === 'dashboard' && <Dashboard accounts={accounts} transactions={transactions} customers={customers} vendors={vendors} />}
          {currentPage === 'accounts' && <AccountsPage accounts={accounts} onRefresh={fetchAccounts} />}
          {currentPage === 'customers' && <CustomersPage customers={customers} terms={terms} onRefresh={fetchCustomers} />}
          {currentPage === 'vendors' && <VendorsPage vendors={vendors} terms={terms} onRefresh={fetchVendors} />}
          {currentPage === 'employees' && <EmployeesPage employees={employees} onRefresh={fetchEmployees} />}
          {currentPage === 'items' && <ItemsPage items={items} accounts={accounts} vendors={vendors} onRefresh={fetchItems} />}
          {currentPage === 'invoices' && <InvoicesPage transactions={transactions.filter(t => t.transaction_type === 'Invoice')} customers={customers} items={items} accounts={accounts} classes={classes} locations={locations} terms={terms} onRefresh={fetchTransactions} />}
          {currentPage === 'sales-receipts' && <SalesReceiptsPage transactions={transactions.filter(t => t.transaction_type === 'Sales Receipt')} customers={customers} items={items} accounts={accounts} onRefresh={fetchTransactions} />}
          {currentPage === 'estimates' && <EstimatesPage transactions={transactions.filter(t => t.transaction_type === 'Estimate')} customers={customers} items={items} accounts={accounts} onRefresh={fetchTransactions} />}
          {currentPage === 'receive-payments' && <ReceivePaymentsPage customers={customers} transactions={transactions} accounts={accounts} onRefresh={fetchTransactions} />}
          {currentPage === 'bills' && <BillsPage transactions={transactions.filter(t => t.transaction_type === 'Bill')} vendors={vendors} items={items} accounts={accounts} onRefresh={fetchTransactions} />}
          {currentPage === 'pay-bills' && <PayBillsPage vendors={vendors} transactions={transactions} accounts={accounts} onRefresh={fetchTransactions} />}
          {currentPage === 'purchase-orders' && <PurchaseOrdersPage transactions={transactions.filter(t => t.transaction_type === 'Purchase Order')} vendors={vendors} items={items} onRefresh={fetchTransactions} />}
          {currentPage === 'checks' && <ChecksPage accounts={accounts} vendors={vendors} items={items} onRefresh={fetchTransactions} />}
          {currentPage === 'transfers' && <TransfersPage accounts={accounts} onRefresh={fetchAccounts} />}
          {currentPage === 'reconcile' && <ReconcilePage accounts={accounts} transactions={transactions} />}
          {currentPage === 'reports' && <ReportsPage />}
          {currentPage === 'memorized-transactions' && <MemorizedTransactionsPage memorizedTransactions={memorizedTransactions} onRefresh={fetchMemorizedTransactions} />}
          {currentPage === 'calendar' && <CalendarPage todos={todos} transactions={transactions} onRefresh={fetchTodos} />}
          {currentPage === 'audit-trail' && <AuditTrailPage />}
          {currentPage === 'users' && <UsersPage users={users} roles={roles} onRefreshUsers={fetchUsers} onRefreshRoles={fetchRoles} />}
          {currentPage === 'lists' && <ListsPage classes={classes} locations={locations} terms={terms} priceLevels={priceLevels} onRefreshClasses={fetchClasses} onRefreshLocations={fetchLocations} onRefreshTerms={fetchTerms} onRefreshPriceLevels={fetchPriceLevels} />}
        </main>
      </div>
    </div>
  );
}

// Dashboard Component
const Dashboard = ({ accounts, transactions, customers, vendors }) => {
  const [reports, setReports] = useState({
    totalAssets: 0,
    totalLiabilities: 0,
    totalEquity: 0,
    totalIncome: 0,
    totalExpenses: 0,
    netIncome: 0,
    totalAR: 0,
    totalAP: 0
  });

  useEffect(() => {
    // Calculate basic metrics
    const assets = accounts.filter(acc => acc.account_type === 'Asset').reduce((sum, acc) => sum + acc.balance, 0);
    const liabilities = accounts.filter(acc => acc.account_type === 'Liability').reduce((sum, acc) => sum + acc.balance, 0);
    const equity = accounts.filter(acc => acc.account_type === 'Equity').reduce((sum, acc) => sum + acc.balance, 0);
    const income = accounts.filter(acc => acc.account_type === 'Income').reduce((sum, acc) => sum + acc.balance, 0);
    const expenses = accounts.filter(acc => acc.account_type === 'Expense').reduce((sum, acc) => sum + acc.balance, 0);
    
    const totalAR = customers.reduce((sum, customer) => sum + customer.balance, 0);
    const totalAP = vendors.reduce((sum, vendor) => sum + vendor.balance, 0);

    setReports({
      totalAssets: assets,
      totalLiabilities: liabilities,
      totalEquity: equity,
      totalIncome: income,
      totalExpenses: expenses,
      netIncome: income - expenses,
      totalAR: totalAR,
      totalAP: totalAP
    });
  }, [accounts, customers, vendors]);

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Company Snapshot</h2>
      
      {/* Key Metrics */}
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

      {/* Secondary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Accounts Receivable</h3>
          <p className="text-2xl font-bold text-orange-600">${reports.totalAR.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Accounts Payable</h3>
          <p className="text-2xl font-bold text-purple-600">${reports.totalAP.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Total Income</h3>
          <p className="text-2xl font-bold text-cyan-600">${reports.totalIncome.toLocaleString()}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-sm font-medium text-gray-600">Total Expenses</h3>
          <p className="text-2xl font-bold text-red-500">${reports.totalExpenses.toLocaleString()}</p>
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

// Accounts Page Component (keeping existing implementation)
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
    Asset: ['Checking', 'Savings', 'Accounts Receivable', 'Inventory', 'Fixed Assets', 'Undeposited Funds'],
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

// Continue with other components...
// I'll implement the remaining components (Items, Employees, etc.) in a follow-up due to length constraints

export default App;
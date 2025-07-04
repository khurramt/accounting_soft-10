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

// Customers Page Component (Enhanced)
const CustomersPage = ({ customers, terms, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    terms: '',
    credit_limit: '',
    tax_id: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API}/customers`, {
        ...formData,
        credit_limit: formData.credit_limit ? parseFloat(formData.credit_limit) : null
      });
      setShowModal(false);
      setFormData({
        name: '',
        company: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        state: '',
        zip_code: '',
        terms: '',
        credit_limit: '',
        tax_id: ''
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating customer:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Customer Center</h2>
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
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Credit Limit</th>
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
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {customer.credit_limit ? `$${customer.credit_limit.toLocaleString()}` : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Customer Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Customer</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
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
              </div>
              <div className="grid grid-cols-2 gap-4">
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
              <div className="grid grid-cols-3 gap-4">
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
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code</label>
                  <input
                    type="text"
                    value={formData.zip_code}
                    onChange={(e) => setFormData({...formData, zip_code: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Terms</label>
                  <select
                    value={formData.terms}
                    onChange={(e) => setFormData({...formData, terms: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select Terms</option>
                    {terms.map(term => (
                      <option key={term.id} value={term.name}>{term.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Credit Limit</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.credit_limit}
                    onChange={(e) => setFormData({...formData, credit_limit: e.target.value})}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Tax ID</label>
                <input
                  type="text"
                  value={formData.tax_id}
                  onChange={(e) => setFormData({...formData, tax_id: e.target.value})}
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

// Vendors Page Component (Enhanced)
const VendorsPage = ({ vendors, terms, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    company: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    terms: '',
    tax_id: ''
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
        zip_code: '',
        terms: '',
        tax_id: ''
      });
      onRefresh();
    } catch (error) {
      console.error('Error creating vendor:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Vendor Center</h2>
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
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Terms</th>
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
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {vendor.terms || '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Vendor Modal - Similar to Customer Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Vendor</h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
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
              </div>
              {/* Include all other fields similar to customer form */}
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

// Placeholder components for other pages to make the app functional
// These would be implemented with full functionality in a production environment

// Employees Page Component (Full Implementation)
const EmployeesPage = ({ employees, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [activeTab, setActiveTab] = useState('summary');
  const [formData, setFormData] = useState({
    name: '',
    status: 'Active',
    title: '',
    ssn: '',
    employee_id: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: '',
    hire_date: '',
    pay_type: 'Hourly',
    pay_rate: '',
    pay_schedule: 'Weekly',
    vacation_balance: 0,
    sick_balance: 0,
    notes: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        pay_rate: formData.pay_rate ? parseFloat(formData.pay_rate) : null,
        vacation_balance: parseFloat(formData.vacation_balance),
        sick_balance: parseFloat(formData.sick_balance),
        hire_date: formData.hire_date ? new Date(formData.hire_date) : null
      };

      if (selectedEmployee) {
        await axios.put(`${API}/employees/${selectedEmployee.id}`, submitData);
      } else {
        await axios.post(`${API}/employees`, submitData);
      }
      
      setShowModal(false);
      setSelectedEmployee(null);
      resetForm();
      onRefresh();
    } catch (error) {
      console.error('Error saving employee:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      status: 'Active',
      title: '',
      ssn: '',
      employee_id: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      state: '',
      zip_code: '',
      hire_date: '',
      pay_type: 'Hourly',
      pay_rate: '',
      pay_schedule: 'Weekly',
      vacation_balance: 0,
      sick_balance: 0,
      notes: ''
    });
  };

  const handleEdit = (employee) => {
    setSelectedEmployee(employee);
    setFormData({
      name: employee.name,
      status: employee.status,
      title: employee.title || '',
      ssn: employee.ssn || '',
      employee_id: employee.employee_id || '',
      email: employee.email || '',
      phone: employee.phone || '',
      address: employee.address || '',
      city: employee.city || '',
      state: employee.state || '',
      zip_code: employee.zip_code || '',
      hire_date: employee.hire_date ? new Date(employee.hire_date).toISOString().split('T')[0] : '',
      pay_type: employee.pay_type || 'Hourly',
      pay_rate: employee.pay_rate || '',
      pay_schedule: employee.pay_schedule || 'Weekly',
      vacation_balance: employee.vacation_balance,
      sick_balance: employee.sick_balance,
      notes: employee.notes || ''
    });
    setShowModal(true);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Employee Center</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Employee
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Employee ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pay Schedule</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hire Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {employees.map((employee) => (
              <tr key={employee.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-gray-900">{employee.name}</div>
                    {employee.email && <div className="text-sm text-gray-500">{employee.email}</div>}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    employee.status === 'Active' ? 'bg-green-100 text-green-800' :
                    employee.status === 'Inactive' ? 'bg-gray-100 text-gray-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {employee.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {employee.title || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {employee.employee_id || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {employee.pay_schedule || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {employee.hire_date ? new Date(employee.hire_date).toLocaleDateString() : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  <button
                    onClick={() => handleEdit(employee)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Employee Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {selectedEmployee ? 'Edit Employee' : 'Create New Employee'}
            </h3>
            
            {/* Tabs */}
            <div className="border-b border-gray-200 mb-6">
              <nav className="-mb-px flex space-x-8">
                {['summary', 'payroll', 'timeoff'].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {tab.charAt(0).toUpperCase() + tab.slice(1)}
                  </button>
                ))}
              </nav>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              {activeTab === 'summary' && (
                <>
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({...formData, name: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                      <select
                        value={formData.status}
                        onChange={(e) => setFormData({...formData, status: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="Active">Active</option>
                        <option value="Inactive">Inactive</option>
                        <option value="Terminated">Terminated</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                      <input
                        type="text"
                        value={formData.title}
                        onChange={(e) => setFormData({...formData, title: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Employee ID</label>
                      <input
                        type="text"
                        value={formData.employee_id}
                        onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({...formData, email: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                      <input
                        type="tel"
                        value={formData.phone}
                        onChange={(e) => setFormData({...formData, phone: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                    <input
                      type="text"
                      value={formData.address}
                      onChange={(e) => setFormData({...formData, address: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                      <input
                        type="text"
                        value={formData.city}
                        onChange={(e) => setFormData({...formData, city: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">State</label>
                      <input
                        type="text"
                        value={formData.state}
                        onChange={(e) => setFormData({...formData, state: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">ZIP Code</label>
                      <input
                        type="text"
                        value={formData.zip_code}
                        onChange={(e) => setFormData({...formData, zip_code: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Hire Date</label>
                    <input
                      type="date"
                      value={formData.hire_date}
                      onChange={(e) => setFormData({...formData, hire_date: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </>
              )}

              {activeTab === 'payroll' && (
                <>
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">SSN/Tax ID</label>
                      <input
                        type="text"
                        value={formData.ssn}
                        onChange={(e) => setFormData({...formData, ssn: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="XXX-XX-XXXX"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Pay Type</label>
                      <select
                        value={formData.pay_type}
                        onChange={(e) => setFormData({...formData, pay_type: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="Hourly">Hourly</option>
                        <option value="Salary">Salary</option>
                        <option value="Commission">Commission</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Pay Rate ({formData.pay_type === 'Hourly' ? 'per hour' : 'annual'})
                      </label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.pay_rate}
                        onChange={(e) => setFormData({...formData, pay_rate: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Pay Schedule</label>
                      <select
                        value={formData.pay_schedule}
                        onChange={(e) => setFormData({...formData, pay_schedule: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      >
                        <option value="Weekly">Weekly</option>
                        <option value="Bi-weekly">Bi-weekly</option>
                        <option value="Semi-monthly">Semi-monthly</option>
                        <option value="Monthly">Monthly</option>
                      </select>
                    </div>
                  </div>
                </>
              )}

              {activeTab === 'timeoff' && (
                <>
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Vacation Balance (hours)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.vacation_balance}
                        onChange={(e) => setFormData({...formData, vacation_balance: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Sick Balance (hours)</label>
                      <input
                        type="number"
                        step="0.01"
                        value={formData.sick_balance}
                        onChange={(e) => setFormData({...formData, sick_balance: e.target.value})}
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                    <textarea
                      value={formData.notes}
                      onChange={(e) => setFormData({...formData, notes: e.target.value})}
                      rows={4}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Employee notes, performance reviews, etc."
                    />
                  </div>
                </>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setSelectedEmployee(null);
                    resetForm();
                    setActiveTab('summary');
                  }}
                  className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {selectedEmployee ? 'Update Employee' : 'Create Employee'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Items & Services Page Component (Full Implementation)
const ItemsPage = ({ items, accounts, vendors, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    item_number: '',
    item_type: 'Service',
    description: '',
    sales_price: '',
    cost: '',
    income_account_id: '',
    expense_account_id: '',
    inventory_account_id: '',
    qty_on_hand: 0,
    reorder_point: '',
    preferred_vendor_id: '',
    tax_code: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        sales_price: formData.sales_price ? parseFloat(formData.sales_price) : null,
        cost: formData.cost ? parseFloat(formData.cost) : null,
        qty_on_hand: parseFloat(formData.qty_on_hand),
        reorder_point: formData.reorder_point ? parseFloat(formData.reorder_point) : null
      };

      if (selectedItem) {
        await axios.put(`${API}/items/${selectedItem.id}`, submitData);
      } else {
        await axios.post(`${API}/items`, submitData);
      }
      
      setShowModal(false);
      setSelectedItem(null);
      resetForm();
      onRefresh();
    } catch (error) {
      console.error('Error saving item:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      item_number: '',
      item_type: 'Service',
      description: '',
      sales_price: '',
      cost: '',
      income_account_id: '',
      expense_account_id: '',
      inventory_account_id: '',
      qty_on_hand: 0,
      reorder_point: '',
      preferred_vendor_id: '',
      tax_code: ''
    });
  };

  const handleEdit = (item) => {
    setSelectedItem(item);
    setFormData({
      name: item.name,
      item_number: item.item_number || '',
      item_type: item.item_type,
      description: item.description || '',
      sales_price: item.sales_price || '',
      cost: item.cost || '',
      income_account_id: item.income_account_id || '',
      expense_account_id: item.expense_account_id || '',
      inventory_account_id: item.inventory_account_id || '',
      qty_on_hand: item.qty_on_hand,
      reorder_point: item.reorder_point || '',
      preferred_vendor_id: item.preferred_vendor_id || '',
      tax_code: item.tax_code || ''
    });
    setShowModal(true);
  };

  const incomeAccounts = accounts.filter(acc => acc.account_type === 'Income');
  const expenseAccounts = accounts.filter(acc => acc.account_type === 'Expense');
  const assetAccounts = accounts.filter(acc => acc.account_type === 'Asset');

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Items & Services</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + New Item
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name/Number</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sales Price</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Qty on Hand</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reorder Point</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {items.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div className="text-sm font-medium text-gray-900">{item.name}</div>
                    {item.item_number && <div className="text-sm text-gray-500">#{item.item_number}</div>}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    item.item_type === 'Inventory' ? 'bg-blue-100 text-blue-800' :
                    item.item_type === 'Service' ? 'bg-green-100 text-green-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {item.item_type}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {item.sales_price ? `$${item.sales_price.toLocaleString()}` : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {item.cost ? `$${item.cost.toLocaleString()}` : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {item.item_type === 'Inventory' ? item.qty_on_hand : '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {item.reorder_point || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  <button
                    onClick={() => handleEdit(item)}
                    className="text-blue-600 hover:text-blue-800 mr-3"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Item Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {selectedItem ? 'Edit Item' : 'Create New Item'}
            </h3>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Item Name *</label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Item Number</label>
                  <input
                    type="text"
                    value={formData.item_number}
                    onChange={(e) => setFormData({...formData, item_number: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Item Type *</label>
                  <select
                    value={formData.item_type}
                    onChange={(e) => setFormData({...formData, item_type: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="Service">Service</option>
                    <option value="Inventory">Inventory</option>
                    <option value="Non-Inventory">Non-Inventory</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tax Code</label>
                  <input
                    type="text"
                    value={formData.tax_code}
                    onChange={(e) => setFormData({...formData, tax_code: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  rows={3}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Sales Price</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.sales_price}
                    onChange={(e) => setFormData({...formData, sales_price: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Cost</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.cost}
                    onChange={(e) => setFormData({...formData, cost: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Income Account</label>
                  <select
                    value={formData.income_account_id}
                    onChange={(e) => setFormData({...formData, income_account_id: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select Account</option>
                    {incomeAccounts.map(account => (
                      <option key={account.id} value={account.id}>{account.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Expense Account</label>
                  <select
                    value={formData.expense_account_id}
                    onChange={(e) => setFormData({...formData, expense_account_id: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select Account</option>
                    {expenseAccounts.map(account => (
                      <option key={account.id} value={account.id}>{account.name}</option>
                    ))}
                  </select>
                </div>
                {formData.item_type === 'Inventory' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Inventory Account</label>
                    <select
                      value={formData.inventory_account_id}
                      onChange={(e) => setFormData({...formData, inventory_account_id: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Account</option>
                      {assetAccounts.map(account => (
                        <option key={account.id} value={account.id}>{account.name}</option>
                      ))}
                    </select>
                  </div>
                )}
              </div>

              {formData.item_type === 'Inventory' && (
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Quantity on Hand</label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.qty_on_hand}
                      onChange={(e) => setFormData({...formData, qty_on_hand: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Reorder Point</label>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.reorder_point}
                      onChange={(e) => setFormData({...formData, reorder_point: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Preferred Vendor</label>
                    <select
                      value={formData.preferred_vendor_id}
                      onChange={(e) => setFormData({...formData, preferred_vendor_id: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">Select Vendor</option>
                      {vendors.map(vendor => (
                        <option key={vendor.id} value={vendor.id}>{vendor.name}</option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setSelectedItem(null);
                    resetForm();
                  }}
                  className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {selectedItem ? 'Update Item' : 'Create Item'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

// Invoices Page Component (Full Implementation)
const InvoicesPage = ({ transactions, customers, items, accounts, classes, locations, terms, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedInvoice, setSelectedInvoice] = useState(null);
  const [formData, setFormData] = useState({
    customer_id: '',
    date: new Date().toISOString().split('T')[0],
    due_date: '',
    reference_number: '',
    po_number: '',
    terms_id: '',
    bill_to_address: '',
    ship_to_address: '',
    line_items: [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '', class_id: '', location_id: '' }],
    tax_rate: 0,
    memo: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        transaction_type: 'Invoice',
        date: new Date(formData.date),
        due_date: formData.due_date ? new Date(formData.due_date) : null,
        tax_rate: parseFloat(formData.tax_rate),
        line_items: formData.line_items.map(item => ({
          ...item,
          quantity: parseFloat(item.quantity),
          rate: parseFloat(item.rate),
          amount: parseFloat(item.amount)
        }))
      };

      if (selectedInvoice) {
        await axios.put(`${API}/transactions/${selectedInvoice.id}`, submitData);
      } else {
        await axios.post(`${API}/transactions`, submitData);
      }
      
      setShowModal(false);
      setSelectedInvoice(null);
      resetForm();
      onRefresh();
    } catch (error) {
      console.error('Error saving invoice:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      customer_id: '',
      date: new Date().toISOString().split('T')[0],
      due_date: '',
      reference_number: '',
      po_number: '',
      terms_id: '',
      bill_to_address: '',
      ship_to_address: '',
      line_items: [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '', class_id: '', location_id: '' }],
      tax_rate: 0,
      memo: ''
    });
  };

  const handleAddLineItem = () => {
    setFormData({
      ...formData,
      line_items: [...formData.line_items, { item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '', class_id: '', location_id: '' }]
    });
  };

  const handleLineItemChange = (index, field, value) => {
    const newLineItems = [...formData.line_items];
    newLineItems[index][field] = value;
    
    if (field === 'quantity' || field === 'rate') {
      newLineItems[index].amount = parseFloat(newLineItems[index].quantity) * parseFloat(newLineItems[index].rate);
    }
    
    if (field === 'item_id' && value) {
      const selectedItem = items.find(item => item.id === value);
      if (selectedItem) {
        newLineItems[index].description = selectedItem.description || selectedItem.name;
        newLineItems[index].rate = selectedItem.sales_price || 0;
        newLineItems[index].amount = parseFloat(newLineItems[index].quantity) * parseFloat(selectedItem.sales_price || 0);
        newLineItems[index].account_id = selectedItem.income_account_id || '';
      }
    }
    
    setFormData({ ...formData, line_items: newLineItems });
  };

  const removeLineItem = (index) => {
    const newLineItems = formData.line_items.filter((_, i) => i !== index);
    setFormData({ ...formData, line_items: newLineItems });
  };

  const handleEdit = (invoice) => {
    setSelectedInvoice(invoice);
    setFormData({
      customer_id: invoice.customer_id || '',
      date: new Date(invoice.date).toISOString().split('T')[0],
      due_date: invoice.due_date ? new Date(invoice.due_date).toISOString().split('T')[0] : '',
      reference_number: invoice.reference_number || '',
      po_number: invoice.po_number || '',
      terms_id: invoice.terms_id || '',
      bill_to_address: invoice.bill_to_address || '',
      ship_to_address: invoice.ship_to_address || '',
      line_items: invoice.line_items.length > 0 ? invoice.line_items : [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '', class_id: '', location_id: '' }],
      tax_rate: invoice.tax_rate || 0,
      memo: invoice.memo || ''
    });
    setShowModal(true);
  };

  const calculateSubtotal = () => {
    return formData.line_items.reduce((sum, item) => sum + (parseFloat(item.amount) || 0), 0);
  };

  const calculateTax = () => {
    const subtotal = calculateSubtotal();
    return subtotal * (parseFloat(formData.tax_rate) / 100);
  };

  const calculateTotal = () => {
    return calculateSubtotal() + calculateTax();
  };

  const incomeAccounts = accounts.filter(acc => acc.account_type === 'Income');

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Invoices</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Create Invoice
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invoice #</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Customer</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((invoice) => {
              const customer = customers.find(c => c.id === invoice.customer_id);
              return (
                <tr key={invoice.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {invoice.transaction_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {customer?.name || 'Unknown Customer'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {new Date(invoice.date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${invoice.total.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      invoice.status === 'Paid' ? 'bg-green-100 text-green-800' :
                      invoice.status === 'Open' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {invoice.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <button
                      onClick={() => handleEdit(invoice)}
                      className="text-blue-600 hover:text-blue-800 mr-3"
                    >
                      Edit
                    </button>
                    <button className="text-green-600 hover:text-green-800 mr-3">
                      Print
                    </button>
                    <button className="text-purple-600 hover:text-purple-800">
                      Email
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Invoice Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-6xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {selectedInvoice ? 'Edit Invoice' : 'Create New Invoice'}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Header Information */}
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Customer *</label>
                  <select
                    value={formData.customer_id}
                    onChange={(e) => setFormData({...formData, customer_id: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  >
                    <option value="">Select Customer</option>
                    {customers.map(customer => (
                      <option key={customer.id} value={customer.id}>{customer.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Invoice Date *</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                  <input
                    type="date"
                    value={formData.due_date}
                    onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Reference Number</label>
                  <input
                    type="text"
                    value={formData.reference_number}
                    onChange={(e) => setFormData({...formData, reference_number: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">PO Number</label>
                  <input
                    type="text"
                    value={formData.po_number}
                    onChange={(e) => setFormData({...formData, po_number: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Terms</label>
                  <select
                    value={formData.terms_id}
                    onChange={(e) => setFormData({...formData, terms_id: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select Terms</option>
                    {terms.map(term => (
                      <option key={term.id} value={term.id}>{term.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Addresses */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bill To Address</label>
                  <textarea
                    value={formData.bill_to_address}
                    onChange={(e) => setFormData({...formData, bill_to_address: e.target.value})}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Ship To Address</label>
                  <textarea
                    value={formData.ship_to_address}
                    onChange={(e) => setFormData({...formData, ship_to_address: e.target.value})}
                    rows={3}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              {/* Line Items */}
              <div>
                <div className="flex justify-between items-center mb-3">
                  <label className="block text-sm font-medium text-gray-700">Line Items</label>
                  <button
                    type="button"
                    onClick={handleAddLineItem}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    + Add Line Item
                  </button>
                </div>
                
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Item</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Description</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Qty</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Rate</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Amount</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Account</th>
                        <th className="px-3 py-2"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {formData.line_items.map((item, index) => (
                        <tr key={index} className="border-t border-gray-200">
                          <td className="px-3 py-2">
                            <select
                              value={item.item_id}
                              onChange={(e) => handleLineItemChange(index, 'item_id', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            >
                              <option value="">Select Item</option>
                              {items.map(item => (
                                <option key={item.id} value={item.id}>{item.name}</option>
                              ))}
                            </select>
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="text"
                              value={item.description}
                              onChange={(e) => handleLineItemChange(index, 'description', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.quantity}
                              onChange={(e) => handleLineItemChange(index, 'quantity', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.rate}
                              onChange={(e) => handleLineItemChange(index, 'rate', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.amount}
                              readOnly
                              className="w-full p-2 border border-gray-300 rounded text-sm bg-gray-50"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <select
                              value={item.account_id}
                              onChange={(e) => handleLineItemChange(index, 'account_id', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            >
                              <option value="">Select Account</option>
                              {incomeAccounts.map(account => (
                                <option key={account.id} value={account.id}>{account.name}</option>
                              ))}
                            </select>
                          </td>
                          <td className="px-3 py-2">
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

              {/* Totals */}
              <div className="flex justify-end">
                <div className="w-64 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Subtotal:</span>
                    <span className="text-sm font-medium">${calculateSubtotal().toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Tax Rate:</span>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.tax_rate}
                      onChange={(e) => setFormData({...formData, tax_rate: e.target.value})}
                      className="w-16 p-1 border border-gray-300 rounded text-sm text-right"
                    />
                    <span className="text-sm text-gray-600">%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Tax Amount:</span>
                    <span className="text-sm font-medium">${calculateTax().toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between border-t pt-2">
                    <span className="text-lg font-medium">Total:</span>
                    <span className="text-lg font-bold">${calculateTotal().toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Memo</label>
                <textarea
                  value={formData.memo}
                  onChange={(e) => setFormData({...formData, memo: e.target.value})}
                  rows={2}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setSelectedInvoice(null);
                    resetForm();
                  }}
                  className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {selectedInvoice ? 'Update Invoice' : 'Create Invoice'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const SalesReceiptsPage = ({ transactions, customers, items, accounts, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Sales Receipts</h2>
    <p className="text-gray-600">Sales receipt functionality coming soon...</p>
  </div>
);

const EstimatesPage = ({ transactions, customers, items, accounts, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Estimates</h2>
    <p className="text-gray-600">Estimate functionality coming soon...</p>
  </div>
);

const ReceivePaymentsPage = ({ customers, transactions, accounts, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Receive Payments</h2>
    <p className="text-gray-600">Payment processing functionality coming soon...</p>
  </div>
);

// Bills Page Component (Full Implementation)
const BillsPage = ({ transactions, vendors, items, accounts, onRefresh }) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedBill, setSelectedBill] = useState(null);
  const [formData, setFormData] = useState({
    vendor_id: '',
    date: new Date().toISOString().split('T')[0],
    due_date: '',
    reference_number: '',
    terms_id: '',
    line_items: [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }],
    tax_rate: 0,
    memo: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        transaction_type: 'Bill',
        date: new Date(formData.date),
        due_date: formData.due_date ? new Date(formData.due_date) : null,
        tax_rate: parseFloat(formData.tax_rate),
        line_items: formData.line_items.map(item => ({
          ...item,
          quantity: parseFloat(item.quantity),
          rate: parseFloat(item.rate),
          amount: parseFloat(item.amount)
        }))
      };

      if (selectedBill) {
        await axios.put(`${API}/transactions/${selectedBill.id}`, submitData);
      } else {
        await axios.post(`${API}/transactions`, submitData);
      }
      
      setShowModal(false);
      setSelectedBill(null);
      resetForm();
      onRefresh();
    } catch (error) {
      console.error('Error saving bill:', error);
    }
  };

  const resetForm = () => {
    setFormData({
      vendor_id: '',
      date: new Date().toISOString().split('T')[0],
      due_date: '',
      reference_number: '',
      terms_id: '',
      line_items: [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }],
      tax_rate: 0,
      memo: ''
    });
  };

  const handleAddLineItem = () => {
    setFormData({
      ...formData,
      line_items: [...formData.line_items, { item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }]
    });
  };

  const handleLineItemChange = (index, field, value) => {
    const newLineItems = [...formData.line_items];
    newLineItems[index][field] = value;
    
    if (field === 'quantity' || field === 'rate') {
      newLineItems[index].amount = parseFloat(newLineItems[index].quantity) * parseFloat(newLineItems[index].rate);
    }
    
    if (field === 'item_id' && value) {
      const selectedItem = items.find(item => item.id === value);
      if (selectedItem) {
        newLineItems[index].description = selectedItem.description || selectedItem.name;
        newLineItems[index].rate = selectedItem.cost || 0;
        newLineItems[index].amount = parseFloat(newLineItems[index].quantity) * parseFloat(selectedItem.cost || 0);
        newLineItems[index].account_id = selectedItem.expense_account_id || '';
      }
    }
    
    setFormData({ ...formData, line_items: newLineItems });
  };

  const removeLineItem = (index) => {
    const newLineItems = formData.line_items.filter((_, i) => i !== index);
    setFormData({ ...formData, line_items: newLineItems });
  };

  const handleEdit = (bill) => {
    setSelectedBill(bill);
    setFormData({
      vendor_id: bill.vendor_id || '',
      date: new Date(bill.date).toISOString().split('T')[0],
      due_date: bill.due_date ? new Date(bill.due_date).toISOString().split('T')[0] : '',
      reference_number: bill.reference_number || '',
      terms_id: bill.terms_id || '',
      line_items: bill.line_items.length > 0 ? bill.line_items : [{ item_id: '', description: '', quantity: 1, rate: 0, amount: 0, account_id: '' }],
      tax_rate: bill.tax_rate || 0,
      memo: bill.memo || ''
    });
    setShowModal(true);
  };

  const calculateSubtotal = () => {
    return formData.line_items.reduce((sum, item) => sum + (parseFloat(item.amount) || 0), 0);
  };

  const calculateTax = () => {
    const subtotal = calculateSubtotal();
    return subtotal * (parseFloat(formData.tax_rate) / 100);
  };

  const calculateTotal = () => {
    return calculateSubtotal() + calculateTax();
  };

  const expenseAccounts = accounts.filter(acc => acc.account_type === 'Expense');

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Enter Bills</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          + Enter Bill
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bill #</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {transactions.map((bill) => {
              const vendor = vendors.find(v => v.id === bill.vendor_id);
              return (
                <tr key={bill.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {bill.transaction_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {vendor?.name || 'Unknown Vendor'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {new Date(bill.date).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {bill.due_date ? new Date(bill.due_date).toLocaleDateString() : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    ${bill.total.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      bill.status === 'Paid' ? 'bg-green-100 text-green-800' :
                      bill.status === 'Open' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {bill.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    <button
                      onClick={() => handleEdit(bill)}
                      className="text-blue-600 hover:text-blue-800 mr-3"
                    >
                      Edit
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Bill Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-6xl max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {selectedBill ? 'Edit Bill' : 'Enter New Bill'}
            </h3>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Header Information */}
              <div className="grid grid-cols-3 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vendor *</label>
                  <select
                    value={formData.vendor_id}
                    onChange={(e) => setFormData({...formData, vendor_id: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  >
                    <option value="">Select Vendor</option>
                    {vendors.map(vendor => (
                      <option key={vendor.id} value={vendor.id}>{vendor.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bill Date *</label>
                  <input
                    type="date"
                    value={formData.date}
                    onChange={(e) => setFormData({...formData, date: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                  <input
                    type="date"
                    value={formData.due_date}
                    onChange={(e) => setFormData({...formData, due_date: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reference Number</label>
                <input
                  type="text"
                  value={formData.reference_number}
                  onChange={(e) => setFormData({...formData, reference_number: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Vendor invoice number"
                />
              </div>

              {/* Line Items */}
              <div>
                <div className="flex justify-between items-center mb-3">
                  <label className="block text-sm font-medium text-gray-700">Expenses</label>
                  <button
                    type="button"
                    onClick={handleAddLineItem}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    + Add Line
                  </button>
                </div>
                
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Item</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Description</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Qty</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Cost</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Amount</th>
                        <th className="px-3 py-2 text-left text-xs font-medium text-gray-500">Account</th>
                        <th className="px-3 py-2"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {formData.line_items.map((item, index) => (
                        <tr key={index} className="border-t border-gray-200">
                          <td className="px-3 py-2">
                            <select
                              value={item.item_id}
                              onChange={(e) => handleLineItemChange(index, 'item_id', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            >
                              <option value="">Select Item</option>
                              {items.map(item => (
                                <option key={item.id} value={item.id}>{item.name}</option>
                              ))}
                            </select>
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="text"
                              value={item.description}
                              onChange={(e) => handleLineItemChange(index, 'description', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.quantity}
                              onChange={(e) => handleLineItemChange(index, 'quantity', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.rate}
                              onChange={(e) => handleLineItemChange(index, 'rate', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <input
                              type="number"
                              step="0.01"
                              value={item.amount}
                              readOnly
                              className="w-full p-2 border border-gray-300 rounded text-sm bg-gray-50"
                            />
                          </td>
                          <td className="px-3 py-2">
                            <select
                              value={item.account_id}
                              onChange={(e) => handleLineItemChange(index, 'account_id', e.target.value)}
                              className="w-full p-2 border border-gray-300 rounded text-sm"
                            >
                              <option value="">Select Account</option>
                              {expenseAccounts.map(account => (
                                <option key={account.id} value={account.id}>{account.name}</option>
                              ))}
                            </select>
                          </td>
                          <td className="px-3 py-2">
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

              {/* Totals */}
              <div className="flex justify-end">
                <div className="w-64 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Subtotal:</span>
                    <span className="text-sm font-medium">${calculateSubtotal().toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Tax Rate:</span>
                    <input
                      type="number"
                      step="0.01"
                      value={formData.tax_rate}
                      onChange={(e) => setFormData({...formData, tax_rate: e.target.value})}
                      className="w-16 p-1 border border-gray-300 rounded text-sm text-right"
                    />
                    <span className="text-sm text-gray-600">%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Tax Amount:</span>
                    <span className="text-sm font-medium">${calculateTax().toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between border-t pt-2">
                    <span className="text-lg font-medium">Total:</span>
                    <span className="text-lg font-bold">${calculateTotal().toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Memo</label>
                <textarea
                  value={formData.memo}
                  onChange={(e) => setFormData({...formData, memo: e.target.value})}
                  rows={2}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setSelectedBill(null);
                    resetForm();
                  }}
                  className="px-6 py-3 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {selectedBill ? 'Update Bill' : 'Save Bill'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const PayBillsPage = ({ vendors, transactions, accounts, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Pay Bills</h2>
    <p className="text-gray-600">Bill payment functionality coming soon...</p>
  </div>
);

const PurchaseOrdersPage = ({ transactions, vendors, items, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Purchase Orders</h2>
    <p className="text-gray-600">Purchase order functionality coming soon...</p>
  </div>
);

const ChecksPage = ({ accounts, vendors, items, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Write Checks</h2>
    <p className="text-gray-600">Check writing functionality coming soon...</p>
  </div>
);

const TransfersPage = ({ accounts, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Transfer Funds</h2>
    <p className="text-gray-600">Fund transfer functionality coming soon...</p>
  </div>
);

const ReconcilePage = ({ accounts, transactions }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Reconcile Accounts</h2>
    <p className="text-gray-600">Account reconciliation functionality coming soon...</p>
  </div>
);

// Reports Page Component (keeping existing implementation)
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
          <button
            onClick={() => setCurrentReport('ar-aging')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              currentReport === 'ar-aging'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            A/R Aging
          </button>
          <button
            onClick={() => setCurrentReport('ap-aging')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              currentReport === 'ap-aging'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            A/P Aging
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
            {/* Other report types would be implemented similarly */}
          </div>
        )}
      </div>
    </div>
  );
};

const MemorizedTransactionsPage = ({ memorizedTransactions, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Memorized Transactions</h2>
    <p className="text-gray-600">Memorized transaction functionality coming soon...</p>
  </div>
);

const CalendarPage = ({ todos, transactions, onRefresh }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Calendar & To-Dos</h2>
    <p className="text-gray-600">Calendar and task management functionality coming soon...</p>
  </div>
);

const AuditTrailPage = () => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Audit Trail</h2>
    <p className="text-gray-600">Audit trail functionality coming soon...</p>
  </div>
);

const UsersPage = ({ users, roles, onRefreshUsers, onRefreshRoles }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Users & Roles</h2>
    <p className="text-gray-600">User and role management functionality coming soon...</p>
  </div>
);

const ListsPage = ({ classes, locations, terms, priceLevels, onRefreshClasses, onRefreshLocations, onRefreshTerms, onRefreshPriceLevels }) => (
  <div>
    <h2 className="text-2xl font-bold text-gray-900 mb-6">Classes & Locations</h2>
    <p className="text-gray-600">Lists management functionality coming soon...</p>
  </div>
);

export default App;